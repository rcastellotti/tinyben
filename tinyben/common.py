import csv
import os
import pathlib
import subprocess
import tempfile

import requests
from tqdm import tqdm

from tinyben.log import logger


def add_header_to_file(filename, row_to_append):
    os.makedirs("./results", exist_ok=True)
    file = f"./results/{filename}.csv"
    file_exists = os.path.exists(file)
    with open(file, "a+") as f:
        csv_writer = csv.writer(f)
        if not file_exists:
            csv_writer.writerow(row_to_append)


def add_to_result_file(filename, row_to_append):
    file = f"./results/{filename}.csv"
    # file_exists = os.path.exists(file)
    with open(file, "a+") as f:
        csv_writer = csv.writer(f, quotechar='"')
        # if not file_exists:
        csv_writer.writerow(row_to_append)


def append_to_txt_file(filename, data):
    os.makedirs("./results", exist_ok=True)

    file = f"./results/{filename}.txt"
    # file_exists = os.path.exists(file)
    with open(file, "a+") as f:
        # if not file_exists:
        f.write(data)


def download_file(url, fp, skip_if_exists=True):
    if skip_if_exists and os.path.isfile(fp) and os.stat(fp).st_size > 0:
        return
    r = requests.get(url, stream=True)
    assert r.status_code == 200
    progress_bar = tqdm(
        total=int(r.headers.get("content-length", 0)),
        unit="B",
        unit_scale=True,
        desc=url,
    )
    with tempfile.NamedTemporaryFile(dir=pathlib.Path(fp).parent, delete=False) as f:
        for chunk in r.iter_content(chunk_size=16384):
            progress_bar.update(f.write(chunk))
        f.close()
        os.rename(f.name, fp)


def log_command(popenargs, **kwargs):
    # adapted from https://gist.github.com/krzemienski/8c7e8e76c8652984cca0da3fea5b5368
    process = subprocess.Popen(
        popenargs, **kwargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    def check_io():
        while True:
            output = process.stdout.readline().decode().strip("\n")
            if output:
                logger.debug(output)
            else:
                break

    # keep checking stdout/stderr until the child exits
    while process.poll() is None:
        check_io()
