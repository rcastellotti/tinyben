import os
import subprocess
from datetime import datetime
import tinyben.common as common
import argparse
import tarfile


def main():
    common.append_to_txt_file("mbw", f"mbw: {datetime.now()}")
    os.makedirs(".cache", exist_ok=True)

    if not os.path.exists(".cache/mbw"):
        common.download_file(
            "https://github.com/raas/mbw/archive/refs/tags/v2.0.tar.gz",
            ".cache/mbw.tar.gz",
            skip_if_exists=True,
        )
        with tarfile.open(".cache/mbw.tar.gz") as tar:
            tar.extractall(".cache/mbw")

        cwd = os.path.join(".cache/mbw", os.listdir(".cache/mbw")[0])

        common.log_command(["make"], cwd=cwd)

    cwd = os.path.join(".cache/mbw", os.listdir(".cache/mbw")[0])
    with open("results/mbw.txt", "a+", encoding="utf-8") as f:
        subprocess.call(["./mbw", "1024"], cwd=cwd, stdout=f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tinyben mbw benchmark")
    parser.add_argument("--runs", "-r", help="runs", type=int, default=1)
    args = parser.parse_args()
    for i in range(args.runs):
        main()
