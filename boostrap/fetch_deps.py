import json
import os
import subprocess
import sys
import time

CONFIG_FILE     = './toggle/config.json'                       # Adjust if running locally
EFS_MOUNT_PATH  = './mnt/efs'                                  # Simulated mount path locally
LOCAL_DEPS_PATH = './local_dependencies'                       # Simulated target path
EFS_DNS_NAME    = os.environ.get("EFS_DNS_NAME", "dummy-efs")  # Dummy value for local run

def log(msg):
    print(f"[fetch_deps] {msg}")
    
def mount_efs():
    os.makedirs(EFS_MOUNT_PATH, exist_ok=True)
    log(f"Simulating EFS mount to {EFS_MOUNT_PATH} (EFS: {EFS_DNS_NAME})")
    
def copy_from_efs():
    log("Copying dependencies from EFS...")
    os.makedirs(LOCAL_DEPS_PATH, exist_ok=True)
    subprocess.run(["cp", "-r", os.path.join(EFS_MOUNT_PATH, "dependencies"), LOCAL_DEPS_PATH], check=True)
    
def fetch_from_remote():
    log("Fetching from remote (simulated)...")
    time.sleep(10)  # Simulate slow remote fetch
    os.makedirs(LOCAL_DEPS_PATH, exist_ok=True)
    with open(os.path.join(LOCAL_DEPS_PATH, "dummy_lib.py"), "w") as f:
        f.write("# Simulated downloaded dependency")

def main():
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
        use_efs = config.get("use_efs", False)

        log(f"Config: use_efs = {use_efs}")

        if use_efs:
            mount_efs()
            copy_from_efs()
        else:
            fetch_from_remote()

        log("Dependency setup complete.")

    except Exception as e:
        log(f"ERROR: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
