import json

from task_1 import (
    read_log_file,
    parse_log
)

from task_2 import (
    find_log_files,
    get_active_registers
)

from task_3 import (
    remove_outliers
)

from task_4 import (
    build_dataframe,
    hourly_revenue,
    status_pivot,
    refund_ratio_per_item
)


def main():

    log_files = find_log_files(
        "d2_data"
    )

    with open(
        "d2_data/store_config.json",
        "r",
        encoding="utf-8"
    ) as f:

        config = json.load(f)

    active_registers = (
        get_active_registers(config)
    )

    print(
        "Active Registers:",
        active_registers
    )

    all_records = []

    for file in log_files:

        content, encoding = (
            read_log_file(file)
        )

        records = parse_log(
            content
        )

        all_records.extend(
            records
        )

    df = build_dataframe(
        all_records
    )

    df["price"] = remove_outliers(
        df["price"]
    )

    df.loc[
        df["currency"] == "NOK",
        "price"
    ] *= 10.0

    hourly_report = hourly_revenue(
        df
    )

    pivot_table = status_pivot(
        df
    )

    refund_report = (
        refund_ratio_per_item(df)
    )

    df.to_csv(
        "cleaned_transactions.csv"
    )

    hourly_report.to_json(
        "hourly_revenue.json"
    )

    pivot_table.to_csv(
        "status_pivot_table.csv"
    )

    refund_report.to_csv(
        "item_refund_ratios.csv",
        index=False
    )

    print(
        "Files created successfully!"
    )


if __name__ == "__main__":
    main()
