import os
import subprocess
import tarfile
from datetime import datetime
import tinyben.common as common


def main():
    cache = os.path.join(os.getcwd(), ".cache")
    os.makedirs(cache, exist_ok=True)
    common.append_to_txt_file("mbw", f"mbw: {datetime.now()}")
    cwd = os.path.join(cache, "mbw")
    if not os.path.exists(cwd):
        os.makedirs(cwd)
        common.download_file(
            "https://github.com/raas/mbw/archive/refs/tags/v2.0.tar.gz",
            os.path.join(cache, "mbw.tar.gz"),
            skip_if_exists=True,
        )
        with tarfile.open(os.path.join(cache, "mbw.tar.gz")) as tar:
            tar.extractall(cwd)

        common.log_command(
            ["make"],
            cwd=os.path.join(cwd, os.listdir(cwd)[0]),
        )

    cwd = os.path.join(cwd, os.listdir(cwd)[0])
    with open("results/mbw.txt", "a+", encoding="utf-8") as f:
        subprocess.call(["./mbw", "1024"], cwd=cwd, stdout=f)
