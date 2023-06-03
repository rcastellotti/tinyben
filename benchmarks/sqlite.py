"""
TBBenchmark sqlite benchmark
This benchmark performs some actions (inserts) on a sqlite database
to measure I/O performance
"""

import urllib.request
import logging
import os
import zipfile
import time
import subprocess
import shutil
from base import TBBenchmarkBase
from tinyben import TinyBen, TinyBenResult


CWD = os.path.realpath(__file__)
PARENT = os.path.dirname(os.path.dirname(CWD))

# https://imagemagick.org/script/install-source.php#linux
# https://www.sqlite.org/2023/sqlite-amalgamation-3420000.zip


class TBBenchmark(TBBenchmarkBase):
    """TBBenchmark sqlite insertion"""

    filename = "sqlite-amalgamation-3420000"
    filename_zip = filename + ".zip"
    pre_return_code = 1
    cwd = ""
    result = TinyBenResult(
        benchmark_fullname="sqlite 2500 insertions",
        benchmark_shortname="sqlite",
        benchmark_status=":x:",
        benchmark_result=None,
    )

    def pre(self):
        url = "https://www.sqlite.org/2023/" + self.filename_zip

        if not os.path.exists(self.filename_zip):
            logging.info("starting download: %s", url)
            urllib.request.urlretrieve(url, self.filename_zip)
            logging.info("completed download: %s", url)

        with zipfile.ZipFile(self.filename_zip, "r") as f:
            f.extractall(self.filename)
        self.cwd = self.filename + "/" + os.listdir(self.filename)[0]
        command = [
            "gcc",
            "shell.c",
            "sqlite3.c",
            "-lpthread",
            "-ldl",
            "-lm",
            "-o",
            "sqlite3",
        ]
        self.pre_return_code = subprocess.call(command, cwd=self.cwd)
        print(self.pre_return_code)
        os.chmod(self.cwd + "/sqlite3", 0o755)

        command = [
            "./sqlite3",
            "benchmark.db",
            """CREATE TABLE pts1 (
                'I' SMALLINT NOT NULL,
                'DT' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                'F1' VARCHAR(4) NOT NULL,
                'F2' VARCHAR(16) NOT NULL
            );""",
        ]
        os.chmod(self.cwd + "/sqlite3", 0o755)
        self.pre_return_code = subprocess.call(command, cwd=self.cwd)

    def run_benchmark(self):
        logging.debug("pre phase return code: %s", self.pre_return_code)
        if self.pre_return_code == 0:
            start_time = time.time()
            ret = subprocess.call(
                [
                    "./sqlite3",
                    "benchmark.db",
                    ".read ../../assets/sqlite-2500-insertions.sql",
                ],
                cwd=self.cwd,
            )

            running_time = time.time() - start_time
            if ret == 0:
                self.result.set_benchmark_result(f"{running_time} s")
                self.result.set_benchmark_status(":white_check_mark:")

        TinyBen.results.append(self.result)

    def post(self):
        shutil.rmtree(self.filename)
        os.remove(self.filename_zip)
