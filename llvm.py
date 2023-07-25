import tarfile
import os
import time
import shutil
import common
import argparse


# https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-16.0.4.tar.gz
# https://llvm.org/docs/GettingStarted.html#getting-the-source-code-and-building-llvm


def main():
    common.add_header_to_file("llvm", ["timestamp", "completion_time_ms"])
    os.makedirs(".cache", exist_ok=True)

    if not os.path.exists(".cache/llvm"):
        common.download_file(
            "https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-16.0.4.tar.gz",
            ".cache/llvm.tar.gz",
            skip_if_exists=True,
        )

        with tarfile.open(".cache/llvm.tar.gz") as tar:
            tar.extractall(".cache/llvm")

        cwd = os.path.join(".cache/llvm", os.listdir(".cache/llvm")[0])

        common.log_command(
            ["cmake", "-S llvm", "-DCMAKE_BUILD_TYPE=Release", "-B build", "-G Ninja"],
            cwd=cwd,
        )

    cwd = os.path.join(".cache/llvm", os.listdir(".cache/llvm")[0])

    start_time = time.time()
    common.log_command(["ninja"], cwd=os.path.join(cwd, "/build"))
    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("llvm", [start_time, completion_time_ms])
    shutil.rmtree(cwd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tinyben llvm benchmark")
    parser.add_argument("--runs", "-r", help="runs", type=int, default=1)
    args = parser.parse_args()
    for i in range(args.runs):
        main()
