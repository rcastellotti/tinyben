"""
TBBenchmark ffmpeg compilation benchmark
"""

import urllib.request
import logging
import tarfile
import os
import subprocess
import time
import shutil
from tinyben import TinyBen
from tinyben import TinyBenResult
from base import TBBenchmarkBase


# option to choose how many cores?

# https://imagemagick.org/script/install-source.php#linux
# https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.1-11.tar.gz


class TBBenchmark(TBBenchmarkBase):
    """TBBenchmark ffmpeg compilation"""

    filename = "7.1.1-11"
    filename_tar_gz = filename + ".tar.gz"
    pre_return_code = 1
    cwd = ""
    result = TinyBenResult(
        test_fullname="ImageMagick compilation (gcc)",
        test_shortname="imagemagick",
        test_status=":x:",
        test_result=None,
    )

    def pre(self):
        url = (
            "https://github.com/ImageMagick/ImageMagick/archive/refs/tags/"
            + self.filename_tar_gz
        )

        if not os.path.exists(self.filename_tar_gz):
            logging.info("starting download: %s", url)
            urllib.request.urlretrieve(url, self.filename_tar_gz)
            logging.info("completed download: %s", url)

        with tarfile.open(self.filename_tar_gz) as tar:
            tar.extractall(path="imagemagick")
        self.cwd = "imagemagick/" + os.listdir("imagemagick")[0]
        print(self.cwd)
        self.pre_return_code = subprocess.call(["./configure"], cwd=self.cwd)

    def run_benchmark(self):
        logging.debug("pre phase return code: %s", self.pre_return_code)
        if self.pre_return_code == 0:
            start_time = time.time()
            ret = subprocess.call(["make", "-j", "4"], cwd=self.cwd)
            running_time = time.time() - start_time
            if ret == 0:
                self.result.set_test_result(running_time)
                self.result.set_test_status(":white_check_mark:")

        TinyBen.results.append(self.result)

    def post(self):
        shutil.rmtree(self.cwd)
        os.remove(self.filename_tar_gz)
