"""
TBBenchmark fake_success benchmark
"""


import subprocess
import time
from tinyben import TinyBen
from tinyben import TinyBenResult
from base import TBBenchmarkBase


class TBFakeSuccessBenchmark(TBBenchmarkBase):
    """TBBenchmark fake_success"""

    pre_return_code = 1
    result = TinyBenResult(
        benchmark_fullname="fake benchmark success",
        benchmark_shortname="fake_success",
        benchmark_status=":x:",
        benchmark_result=None,
    )

    def pre(self):
        try:
            self.pre_return_code = subprocess.call(
                "ls", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            )
        except FileNotFoundError:
            pass

    def run_benchmark(self):
        if self.pre_return_code != 1:
            start_time = time.time()
            ret = subprocess.call(
                "ls", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            )
            running_time = time.time() - start_time

            if ret == 0:
                self.result.set_benchmark_result(running_time)
                self.result.set_benchmark_status(":white_check_mark:")

        TinyBen.results.append(self.result)

    def post(self):
        pass
