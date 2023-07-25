import os
import zipfile
import time
import subprocess
from datetime import datetime
import common
import argparse

# https://www.sqlite.org/howtocompile.html
# https://www.sqlite.org/2023/sqlite-amalgamation-3420000.zip


def main():
    common.add_header_to_file("sqlite", ["timestamp", "completion_time_ms"])
    os.makedirs(".cache", exist_ok=True)

    if not os.path.exists(".cache/sqlite"):
        common.download_file(
            "https://www.sqlite.org/2023/sqlite-amalgamation-3420000.zip",
            ".cache/sqlite.zip",
            skip_if_exists=True,
        )
        with zipfile.ZipFile("./.cache/sqlite.zip", "r") as f:
            f.extractall(".cache/sqlite")

        cwd = os.path.join(".cache/sqlite", os.listdir(".cache/sqlite")[0])

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
            cwd=cwd,
        )
        os.chmod(f"{cwd}/sqlite3", 0o755)

    cwd = os.path.join(".cache/sqlite", os.listdir(".cache/sqlite")[0])
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
            ".read ../../../../assets/sqlite-2500-insertions.sql",
        ],
        cwd=cwd,
    )
    completion_time_ms = (time.time() - start_time) * 1000
    common.add_to_result_file("sqlite", [datetime.now(), completion_time_ms])

    os.remove(os.path.join(cwd, "benchmark.db"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tinyben sqlite benchmark")
    parser.add_argument("--runs", "-r", help="runs", type=int, default=1)
    args = parser.parse_args()
    for i in range(args.runs):
        main()