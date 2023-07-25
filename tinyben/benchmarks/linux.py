import os
import tarfile
import time
import shutil
from datetime import datetime
import common
import argparse

# https://www.sqlite.org/howtocompile.html
# https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.3.5.tar.xz


def main():
    common.add_header_to_file("linux", ["timestamp", "completion_time_ms"])
    os.makedirs(".cache", exist_ok=True)

    if not os.path.exists(".cache/linux"):
        common.download_file(
            "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.3.5.tar.xz",
            ".cache/linux.tar.xz",
            skip_if_exists=True,
        )
        with tarfile.open(".cache/linux.tar.xz") as tar:
            tar.extractall(".cache/linux")

        cwd = os.path.join(".cache/linux", os.listdir(".cache/linux")[0])

        common.log_command(
            ["make", "defconfig"],
            cwd=cwd,
        )

    cwd = os.path.join(".cache/linux", os.listdir(".cache/linux")[0])
    start_time = time.time()

    common.log_command(
        ["make", "-j", "4"],
        cwd=cwd,
    )

    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("linux", [datetime.now(), completion_time_ms])

    shutil.rmtree(cwd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tinyben sqlite benchmark")
    parser.add_argument("--runs", "-r", help="runs", type=int, default=1)
    args = parser.parse_args()
    for i in range(args.runs):
        main()
