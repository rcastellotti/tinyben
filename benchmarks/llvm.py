"""
LLVM project compilation (ninja) benchmark
"""

import urllib.request
import logging
import tarfile
import os
import subprocess
import time
import shutil
from base import TBBenchmarkBase
from tinyben import TinyBen
from tinyben import TinyBenResult

# https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-16.0.4.tar.gz
# https://llvm.org/docs/GettingStarted.html#getting-the-source-code-and-building-llvm


class TBBenchmark(TBBenchmarkBase):
    """LLVM project compilation (ninja)"""

    filename = "llvmorg-16.0.4"
    filename_tar_gz = filename + ".tar.gz"
    pre_return_code = 1
    cwd = ""
    result = TinyBenResult(
        benchmark_fullname="llvm-project compilation (ninja)",
        benchmark_shortname="llvm",
        benchmark_status=":x:",
        benchmark_result=None,
    )

    def pre(self):
        self.pre_return_code = subprocess.call(
            ["apt-get", "install", "-y", "cmake", "ninja"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        if self.pre_return_code != 0:
            logging.error("apt-get requires root permission")
            return

        url = (
            "https://github.com/llvm/llvm-project/archive/refs/tags/"
            + self.filename_tar_gz
        )

        if not os.path.exists(self.filename_tar_gz):
            logging.info("starting download: %s", url)
            urllib.request.urlretrieve(url, self.filename_tar_gz)
            logging.info("completed download: %s", url)

        with tarfile.open(self.filename_tar_gz) as tar:
            tar.extractall(path=self.filename)
        self.cwd = self.filename + "/" + os.listdir(self.filename)[0]

        self.pre_return_code = subprocess.call(
            ["cmake", "-S llvm", "-DCMAKE_BUILD_TYPE=Release", "-B build", "-G Ninja"],
            cwd=self.cwd,
        )

    def run_benchmark(self):
        if self.pre_return_code == 0:
            start_time = time.time()
            ret = subprocess.call(["ninja"], cwd=self.cwd + "/build")
            running_time = time.time() - start_time
            if ret == 0:
                self.result.set_benchmark_result(f"{running_time} s")
                self.result.set_benchmark_status(":white_check_mark:")

        TinyBen.results.append(self.result)

    def post(self):
        if self.pre_return_code == 0:
            shutil.rmtree(self.filename)
            os.remove(self.filename_tar_gz)
