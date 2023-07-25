import os
import subprocess
import time
from datetime import datetime
import tinyben.common as common


def main():
    cache = os.path.join(os.getcwd(), ".cache")
    os.makedirs(cache, exist_ok=True)
    timestamp = datetime.now()
    common.add_header_to_file("lz4", ["timestamp", "type", "completion_time_ms"])
    common.download_file(
        "https://releases.ubuntu.com/jammy/ubuntu-22.04.2-desktop-amd64.iso",
        os.path.join(cache, "ubuntu.iso"),
        skip_if_exists=True,
    )

    start_time = time.time()
    subprocess.call(["lz4", "ubuntu.iso"], cwd=cache)
    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("lz4", [timestamp, "compression", completion_time_ms])

    start_time = time.time()
    subprocess.call(
        ["lz4", "ubuntu.iso.lz4", "decompressed.iso"],
        cwd=cache,
    )
    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("lz4", [timestamp, "decompression", completion_time_ms])
    os.remove(os.path.join(cache, "ubuntu.iso.lz4"))
    os.remove(os.path.join(cache, "decompressed.iso"))
