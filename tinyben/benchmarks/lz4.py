import os
import shutil
import subprocess
import time
from datetime import datetime

import tinyben.common as common


def main():
    cache = os.path.join(os.getcwd(), ".cache")
    timestamp = datetime.now()
    common.add_header_to_file("lz4", ["timestamp", "type", "completion_time_ms"])
    cwd = os.path.join(cache, "lz4")

    if not os.path.exists(cwd):
        os.makedirs(cwd, exist_ok=True)
        common.download_file(
            "https://releases.ubuntu.com/jammy/ubuntu-22.04.2-desktop-amd64.iso",
            os.path.join(cwd, "ubuntu-22.04.2-desktop-amd64.iso"),
            skip_if_exists=True,
        )

    start_time = time.time()
    subprocess.call(["lz4", "ubuntu-22.04.2-desktop-amd64.iso"], cwd=cwd)
    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("lz4", [timestamp, "compression", completion_time_ms])

    start_time = time.time()
    subprocess.call(
        ["lz4", "ubuntu-22.04.2-desktop-amd64.iso.lz4", "decompressed.iso"],
        cwd=cwd,
    )
    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("lz4", [timestamp, "decompression", completion_time_ms])

    shutil.rmtree(cwd)
