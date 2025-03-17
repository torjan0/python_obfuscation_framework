import shutil

def copy_directory(src, dst):
    """Copy the source directory to the destination directory."""
    shutil.copytree(src, dst, dirs_exist_ok=True)
