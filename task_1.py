from pathlib import Path
import re

def read_log_file(file_path):

    file_path = Path(file_path)

    try:
        text = file_path.read_text(encoding="utf-8")
        return text, "utf-8"

    except UnicodeDecodeError:

        text = file_path.read_text(
            encoding="iso-8859-1"
        )

        return text, "iso-8859-1"


pattern = re.compile(
    r"\[(.*?)\]\s"
    r"\[(.*?)\]\s"
    r"item=(.*?)\s"
    r"price=([\d.]+)\s"
    r"(\w+)\s"
    r"\((.*?)\)"
)


def parse_log(text):

    records = []

    for line in text.splitlines():

        match = pattern.match(line)

        if match:

            record = {
                "timestamp": match.group(1),
                "register_id": match.group(2),
                "item": match.group(3),
                "price": float(match.group(4)),
                "currency": match.group(5),
                "status": match.group(6)
            }

            records.append(record)

    return records