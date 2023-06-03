"""
TBBenchmark redis benchmark
This benchmark runs the tool redis-benchmarks some actions (inserts) on a sqlite database
to measure I/O performance
"""

import urllib.request
import logging
import os
import tarfile
import time
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from base import TBBenchmarkBase
from tinyben import TinyBen, TinyBenResult


CWD = os.path.realpath(__file__)
PARENT = os.path.dirname(os.path.dirname(CWD))

# https://redis.io/docs/management/optimization/benchmarks/
# https://redis.io/docs/getting-started/installation/install-redis-from-source/
# https://github.com/redis/redis/archive/7.0.11.tar.gz


class TBBenchmark(TBBenchmarkBase):
    """TBBenchmark redis-benchmark"""

    tardir = "redis"
    process = "redis-server-process"
    filename = "7.0.11"
    filename_tar_gz = filename + ".tar.gz"
    pre_return_code = 1
    cwd = ""
    result = TinyBenResult(
        benchmark_fullname="redis-benchmark",
        benchmark_shortname="redis",
        benchmark_status=":x:",
        benchmark_result=None,
    )

    def pre(self):
        url = "https://github.com/redis/redis/archive/" + self.filename_tar_gz

        if not os.path.exists(self.filename_tar_gz):
            logging.info("starting download: %s", url)
            urllib.request.urlretrieve(url, self.filename_tar_gz)
            logging.info("completed download: %s", url)

        with tarfile.open(self.filename_tar_gz) as tar:
            tar.extractall(path=self.tardir)
        self.cwd = self.tardir + "/" + os.listdir(self.tardir)[0]
        self.pre_return_code = subprocess.call(["make"], cwd=self.cwd)
        # pylint: disable=consider-using-with
        self.process = subprocess.Popen(
            ["src/redis-server"],
            cwd=self.cwd,
            shell=True,
        )
        # give redis-server some time to come up
        time.sleep(5)

    def run_benchmark(self):
        logging.debug("pre phase return code: %s", self.pre_return_code)
        if self.pre_return_code == 0:
            Path("results").mkdir(parents=True, exist_ok=True)
            filename = (
                f"results/redis-{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}.csv"
            )
            with open(filename, "a", encoding="utf-8") as f:
                ret = subprocess.call(
                    ["src/redis-benchmark", "-q", "--csv"], cwd=self.cwd, stdout=f
                )
                print(ret)
                if ret == 0:
                    self.result.set_benchmark_result(filename)
                    self.result.set_benchmark_status(":white_check_mark:")

        TinyBen.results.append(self.result)

    def post(self):
        subprocess.call(["src/redis-cli", "shutdown"], cwd=self.cwd)
        shutil.rmtree(self.tardir)
        os.remove(self.filename_tar_gz)
