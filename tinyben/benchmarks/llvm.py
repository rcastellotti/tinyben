import os
import shutil
import tarfile
import time

import tinyben.common as common


def main():
    cache = os.path.join(os.getcwd(), ".cache")
    os.makedirs(cache, exist_ok=True)
    common.add_header_to_file("llvm", ["timestamp", "completion_time_ms"])
    cwd = os.path.join(cache, "llvm")

    if not os.path.exists(cwd):
        os.makedirs(cwd)
        common.download_file(
            "https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-16.0.4.tar.gz",
            os.path.join(cache, "llvm.tar.gz"),
            skip_if_exists=True,
        )

        with tarfile.open(os.path.join(cache, "llvm.tar.gz")) as tar:
            tar.extractall(cwd)

        common.log_command(
            ["cmake", "-S llvm", "-DCMAKE_BUILD_TYPE=Release", "-B build", "-G Ninja"],
            cwd=os.path.join(cwd, os.listdir(cwd)[0]),
        )

    cwd = os.path.join(cwd, os.listdir(cwd)[0])

    start_time = time.time()
    common.log_command(["ninja"], cwd=os.path.join(cwd, "build"))
    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("llvm", [start_time, completion_time_ms])
    shutil.rmtree(cwd)
