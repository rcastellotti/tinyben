import os
import subprocess
from datetime import datetime
import tinyben.common as common
import argparse
import tarfile


def main():
    common.append_to_txt_file("tinymembench", f"tinymembench: {datetime.now()}\n")
    os.makedirs(".cache", exist_ok=True)

    if not os.path.exists(".cache/tinymembench"):
        common.download_file(
            "https://github.com/ssvb/tinymembench/archive/refs/tags/v0.4.tar.gz",
            ".cache/tinymembench.tar.gz",
            skip_if_exists=True,
        )
        with tarfile.open(".cache/tinymembench.tar.gz") as tar:
            tar.extractall(".cache/tinymembench")

        cwd = os.path.join(".cache/tinymembench", os.listdir(".cache/tinymembench")[0])

        common.log_command(["make"], cwd=cwd)

    cwd = os.path.join(".cache/tinymembench", os.listdir(".cache/tinymembench")[0])
    with open("results/tinymembench.txt", "a+", encoding="utf-8") as f:
        subprocess.call(["./tinymembench"], cwd=cwd, stdout=f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tinyben sqlite benchmark")
    parser.add_argument("--runs", "-r", help="runs", type=int, default=1)
    args = parser.parse_args()
    for i in range(args.runs):
        main()
