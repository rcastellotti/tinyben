from base import TBBenchmark_base
import urllib.request
import logging
import tarfile
import os
import subprocess
import time
from tinyben import TinyBen
from tinyben import TinyBenResult
import shutil

# option to choose how many cores?
# https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.3.5.tar.xz


class TBBenchmark(TBBenchmark_base):
    filename = "linux-6.3.5"
    filename_tar_xz = filename + ".tar.xz"
    pre_return_code = 1
    cwd = ""
    result = TinyBenResult(
        test_fullname="linux compilation (defconfig)",
        test_shortname="linux",
        test_status=":x:",
        test_result=None,
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
            logging.info(f"starting download: {url}")
            urllib.request.urlretrieve(url, self.filename_tar_xz)
            logging.info(f"completed download: {url}")

        tar = tarfile.open(self.filename_tar_xz)
        tar.extractall(path="linux")
        self.cwd = "linux/" + os.listdir("linux")[0]

        self.pre_return_code = subprocess.call(["make", "defconfig"], cwd=self.cwd)

    def run_benchmark(self):
        logging.debug(f"pre phase return code: {self.pre_return_code}")
        if self.pre_return_code == 0:
            start_time = time.time()
            ret = subprocess.call(["make", "-j", "4"], cwd=self.cwd)
            running_time = time.time() - start_time
            logging.info(f"--- {running_time} seconds ---")
            if ret == 0:
                self.result.set_testResult(running_time)
                self.result.set_testStatus(":white_check_mark:")

        TinyBen.results.append(self.result)

    def post(self):
        if self.pre_return_code == 0:
            shutil.rmtree(self.cwd)
            os.remove(self.filename_tar_xz)


# this of course requires root privileges
