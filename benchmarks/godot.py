"""
TBBenchmark Godot game engine compilation benchmark
"""

import urllib.request
import logging
import tarfile
import os
import subprocess
import shutil
import time
from tinyben import TinyBen
from tinyben import TinyBenResult
from base import TBBenchmarkBase


# option to choose how many cores?


# https://github.com/godotengine/godot/releases/download/4.0.3-stable/Godot_v4.0.3-stable_linux.x86_64.zip
# https://docs.godotengine.org/en/stable/contributing/development/compiling/compiling_for_linuxbsd.html
# https://github.com/godotengine/godot/archive/refs/tags/4.0.3-stable.tar.gz
class TBBenchmark(TBBenchmarkBase):
    """TBBenchmark Godot game engine compilation"""

    tardir = "godot"
    filename = "4.0.3-stable"
    filename_tar_gz = filename + ".tar.gz"
    pre_return_code = 1
    cwd = ""
    result = TinyBenResult(
        benchmark_fullname="Godot Game Enging compilation",
        benchmark_shortname="godot",
        benchmark_status=":x:",
        benchmark_result=None,
    )

    def pre(self):
        self.pre_return_code = subprocess.call(
            [
                "apt-get",
                "install",
                "-y",
                "build-essential",
                "scons",
                "pkg-config",
                "libx11-dev",
                "libxcursor-dev",
                "libxinerama-dev",
                "libgl1-mesa-dev",
                "libglu-dev",
                "libasound2-dev",
                "libpulse-dev",
                "libudev-dev",
                "libxi-dev",
                "libxrandr-dev",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        if self.pre_return_code != 0:
            logging.error("apt-get requires root permission")
            return

        url = (
            "https://github.com/godotengine/godot/archive/refs/tags/"
            + self.filename_tar_gz
        )

        if not os.path.exists(self.filename_tar_gz):
            logging.info("starting download: %s", url)
            urllib.request.urlretrieve(url, self.filename_tar_gz)
            logging.info("completed download: %s", url)

        with tarfile.open(self.filename_tar_gz) as tar:
            tar.extractall(path=self.tardir)
        self.cwd = self.tardir + "/" + os.listdir(self.tardir)[0]

    def run_benchmark(self):
        logging.debug("pre phase return code: %s", self.pre_return_code)
        if self.pre_return_code == 0:
            start_time = time.time()
            ret = subprocess.call(["scons", "platform=linuxbsd"], cwd=self.cwd)
            running_time = time.time() - start_time
            if ret == 0:
                self.result.set_benchmark_result(running_time)
                self.result.set_benchmark_status(":white_check_mark:")

        TinyBen.results.append(self.result)

    def post(self):
        shutil.rmtree(self.tardir)
        os.remove(self.filename_tar_gz)
