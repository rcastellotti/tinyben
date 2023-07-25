import os
import subprocess
import time
import zipfile
from datetime import datetime

import tinyben.common as common


def main():
    cache = os.path.join(os.getcwd(), ".cache")
    os.makedirs(cache, exist_ok=True)
    common.add_header_to_file("sqlite", ["timestamp", "completion_time_ms"])
    cwd = os.path.join(cache, "sqlite")

    if not os.path.exists(cwd):
        os.makedirs(cwd)

        common.download_file(
            "https://www.sqlite.org/2023/sqlite-amalgamation-3420000.zip",
            os.path.join(cache, "sqlite.zip"),
            skip_if_exists=True,
        )
        with zipfile.ZipFile(os.path.join(cache, "sqlite.zip"), "r") as f:
            f.extractall(cwd)

        common.log_command(
            [
                "gcc",
                "-v",
                "shell.c",
                "sqlite3.c",
                "-lpthread",
                "-ldl",
                "-lm",
                "-o",
                "sqlite3",
            ],
            cwd=os.path.join(cwd, os.listdir(cwd)[0]),
        )

    cwd = os.path.join(cwd, os.listdir(cwd)[0])
    common.log_command(
        [
            "./sqlite3",
            "benchmark.db",
            """CREATE TABLE pts1 (
            'I' SMALLINT NOT NULL,
            'DT' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            'F1' VARCHAR(4) NOT NULL,
            'F2' VARCHAR(16) NOT NULL
            );""",
        ],
        cwd=cwd,
    )

    start_time = time.time()
    subprocess.call(
        [
            "./sqlite3",
            "benchmark.db",
            f".read {os.path.join(os.getcwd(),'assets','sqlite-2500-insertions.sql')}",
        ],
        cwd=cwd,
    )
    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("sqlite", [datetime.now(), completion_time_ms])

    os.remove(os.path.join(cwd, "benchmark.db"))
