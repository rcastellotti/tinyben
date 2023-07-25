import os
import tarfile
import subprocess
from datetime import datetime
import common

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

    url = "https://github.com/redis/redis/archive/7.0.11.tar.gz"
    os.makedirs(".cache", exist_ok=True)
    common.download_file(
        url,
        ".cache/redis.tar.gz",
        skip_if_exists=True,
    )
    with tarfile.open(".cache/redis.tar.gz") as tar:
        tar.extractall(".cache/redis")

    cwd = os.path.join(".cache/redis/", os.listdir(".cache/redis")[0])
    subprocess.run(["make"], cwd=cwd)

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
    main()
