"""
LLVM project compilation (ninja) benchmark
"""

import urllib.request
import logging
import tarfile
import os
import subprocess
import time
import shutil
import common

# https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-16.0.4.tar.gz
# https://llvm.org/docs/GettingStarted.html#getting-the-source-code-and-building-llvm


filename = "llvmorg-16.0.4"
filename_tar_gz = filename + ".tar.gz"
pre_return_code = 1
cwd = ""

pre_return_code = subprocess.call(
    ["apt-get", "install", "-y", "cmake", "ninja-build"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT,
)
if pre_return_code != 0:
    logging.error("apt-get requires root permission")
    exit

url = "https://github.com/llvm/llvm-project/archive/refs/tags/" + filename_tar_gz

if not os.path.exists(filename_tar_gz):
    logging.info("starting download: %s", url)
    urllib.request.urlretrieve(url, filename_tar_gz)
    logging.info("completed download: %s", url)

with tarfile.open(filename_tar_gz) as tar:
    tar.extractall(path=filename)
cwd = filename + "/" + os.listdir(filename)[0]

pre_return_code = subprocess.call(
    ["cmake", "-S llvm", "-DCMAKE_BUILD_TYPE=Release", "-B build", "-G Ninja"],
    cwd=cwd,
)

if pre_return_code == 0:
    start_time = time.time()
    ret = subprocess.call(["ninja"], cwd=cwd + "/build")
    running_time = (time.time() - start_time) * 1000
    if ret == 0:
        common.save_to_file("llvm", [start_time, running_time])

if pre_return_code == 0:
    shutil.rmtree(filename)
    os.remove(filename_tar_gz)
