import os
import subprocess
import tarfile
from datetime import datetime

import tinyben.common as common


def main():
    cache = os.path.join(os.getcwd(), ".cache")
    os.makedirs(cache, exist_ok=True)
    common.append_to_txt_file("tinymembench", f"tinymembench: {datetime.now()}\n")
    cwd = os.path.join(cache, "tinymembench")

    if not os.path.exists(cwd):
        os.makedirs(cwd)
        common.download_file(
            "https://github.com/ssvb/tinymembench/archive/refs/tags/v0.4.tar.gz",
            os.path.join(cache, "tinymembench.tar.gz"),
            skip_if_exists=True,
        )
        with tarfile.open(os.path.join(cache, "tinymembench.tar.gz")) as tar:
            tar.extractall(cwd)

        common.log_command(["make"], cwd=os.path.join(cwd, os.listdir(cwd)[0]))

    cwd = os.path.join(cwd, os.listdir(cwd)[0])
    with open("results/tinymembench.txt", "a+", encoding="utf-8") as f:
        subprocess.call(["./tinymembench"], cwd=cwd, stdout=f)
