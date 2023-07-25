import os
import tarfile
import subprocess
from datetime import datetime
import tinyben.common as common
import argparse


# https://redis.io/docs/management/optimization/benchmarks/
# https://redis.io/docs/getting-started/installation/install-redis-from-source/
# https://github.com/redis/redis/archive/7.0.11.tar.gz


def main():
    common.add_header_to_file(
        "redis",
        [
            "timestamp",
            "test",
            "rps",
            "avg_latency_ms",
            "min_latency_ms",
            "p50_latency_ms",
            "p95_latency_ms",
            "p99_latency_ms",
            "max_latency_ms",
        ],
    )
    os.makedirs(".cache", exist_ok=True)
    if not os.path.exists(".cache/redis/"):
        common.download_file(
            "https://github.com/redis/redis/archive/7.0.11.tar.gz",
            ".cache/redis.tar.gz",
            skip_if_exists=True,
        )
        with tarfile.open(".cache/redis.tar.gz") as tar:
            tar.extractall(".cache/redis")
        cwd = os.path.join(".cache/redis/", os.listdir(".cache/redis")[0])
        common.log_command(["make"], cwd=cwd)

    cwd = os.path.join(".cache/redis/", os.listdir(".cache/redis")[0])
    subprocess.run(
        ["src/redis-server", "--daemonize", "yes"],
        cwd=cwd,
    )
    s = subprocess.check_output(
        ["src/redis-benchmark", "--csv"],
        cwd=cwd,
    )
    lines = s.decode().splitlines()[1:]

    for line in lines:
        line = [datetime.now()] + [x.strip('"') for x in line.split(",")]
        common.add_to_result_file("redis", line)

    subprocess.call(["src/redis-cli", "shutdown"], cwd=cwd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tinyben redis benchmark")
    parser.add_argument("--runs", "-r", help="runs", type=int, default=1)
    args = parser.parse_args()

    for i in range(args.runs):
        main()
