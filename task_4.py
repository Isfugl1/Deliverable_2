import pandas as pd

from task3 import compute_refund_ratio


def build_dataframe(records):

    df = pd.DataFrame(records)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df = df.sort_values(
        "timestamp"
    )

    df = df.set_index(
        "timestamp"
    )

    return df


def hourly_revenue(df):

    return (
        df.groupby("item")
          .resample("1h")
          ["price"]
          .sum()
    )


def status_pivot(df):

    return pd.pivot_table(
        df,
        values="price",
        index="item",
        columns="status",
        aggfunc="sum",
        fill_value=0
    )


def refund_ratio_per_item(df):

    sales = (
        df[df["status"] == "SUCCESS"]
        .groupby("item")
        .size()
    )

    refunds = (
        df[df["status"] == "REFUND"]
        .groupby("item")
        .size()
    )

    sales, refunds = sales.align(
        refunds,
        fill_value=0
    )

    ratios = compute_refund_ratio(
        sales.to_numpy(),
        refunds.to_numpy()
    )

    return pd.DataFrame({
        "item": sales.index,
        "refund_ratio": ratios
    })
