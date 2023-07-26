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
    subprocess.run(
        ["redis-server", "--daemonize", "yes"],
    
    )
    s = subprocess.check_output(
        ["redis-benchmark", "--csv"],
    
    )
    lines = s.decode().splitlines()[1:]
    for line in lines:
        line = [datetime.now()] + [x.strip('"') for x in line.split(",")]
        common.add_to_result_file("redis", line)
    subprocess.call(["redis-cli", "shutdown"])
