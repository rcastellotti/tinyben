import argparse
import os
import shutil
import tarfile
import time
from datetime import datetime

import tinyben.common as common


def main():
    cache = os.path.join(os.getcwd(), ".cache")
    os.makedirs(cache, exist_ok=True)

    common.add_header_to_file("godot", ["timestamp", "completion_time_ms"])
    cwd = os.path.join(cache, "godot")

    if not os.path.exists(cwd):
        os.makedirs(cwd)
        common.download_file(
            "https://github.com/godotengine/godot/archive/refs/tags/4.0.3-stable.tar.gz",
            os.path.join(cache, "godot.tar.gz"),
            skip_if_exists=True,
        )
        with tarfile.open(
            os.path.join(cache, "godot.tar.gz"),
        ) as tar:
            tar.extractall(cwd)

    cwd = os.path.join(cwd, os.listdir(cwd)[0])
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
