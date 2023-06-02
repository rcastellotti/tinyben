from base import tb_benchmark_base
import urllib.request
import logging
import tarfile
import os
import subprocess
import time
from tinyben import TinyBen
from tinyben import TinyBenResult
import shutil

# https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-16.0.4.tar.gz
# https://llvm.org/docs/GettingStarted.html#getting-the-source-code-and-building-llvm


class tb_benchmark(tb_benchmark_base):
    filename = "llvmorg-16.0.4"
    filename_tar_gz = filename + ".tar.gz"
    pre_return_code = 1
    cwd = ""
    result = TinyBenResult(
        test_fullname="llvm-project compilation (ninja)",
        test_shortname="llvm",
        test_status=":x:",
        test_result=None,
    )

    def pre(self):
        url = (
            "https://github.com/llvm/llvm-project/archive/refs/tags/"
            + self.filename_tar_gz
        )

        if not os.path.exists(self.filename_tar_xz):
            logging.info(f"starting download: {url}")
            urllib.request.urlretrieve(url, self.filename_tar_gz)
            logging.info(f"completed download: {url}")

        tar = tarfile.open(self.filename_tar_xz)
        tar.extractall(path="llvm")
        self.cwd = "llvm/" + os.listdir("llvm")[0]

        self.pre_return_code = subprocess.call(
            ["cmake", "-S llvm", "-DCMAKE_BUILD_TYPE=Release", "-B build", "-G Ninja"],
            cwd=self.cwd,
        )

    def run_benchmark(self):
        if self.pre_return_code == 0:
            start_time = time.time()
            ret = subprocess.call(["ninja"], cwd=self.filename)
            running_time = time.time() - start_time
            logging.info(f"--- {running_time} seconds ---")
            if ret == 0:
                self.result.set_testResult(running_time)
                self.result.set_testStatus(":white_check_mark:")

        TinyBen.results.append(self.result)

    def post(self):
        if self.pre_return_code == 0:
            shutil.rmtree(self.cwd)
            os.remove(self.filename_tar_gz)


