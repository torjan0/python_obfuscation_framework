import argparse
import os
import sys
import shutil
from pipeline import process_directory

def main():
    parser = argparse.ArgumentParser(description="Python Obfuscator")
    parser.add_argument("src", help="Source file or directory to obfuscate")
    parser.add_argument("dst", help="Destination file or directory for obfuscated code")
    parser.add_argument(
        "--level",
        choices=["none", "light", "medium", "heavy"],
        default="light",
        help="Obfuscation level",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    src_path = os.path.abspath(args.src)
    dst_path = os.path.abspath(args.dst)

    if os.path.isdir(src_path):
        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        if args.verbose:
            print(f"Copied source directory from {src_path} to {dst_path}")
    else:
        # Source is a file; ensure destination directory exists.
        dst_dir = os.path.dirname(dst_path)
        os.makedirs(dst_dir, exist_ok=True)
        shutil.copy(src_path, dst_path)
        if args.verbose:
            print(f"Copied source file from {src_path} to {dst_path}")

    # Process the directory or file.
    process_directory(dst_path, args.level, args.verbose)
    if args.verbose:
        print("Obfuscation complete.")

if __name__ == "__main__":
    main()
