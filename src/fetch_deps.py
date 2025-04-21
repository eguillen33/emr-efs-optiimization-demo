import json
import os
import subprocess
import sys

CONFIG_PATH = '/mnt/bootstrap/config.json'
LOCAL_DEPS_PATH = '/home/hadoop/dependencies'
EFS_MOUNT_PATH = '/mnt/efs'
EFS_DNS = os.environ.get('EFS_DNS_NAME')  # Pass in from EMR config
S3_BUCKET = os.environ.get('S3_BUCKET', 'your-bucket')

def log(msg):
    print(f"[fetch_deps] {msg}")

def run_cmd(cmd, **kwargs):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, **kwargs)
    if result.returncode != 0:
        log(f"Command failed: {' '.join(cmd)}")
        log(f"stderr: {result.stderr}")
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result

def is_efs_mounted():
    with open("/proc/mounts", "r") as mounts:
        return any(EFS_MOUNT_PATH in line for line in mounts)

def mount_efs():
    if is_efs_mounted():
        log("EFS already mounted.")
        return
    log("Mounting EFS...")
    os.makedirs(EFS_MOUNT_PATH, exist_ok=True)
    run_cmd([
        "sudo", "mount", "-t", "nfs4", "-o", "nfsvers=4.1",
        f"{EFS_DNS}:/", EFS_MOUNT_PATH
    ], check=True)

def copy_from_efs():
    log("Copying dependencies from EFS...")
    run_cmd([
        "cp", "-r", os.path.join(EFS_MOUNT_PATH, "dependencies"), LOCAL_DEPS_PATH
    ], check=True)

def fetch_from_s3():
    log("Fetching dependencies from S3...")
    run_cmd([
        "aws", "s3", "cp", f"s3://{S3_BUCKET}/dependencies.tar.gz", "/tmp/"
    ], check=True)
    run_cmd([
        "tar", "-xzf", "/tmp/dependencies.tar.gz", "-C", "/home/hadoop/"
    ], check=True)

def main():
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    if config.get("use_efs"):
        mount_efs()
        copy_from_efs()
    else:
        fetch_from_s3()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"ERROR: {e}")
        sys.exit(1)
