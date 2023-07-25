import os
import shutil
import tarfile
import time
import tinyben.common as common


def main():
    cache = os.path.join(os.getcwd(), ".cache")
    os.makedirs(cache, exist_ok=True)
    common.add_header_to_file("imagemagick", ["timestamp", "completion_time_ms"])
    cwd = os.path.join(cache, "imagemagick")

    if not os.path.exists(cwd):
        os.makedirs(cwd)
        common.download_file(
            "https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.1-11.tar.gz",
            os.path.join(cache, "imagemagick.tar.gz"),
            skip_if_exists=True,
        )

        with tarfile.open(
            os.path.join(cache, "imagemagick.tar.gz"),
        ) as tar:
            tar.extractall(cwd)

        common.log_command(
            ["./configure"],
            cwd=os.path.join(cwd, os.listdir(cwd)[0]),
        )

    cwd = os.path.join(cwd, os.listdir(cwd)[0])
    start_time = time.time()
    common.log_command(["make", "-j", "32"], cwd=cwd)
    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("imagemagick", [start_time, completion_time_ms])
    shutil.rmtree(cwd)
