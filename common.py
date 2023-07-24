import csv
import os
def save_to_file(filename, row_to_append):
    file = f"./results/{filename}.csv"
    file_exists = os.path.exists(file)
    with open(file, "a+") as f:
        csv_writer = csv.writer(f)

        if not file_exists:
            if not file_exists:
                csv_writer.writerow(
                    [
                        "timestamp",
                        "insertion_time_ms",
                    ]
                )
        csv_writer.writerow(row_to_append)
