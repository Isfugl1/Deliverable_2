import numpy as np


def remove_outliers(prices):

    arr = np.array(prices, dtype=float)

    mean = np.mean(arr)

    std = np.std(arr)

    mask = np.abs(arr - mean) > 3 * std

    valid = arr[~mask]

    median = np.median(valid)

    arr[mask] = median

    return arr


def compute_refund_ratio(
    sales_count,
    refund_count
):

    return refund_count / (
        sales_count + 1e-6
    )
