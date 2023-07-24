"""
LZ4 compression algorithm benchmark
"""

import urllib.request
import logging
import tarfile
import os
import subprocess
import time
import shutil
from pathlib import Path
from base import TBBenchmarkBase
from tinyben import TinyBen
from tinyben import TinyBenResult

# https://github.com/lz4/lz4/archive/refs/tags/v1.9.4.tar.gz


class TBLz4Benchmark(TBBenchmarkBase):
    """LZ4 compression and decompression algorithm benchmark"""

    tardir = "lz4"
    filename = "v1.9.4"
    filename_tar_gz = filename + ".tar.gz"
    filename_iso = "ubuntu-22.04.2-desktop-amd64.iso"
    pre_return_code = 1
    cwd = ""
    result_compress = TinyBenResult(
        benchmark_fullname=f"lz4 compress {filename_iso}",
        benchmark_shortname="lz4-compress",
        benchmark_status=":x:",
        benchmark_result=None,
    )
    result_decompress = TinyBenResult(
        benchmark_fullname=f"lz4 decompress {filename_iso}.lz4",
        benchmark_shortname="lz4-decompress",
        benchmark_status=":x:",
        benchmark_result=None,
    )

    def pre(self):
        ubuntu_url = "https://releases.ubuntu.com/jammy/" + self.filename_iso
        Path(self.tardir).mkdir(parents=True, exist_ok=True)

        if not os.path.exists(self.tardir + "/" + self.filename_iso):
            logging.info("starting download: %s, might take a lot", ubuntu_url)
            urllib.request.urlretrieve(
                ubuntu_url, self.tardir + "/" + self.filename_iso
            )
            logging.info("completed download: %s", ubuntu_url)

        url = "https://github.com/lz4/lz4/archive/refs/tags/" + self.filename_tar_gz

        if not os.path.exists(self.filename_tar_gz):
            logging.info("starting download: %s", url)
            urllib.request.urlretrieve(url, self.filename_tar_gz)
            logging.info("completed download: %s", url)

        with tarfile.open(self.filename_tar_gz) as tar:
            tar.extractall(path=self.tardir)
        self.cwd = self.tardir + "/" + os.listdir(self.tardir)[1]
        print(self.cwd)
        self.pre_return_code = subprocess.call(
            ["make"],
            cwd=self.cwd,
        )

    def run_benchmark(self):
        if self.pre_return_code == 0:
            start_time = time.time()
            ret = subprocess.call(["./lz4", f"../{self.filename_iso}"], cwd=self.cwd)
            running_time = time.time() - start_time
            if ret == 0:
                self.result_compress.set_benchmark_result(f"{running_time} s")
                self.result_compress.set_benchmark_status(":white_check_mark:")
            start_time = time.time()
            ret = subprocess.call(
                ["./lz4", f"../{self.filename_iso}.lz4", "decompressed.iso"],
                cwd=self.cwd,
            )
            running_time = time.time() - start_time
            if ret == 0:
                self.result_decompress.set_benchmark_result(f"{running_time} s")
                self.result_decompress.set_benchmark_status(":white_check_mark:")
        TinyBen.results.append(self.result_compress)
        TinyBen.results.append(self.result_decompress)

    def post(self):
        if self.pre_return_code == 0:
            shutil.rmtree(self.cwd)
            os.remove(self.filename_tar_gz)
            os.remove(self.tardir + "/" + self.filename_iso + ".lz4")
