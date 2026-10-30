from pathlib import Path

def find_log_files(folder):

    folder = Path(folder)

    log_files = []

    for item in folder.iterdir():

        if item.is_dir():

            log_files.extend(
                find_log_files(item)
            )

        elif (
            item.is_file()
            and item.suffix == ".log"
        ):

            log_files.append(item)

    return log_files


def get_active_registers(data):

    active = set()

    if isinstance(data, dict):

        if (
            "id" in data
            and data.get("active") is True
        ):
            active.add(data["id"])

        for value in data.values():

            active.update(
                get_active_registers(value)
            )

    elif isinstance(data, list):

        for item in data:

            active.update(
                get_active_registers(item)
            )

    return active
