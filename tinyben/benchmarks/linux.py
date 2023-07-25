import os
import shutil
import tarfile
import time
from datetime import datetime

import tinyben.common as common


def main():
    cache = os.path.join(os.getcwd(), ".cache")
    os.makedirs(cache, exist_ok=True)
    common.add_header_to_file("linux", ["timestamp", "completion_time_ms"])
    cwd = os.path.join(cache, "linux")

    if not os.path.exists(cwd):
        common.download_file(
            "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.3.5.tar.xz",
            os.path.join(cache, "linux.tar.xz"),
            skip_if_exists=True,
        )
        with tarfile.open(os.path.join(cache, "linux.tar.xz")) as tar:
            tar.extractall(cwd)

        print(os.path.join(cwd, os.listdir(cwd)[0]))
        common.log_command(
            ["make", "defconfig"],
            cwd=os.path.join(cwd, os.listdir(cwd)[0]),
        )

    cwd = os.path.join(cwd, os.listdir(cwd)[0])
    start_time = time.time()

    common.log_command(
        ["make", "-j", "4"],
        cwd=cwd,
    )

    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("linux", [datetime.now(), completion_time_ms])

    shutil.rmtree(cwd)
