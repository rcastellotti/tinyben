import os
import subprocess
import time
import shutil
import argparse
import tinyben.common as common
from datetime import datetime


def main():
    timestamp=datetime.now()
    common.add_header_to_file("lz4", ["timestamp", "type", "completion_time_ms"])
    os.makedirs(".cache", exist_ok=True)

    if not os.path.exists(".cache/lz4"):
        common.download_file(
            "https://releases.ubuntu.com/jammy/ubuntu-22.04.2-desktop-amd64.iso",
            ".cache/ubuntu-22.04.2-desktop-amd64.iso",
            skip_if_exists=True,
        )

    start_time = time.time()
    subprocess.call(["lz4", "ubuntu-22.04.2-desktop-amd64.iso"], cwd=".cache/lz4")
    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("lz4", [timestamp, "compression", completion_time_ms])

    start_time = time.time()
    subprocess.call(
        ["lz4", "ubuntu-22.04.2-desktop-amd64.iso.lz4", "decompressed.iso"],
        cwd=".cache/lz4",
    )
    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("lz4", [timestamp, "decompression", completion_time_ms])
    
    shutil.rmtree(".cache/lz4")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tinyben lz4 benchmark")
    parser.add_argument("--runs", "-r", help="runs", type=int, default=1)
    args = parser.parse_args()
    for i in range(args.runs):
        main()
