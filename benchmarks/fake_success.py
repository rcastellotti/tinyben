from base import TBBenchmark_base
import urllib.request
import logging
import tarfile
import os
import subprocess
import time
from tinyben import TinyBen
from tinyben import TinyBenResult


class TBBenchmark(TBBenchmark_base):
    pre_return_code = 1
    result = TinyBenResult(
        test_fullname="fake benchmark success",
        test_shortname="fake-success",
        test_status=":x:",
        test_result=None,
    )

    def pre(self):

        try:
            self.pre_return_code = subprocess.call(
                "ls", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            )
        except FileNotFoundError as e:
            pass

    def run_benchmark(self):

        if self.pre_return_code != 1:
            start_time = time.time()
            ret = subprocess.call(
                "ls", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            )
            running_time = time.time() - start_time

            if ret == 0:
                self.result.set_testResult(running_time)
                self.result.set_testStatus(":white_check_mark:")

        TinyBen.results.append(self.result)

    def post(self):
        pass
