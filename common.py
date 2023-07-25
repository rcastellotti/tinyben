import csv
import os
from tqdm import tqdm
import tempfile
import requests
import pathlib


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
