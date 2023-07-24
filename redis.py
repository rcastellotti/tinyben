import urllib.request
import logging
import os
import tarfile
import time
import subprocess
import shutil
from pathlib import Path
from datetime import datetime


CWD = os.path.realpath(__file__)
PARENT = os.path.dirname(os.path.dirname(CWD))

# https://redis.io/docs/management/optimization/benchmarks/
# https://redis.io/docs/getting-started/installation/install-redis-from-source/
# https://github.com/redis/redis/archive/7.0.11.tar.gz

tardir = "redis"
process = "redis-server-process"
filename = "7.0.11"
filename_tar_gz = filename + ".tar.gz"
pre_return_code = 1
cwd = ""
url = "https://github.com/redis/redis/archive/" + filename_tar_gz

if not os.path.exists(filename_tar_gz):
    logging.info("starting download: %s", url)
    urllib.request.urlretrieve(url, filename_tar_gz)
    logging.info("completed download: %s", url)

with tarfile.open(filename_tar_gz) as tar:
    tar.extractall(path=tardir)
cwd = tardir + "/" + os.listdir(tardir)[0]
pre_return_code = subprocess.call(["make"], cwd=cwd)
# pylint: disable=consider-using-with
process = subprocess.Popen(
    ["src/redis-server"],
    cwd=cwd,
    shell=True,
)
# give redis-server some time to come up
time.sleep(5)

logging.debug("pre phase return code: %s", pre_return_code)
if pre_return_code == 0:
    Path("results").mkdir(parents=True, exist_ok=True)
    filename = (
        f"results/redis-{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}.csv"
    )
    with open(filename, "a", encoding="utf-8") as f:
        ret = subprocess.call(
            ["src/redis-benchmark", "-q", "--csv"], cwd=cwd, stdout=f
        )
        print(ret)

subprocess.call(["src/redis-cli", "shutdown"], cwd=cwd)
shutil.rmtree(tardir)
os.remove(filename_tar_gz)
