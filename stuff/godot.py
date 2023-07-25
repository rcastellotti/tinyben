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
import common

# option to choose how many cores?


# https://github.com/godotengine/godot/releases/download/4.0.3-stable/Godot_v4.0.3-stable_linux.x86_64.zip
# https://docs.godotengine.org/en/stable/contributing/development/compiling/compiling_for_linuxbsd.html
# https://github.com/godotengine/godot/archive/refs/tags/4.0.3-stable.tar.gz

tardir = "godot"
filename = "4.0.3-stable"
filename_tar_gz = filename + ".tar.gz"
pre_return_code = 1
cwd = ""
pre_return_code = subprocess.call(
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
if pre_return_code != 0:
    logging.error("apt-get requires root permission")
    exit

url = "https://github.com/godotengine/godot/archive/refs/tags/" + filename_tar_gz

if not os.path.exists(filename_tar_gz):
    logging.info("starting download: %s", url)
    urllib.request.urlretrieve(url, filename_tar_gz)
    logging.info("completed download: %s", url)

with tarfile.open(filename_tar_gz) as tar:
    tar.extractall(path=tardir)
cwd = tardir + "/" + os.listdir(tardir)[0]

logging.debug("pre phase return code: %s", pre_return_code)
if pre_return_code == 0:
    start_time = time.time()
    ret = subprocess.call(["scons", "platform=linuxbsd"], cwd=cwd)
    running_time = (time.time() - start_time) * 1000
    if ret == 0:
        common.save_to_file("godot", [start_time, running_time])

if pre_return_code == 0:
    shutil.rmtree(tardir)
    os.remove(filename_tar_gz)
