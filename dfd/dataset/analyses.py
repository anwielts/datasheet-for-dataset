"""Analyses to run depending on the type of data domain"""
from typing import Union

import pandas as pd
import polars as pl
from pydantic import BaseModel


class TabularStatistics(BaseModel):
    column_name: str
    count: str
    lowest_quantile: float # 25% percentile


class BaseAnalyses:
    def __init__(self):
        pass
        # Define base analyses which should be run regardless of the data domain


class ImageAnalyses:
    def __init__(self):
        pass
        # Define base analyses which should be run on image datasets


class SoundAnalyses:
    def __init__(self):
        pass
        # Define base analyses which should be run on sound datasets


class TabularAnalyses:
    # TODO: Apply strategy pattern here (maybe)
    def __init__(self, data: Union[pd.DataFrame, pl.DataFrame]):
        if isinstance(data, pd.DataFrame) or isinstance(data, pl.DataFrame):
            self.data = data
            self.dataset_summary = self._descriptive_statistics()
        else:
            raise ValueError("Parameter 'data' is none of the supported types pd.DataFrame, pl.DataFrame")

    def _descriptive_statistics(self):
        # TODO: Align output of pandas and polars such that the returned stuff is the same shape and content
        if isinstance(self.data, pd.DataFrame):
            return self.data.describe(include='all')
        else:
            return self.data.describe()
