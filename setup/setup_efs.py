import os
import shutil

EFS_MOUNT_PATH  = './mnt/efs'  # Local simulation
SRC_DEPS_PATH   = './efs_source_dependencies'

def log(msg):
    print(f"[setup_efs] {msg}")
    
def setup_dependencies():
    os.makedirs(SRC_DEPS_PATH, exist_ok=True)
    with open(os.path.join(SRC_DEPS_PATH, "dummy_lib.py"), "w") as f:
        f.write("# Dummy lib from EFS")

    target_path = os.path.join(EFS_MOUNT_PATH, "dependencies")
    os.makedirs(EFS_MOUNT_PATH, exist_ok=True)
    shutil.copytree(SRC_DEPS_PATH, target_path, dirs_exist_ok=True)
    log(f"Dependencies copied to simulated EFS path: {target_path}")