import urllib.request
import logging
import os
import zipfile
import time
import subprocess
import shutil
import common

# make sure this benchmark has everything it needs like unzip?
# https://www.sqlite.org/howtocompile.html
# https://www.sqlite.org/2023/sqlite-amalgamation-3420000.zip




def main():
    print("hi")
    filename = "sqlite-amalgamation-3420000"
    filename_zip = filename + ".zip"
    pre_return_code = 1
    cwd = ""
    url = "https://www.sqlite.org/2023/" + filename_zip

    if not os.path.exists(filename_zip):
        logging.info("starting download: %s", url)
        urllib.request.urlretrieve(url, filename_zip)
        logging.info("completed download: %s", url)

    with zipfile.ZipFile(filename_zip, "r") as f:
        f.extractall(filename)
    cwd = filename + "/" + os.listdir(filename)[0]
    command = [
        "gcc",
        "shell.c",
        "sqlite3.c",
        "-lpthread",
        "-ldl",
        "-lm",
        "-o",
        "sqlite3",
    ]
    pre_return_code = subprocess.call(command, cwd=cwd)
    print(pre_return_code)
    os.chmod(cwd + "/sqlite3", 0o755)

    command = [
        "./sqlite3",
        "benchmark.db",
        """CREATE TABLE pts1 (
            'I' SMALLINT NOT NULL,
            'DT' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            'F1' VARCHAR(4) NOT NULL,
            'F2' VARCHAR(16) NOT NULL
            );""",
    ]
    os.chmod(cwd + "/sqlite3", 0o755)
    pre_return_code = subprocess.call(command, cwd=cwd)

    logging.debug("pre phase return code: %s", pre_return_code)
    if pre_return_code == 0:
        start_time = time.time()
        ret = subprocess.call(
            [
                "./sqlite3",
                "benchmark.db",
                ".read ../../assets/sqlite-2500-insertions.sql",
            ],
            cwd=cwd,
        )

        running_time = (time.time() - start_time) * 1000
        if ret == 0:
            common.save_to_file("sqlite", [start_time, running_time])
        shutil.rmtree(filename)
        os.remove(filename_zip)


if __name__ == "__main__":
    main()
