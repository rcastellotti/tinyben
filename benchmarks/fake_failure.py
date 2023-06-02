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
        test_fullname="fake benchmark failure",
        test_shortname="fake-failure",
        test_status=":x:",
        test_result=None,
    )

    def pre(self):

        try:
            self.pre_return_code = subprocess.call(
                "does_not_exits", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            )
        except FileNotFoundError as e:
            pass

    def run_benchmark(self):

        if self.pre_return_code != 1:
            start_time = time.time()
            ret = subprocess.call("does_not_exist")
            print(ret)
            running_time = time.time() - start_time
            logging.info(f"--- {running_time} seconds ---")
            if ret != 1:
                print("ma qua ci siamo?")
                self.result.set_testStatus(":white_check_mark:")
                self.result.set_testResult(running_time)

        TinyBen.results.append(self.result)

    def post(self):
        pass
