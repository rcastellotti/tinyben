"""
LZ4 compression algorithm benchmark
"""

import urllib.request
import logging
import tarfile
import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from base import TBBenchmarkBase
from tinyben import TinyBen
from tinyben import TinyBenResult

#  https://github.com/raas/mbw/archive/refs/tags/v2.0.tar.gz


class TBMbwBenchmark(TBBenchmarkBase):
    """LZ4 compression and decompression algorithm benchmark"""

    tardir = "mbw"
    filename = "v2.0"
    filename_tar_gz = filename + ".tar.gz"
    pre_return_code = 1
    cwd = ""
    result = TinyBenResult(
        benchmark_fullname="raas/mbw 1024 MiB",
        benchmark_shortname="mbw",
        benchmark_status=":x:",
        benchmark_result=None,
    )

    def pre(self):
        url = "https://github.com/raas/mbw/archive/refs/tags/" + self.filename_tar_gz

        if not os.path.exists(self.filename_tar_gz):
            logging.info("starting download: %s", url)
            urllib.request.urlretrieve(url, self.filename_tar_gz)
            logging.info("completed download: %s", url)

        with tarfile.open(self.filename_tar_gz) as tar:
            tar.extractall(path=self.tardir)
        self.cwd = self.tardir + "/" + os.listdir(self.tardir)[0]
        print(self.cwd)
        self.pre_return_code = subprocess.call(
            ["make"],
            cwd=self.cwd,
        )

    def run_benchmark(self):
        if self.pre_return_code == 0:
            Path("results").mkdir(parents=True, exist_ok=True)
            filename = f"results/mbw-{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}.txt"
            with open(filename, "a", encoding="utf-8") as f:
                ret = subprocess.call(["./mbw", "1024"], cwd=self.cwd, stdout=f)
            if ret == 0:
                self.result.set_benchmark_result(filename)
                self.result.set_benchmark_status(":white_check_mark:")
        TinyBen.results.append(self.result)

    def post(self):
        if self.pre_return_code == 0:
            shutil.rmtree(self.cwd)
            os.remove(self.filename_tar_gz)
