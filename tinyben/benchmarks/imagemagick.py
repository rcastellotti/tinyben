# ""
#     tardir = "imagemagick"
#     filename = "7.1.1-11"
#     filename_tar_gz = filename + ".tar.gz"
#     pre_return_code = 1
#     cwd = ""
#     result = TinyBenResult(
#         benchmark_fullname="ImageMagick compilation (gcc)",
#         benchmark_shortname="imagemagick",
#         benchmark_status=":x:",
#         benchmark_result=None,
#     )

#     def pre(self):
#         url = (
#             "https://github.com/ImageMagick/ImageMagick/archive/refs/tags/"
#             + self.filename_tar_gz
#         )

#         if not os.path.exists(self.filename_tar_gz):
#             logging.info("starting download: %s", url)
#             urllib.request.urlretrieve(url, self.filename_tar_gz)
#             logging.info("completed download: %s", url)

#         with tarfile.open(self.filename_tar_gz) as tar:
#             tar.extractall(path=self.tardir)
#         self.cwd = self.tardir + "/" + os.listdir(self.tardir)[0]
#         print(self.cwd)
#         self.pre_return_code = subprocess.call(["./configure"], cwd=self.cwd)

#     def run_benchmark(self):
#         logging.debug("pre phase return code: %s", self.pre_return_code)
#         if self.pre_return_code == 0:
#             start_time = time.time()
#             ret = subprocess.call(["make", "-j", "4"], cwd=self.cwd)
#             running_time = time.time() - start_time
#             if ret == 0:
#                 self.result.set_benchmark_result(f"{running_time} s")
#                 self.result.set_benchmark_status(":white_check_mark:")

#         TinyBen.results.append(self.result)

#     def post(self):
#         shutil.rmtree(self.tardir)
#         os.remove(self.filename_tar_gz)

import tarfile
import os
import time
import shutil
import tinyben.common as common
import argparse


# https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-16.0.4.tar.gz
# https://llvm.org/docs/GettingStarted.html#getting-the-source-code-and-building-llvm


def main():
    common.add_header_to_file("imagemagick", ["timestamp", "completion_time_ms"])
    os.makedirs(".cache", exist_ok=True)

    if not os.path.exists(".cache/imagemagick"):
        common.download_file(
            "https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.1-11.tar.gz",
            ".cache/imagemagick.tar.gz",
            skip_if_exists=True,
        )

        with tarfile.open(".cache/imagemagick.tar.gz") as tar:
            tar.extractall(".cache/imagemagick")

        cwd = os.path.join(".cache/imagemagick", os.listdir(".cache/imagemagick")[0])

        common.log_command(
            ["./configure"],
            cwd=cwd,
        )

    cwd = os.path.join(".cache/imagemagick", os.listdir(".cache/imagemagick")[0])

    start_time = time.time()
    common.log_command(["make", "-j", "32"], cwd=cwd)
    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("imagemagick", [start_time, completion_time_ms])
    shutil.rmtree(cwd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tinyben imagemagick benchmark")
    parser.add_argument("--runs", "-r", help="runs", type=int, default=1)
    args = parser.parse_args()
    for i in range(args.runs):
        main()
