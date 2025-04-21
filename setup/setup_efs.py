import os
import shutil
import subprocess

EFS_MOUNT_PATH = '/mnt/efs'
SRC_DEPS_PATH = '/tmp/my_deps'  # where your deps are temporarily stored
DEST_DEPS_PATH = os.path.join(EFS_MOUNT_PATH, 'dependencies')


def log(msg):
    print(f"[setup_efs] {msg}")


def mount_efs(efs_dns):
    log(f"Mounting EFS from {efs_dns}...")
    os.makedirs(EFS_MOUNT_PATH, exist_ok=True)
    subprocess.run([
        "sudo", "mount", "-t", "nfs4", "-o", "nfsvers=4.1",
        f"{efs_dns}:/", EFS_MOUNT_PATH
    ], check=True)


def copy_to_efs():
    log(f"Copying dependencies from {SRC_DEPS_PATH} to {DEST_DEPS_PATH}...")
    shutil.copytree(SRC_DEPS_PATH, DEST_DEPS_PATH, dirs_exist_ok=True)


def main():
    efs_dns = os.environ.get("EFS_DNS_NAME")
    if not efs_dns:
        raise EnvironmentError("EFS_DNS_NAME is not set in environment variables")

    mount_efs(efs_dns)
    copy_to_efs()


if __name__ == "__main__":
    main()
