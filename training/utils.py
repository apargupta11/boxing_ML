import numpy as np


def get_window(df, center_idx, before, after, sensor_columns):
    """
    Extract a sliding window centered at center_idx.
    """

    start = center_idx - before
    end = center_idx + after + 1

    return df.iloc[start:end][sensor_columns].values