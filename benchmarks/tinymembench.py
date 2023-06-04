"""
TBBenchmark imagemagick compilation benchmark
"""

import urllib.request
import logging
import tarfile
import os
import subprocess
from datetime import datetime
import shutil
from pathlib import Path
from base import TBBenchmarkBase
from tinyben import TinyBen, TinyBenResult


# option to choose how many cores?

# https://imagemagick.org/script/install-source.php#linux
# https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.1-11.tar.gz


class TBTinymembenchBenchmark(TBBenchmarkBase):
    """TBBenchmark imagemagick compilation"""

    tardir = "tinymembench"
    filename = "v0.4"
    filename_tar_gz = filename + ".tar.gz"
    pre_return_code = 1
    cwd = ""
    result = TinyBenResult(
        benchmark_fullname="ssvb/tinymembench",
        benchmark_shortname="tinymembench",
        benchmark_status=":x:",
        benchmark_result=None,
    )

    def pre(self):
        url = (
            "https://github.com/ssvb/tinymembench/archive/refs/tags/"
            + self.filename_tar_gz
        )

        if not os.path.exists(self.filename_tar_gz):
            logging.info("starting download: %s", url)
            urllib.request.urlretrieve(url, self.filename_tar_gz)
            logging.info("completed download: %s", url)

        with tarfile.open(self.filename_tar_gz) as tar:
            tar.extractall(path=self.tardir)
        self.cwd = self.tardir + "/" + os.listdir(self.tardir)[0]
        print(self.cwd)
        self.pre_return_code = subprocess.call(["make"], cwd=self.cwd)

    def run_benchmark(self):
        logging.debug("pre phase return code: %s", self.pre_return_code)
        if self.pre_return_code == 0:
            Path("results").mkdir(parents=True, exist_ok=True)
            filename = f"results/tinymembench-{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}.txt"
            with open(filename, "a", encoding="utf-8") as f:
                ret = subprocess.call(["./tinymembench"], cwd=self.cwd, stdout=f)
            if ret == 0:
                self.result.set_benchmark_result(filename)
                self.result.set_benchmark_status(":white_check_mark:")

        TinyBen.results.append(self.result)

    def post(self):
        shutil.rmtree(self.tardir)
        os.remove(self.filename_tar_gz)
