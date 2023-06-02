"""
TBBenchmark linux compilation (defconfig) benchmark
"""

import urllib.request
import logging
import tarfile
import os
import subprocess
import shutil
import time
from tinyben import TinyBen
from tinyben import TinyBenResult
from base import TBBenchmarkBase


# option to choose how many cores?
# https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.3.5.tar.xz


class TBBenchmark(TBBenchmarkBase):
    """TBBenchmark linux compilation (defconfig)"""

    filename = "linux-6.3.5"
    filename_tar_xz = filename + ".tar.xz"
    pre_return_code = 1
    cwd = ""
    result = TinyBenResult(
        benchmark_fullname="linux compilation (defconfig)",
        benchmark_shortname="linux",
        benchmark_status=":x:",
        benchmark_result=None,
    )

    def pre(self):
        url = "https://cdn.kernel.org/pub/linux/kernel/v6.x/" + self.filename_tar_xz

        self.pre_return_code = subprocess.call(
            [
                "apt-get",
                "install",
                "-y",
                "git",
                "fakeroot",
                "build-essential",
                "xz-utils",
                "libssl-dev",
                "bc",
                "flex",
                "libelf-dev",
                "bison",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        if self.pre_return_code != 0:
            logging.error("apt-get requires root permission")
            return

        if not os.path.exists(self.filename_tar_xz):
            logging.info("starting download: %s", url)
            urllib.request.urlretrieve(url, self.filename_tar_xz)
            logging.info("completed download: %s", url)

        with tarfile.open(self.filename_tar_xz) as tar:
            tar.extractall(path="linux")
        self.cwd = "linux/" + os.listdir("linux")[0]

        self.pre_return_code = subprocess.call(["make", "defconfig"], cwd=self.cwd)

    def run_benchmark(self):
        logging.debug("pre phase return code: %s", self.pre_return_code)
        if self.pre_return_code == 0:
            start_time = time.time()
            ret = subprocess.call(["make", "-j", "4"], cwd=self.cwd)
            running_time = time.time() - start_time
            if ret == 0:
                self.result.set_benchmark_result(running_time)
                self.result.set_benchmark_status(":white_check_mark:")

        TinyBen.results.append(self.result)

    def post(self):
        if self.pre_return_code == 0:
            shutil.rmtree(self.cwd)
            os.remove(self.filename_tar_xz)


# this of course requires root privileges
