import os
import subprocess
import tarfile
from datetime import datetime

import tinyben.common as common


def main():
    cache = os.path.join(os.getcwd(), ".cache")
    os.makedirs(cache, exist_ok=True)
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
    cwd = os.path.join(cache, "redis")

    if not os.path.exists(cwd):
        os.makedirs(cwd)
        common.download_file(
            "https://github.com/redis/redis/archive/7.0.11.tar.gz",
            os.path.join(cache, "redis.tar.gz"),
            skip_if_exists=True,
        )
        with tarfile.open(os.path.join(cache, "redis.tar.gz")) as tar:
            tar.extractall(cwd)
        common.log_command(["make"], cwd=os.path.join(cwd, os.listdir(cwd)[0]))

    cwd = os.path.join(cwd, os.listdir(cwd)[0])
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
