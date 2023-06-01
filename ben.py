import urllib.request
import pathlib
import subprocess
import tarfile
import logging
import subprocess
import os
import time

path = pathlib.Path(__file__).parent.resolve()
logging.basicConfig(level=logging.DEBUG)

# https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-16.0.4.tar.gz
# https://llvm.org/docs/GettingStarted.html#getting-the-source-code-and-building-llvm

llvm_tar_gz = "llvmorg-16.0.4.tar.gz"
if not os.path.exists(llvm_tar_gz):
    url = "https://github.com/llvm/llvm-project/archive/refs/tags/" + llvm_tar_gz
    logging.info(f"downloading llvm project: {url}")
    urllib.request.urlretrieve(url,llvm_tar_gz)

tar = tarfile.open(llvm_tar_gz)
if not os.path.exists("llvm-project"):
    tar.extractall(path="llvm-project")

llvm_dir=os.listdir("llvm-project")[0]
logging.info("running command: cmake -S llvm -DCMAKE_BUILD_TYPE=Release -B build -G Ninja")

p = subprocess.call(
    ["cmake", "-S llvm", "-DCMAKE_BUILD_TYPE=Release", "-B build", "-G Ninja"],
    cwd=f"llvm-project/{llvm_dir}",
)

start_time = time.time()

p = subprocess.call(
    ["ninja"],
    cwd=f"llvm-project/{llvm_dir}/build",
)
logging.info("--- %s seconds ---" % (time.time() - start_time))
