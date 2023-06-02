from base import tb_benchmark_base
import urllib.request
import logging
import tarfile
import os
import subprocess
import time
from tinyben import TinyBen
from tinyben import TinyBenResult


# option to choose how many cores?
# https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.3.5.tar.xz


class tb_benchmark(tb_benchmark_base):
    filename = "linux-6.3.5"
    filename_tar_xz = filename + ".tar.xz"

    def pre(self):
        linux_tar_xz = "v6.x/" + self.filename_tar_xz
        url = "https://cdn.kernel.org/pub/linux/kernel/" + linux_tar_xz

        if not os.path.exists(self.filename_tar_xz):
            logging.info(f"starting download: {url}")
            urllib.request.urlretrieve(url, self.filename_tar_xz)
            logging.info(f"completed download: {url}")

        tar = tarfile.open(self.filename_tar_xz)
        # if not os.path.exists(filename_tar_xz):
        tar.extractall()

        ret = subprocess.call(["make", "defconfig"], cwd=self.filename)

    def run(self):
        # self.pre()
        start_time = time.time()
        # p = subprocess.call(["make", "-j" ,"4"], cwd=self.filename)
        running_time = time.time() - start_time
        # logging.info(f"--- {running_time} seconds ---")

        result = TinyBenResult(
            test_fullname="linux compilation (defconfig)",
            test_shortname="linux",
            test_result=running_time,
            test_status="[green]:white_check_mark:",
        )
        
        TinyBen.results.append(result)
        # self.post()

    def post(self):
        os.rmdir(self.filename)
        os.rmdir(self.filename_tar_xz)


# sudo apt-get install git fakeroot build-essential xz-utils libssl-dev bc flex libelf-dev bison
