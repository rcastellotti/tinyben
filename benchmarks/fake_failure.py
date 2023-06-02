"""
TBBenchmark fake_success benchmark
"""

import subprocess
import time
from tinyben import TinyBen
from tinyben import TinyBenResult
from base import TBBenchmarkBase


class TBBenchmark(TBBenchmarkBase):
    """TBBenchmark fake_failure compilation"""

    pre_return_code = 1
    result = TinyBenResult(
        benchmark_fullname="fake benchmark failure",
        benchmark_shortname="fake_failure",
        benchmark_status=":x:",
        benchmark_result=None,
    )

    def pre(self):
        try:
            self.pre_return_code = subprocess.call(
                "does_not_exits", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            )
        except FileNotFoundError:
            pass

    def run_benchmark(self):
        if self.pre_return_code != 1:
            start_time = time.time()
            ret = subprocess.call("does_not_exist")
            print(ret)
            running_time = time.time() - start_time
            if ret != 1:
                self.result.set_benchmark_status(":white_check_mark:")
                self.result.set_benchmark_result(running_time)

        TinyBen.results.append(self.result)

    def post(self):
        pass
