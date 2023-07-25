import os
import tarfile
import time
import shutil
from datetime import datetime
import tinyben.common as common
import argparse


def main():
    common.add_header_to_file("godot", ["timestamp", "completion_time_ms"])
    os.makedirs(".cache", exist_ok=True)

    if not os.path.exists(".cache/godot"):
        common.download_file(
            "https://github.com/godotengine/godot/archive/refs/tags/4.0.3-stable.tar.gz",
            ".cache/godot.tar.gz",
            skip_if_exists=True,
        )
        with tarfile.open(".cache/godot.tar.gz") as tar:
            tar.extractall(".cache/godot")

        cwd = os.path.join(".cache/godot", os.listdir(".cache/godot")[0])

    cwd = os.path.join(".cache/godot", os.listdir(".cache/godot")[0])
    start_time = time.time()

    common.log_command(
        ["scons", "platform=linuxbsd"],
        cwd=cwd,
    )

    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("godot", [datetime.now(), completion_time_ms])

    shutil.rmtree(cwd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tinyben godot benchmark")
    parser.add_argument("--runs", "-r", help="runs", type=int, default=1)
    args = parser.parse_args()
    for i in range(args.runs):
        main()
