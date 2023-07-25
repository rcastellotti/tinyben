import urllib.request
import logging
import tarfile
import os
import subprocess
from datetime import datetime
import shutil
from pathlib import Path

# option to choose how many cores?



tardir = "tinymembench"
filename = "v0.4"
filename_tar_gz = filename + ".tar.gz"
pre_return_code = 1
cwd = ""

url = (
    "https://github.com/ssvb/tinymembench/archive/refs/tags/"
    + filename_tar_gz
)

if not os.path.exists(filename_tar_gz):
    logging.info("starting download: %s", url)
    urllib.request.urlretrieve(url, filename_tar_gz)
    logging.info("completed download: %s", url)

with tarfile.open(filename_tar_gz) as tar:
    tar.extractall(path=tardir)
cwd = tardir + "/" + os.listdir(tardir)[0]
print(cwd)
pre_return_code = subprocess.call(["make"], cwd=cwd)

logging.debug("pre phase return code: %s", pre_return_code)
if pre_return_code == 0:
    Path("results").mkdir(parents=True, exist_ok=True)
    filename = f"results/tinymembench.txt"
    with open(filename, "a+", encoding="utf-8") as f:
        f.write(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
        ret = subprocess.call(["./tinymembench"], cwd=cwd, stdout=f)


shutil.rmtree(tardir)
os.remove(filename_tar_gz)
