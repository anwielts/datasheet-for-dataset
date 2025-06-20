"""Analyses to run depending on the type of data domain"""
from abc import ABC, abstractmethod
from typing import Union, List

import pandas as pd
import polars as pl
from pydantic import BaseModel


class TabularStatistics(BaseModel):
    column_name: str
    count: float = None
    highest_quantile: float | None = None # 75% percentile
    middle_quantile: float | None = None # 50% percentile
    lowest_quantile: float | None = None # 25% percentile
    max: float | None = None
    min: float | None = None
    mean: float | None = None
    std: float | None = None


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


TabularDataType = Union[pd.DataFrame, pl.DataFrame]


class TabularAnalysesStrategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def describe(self, data: TabularDataType):
        pass


class TabularDataContext():
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy: TabularAnalysesStrategy) -> None:
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """

        self._strategy = strategy

    @property
    def strategy(self) -> TabularAnalysesStrategy:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: TabularAnalysesStrategy) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """

        self._strategy = strategy

    def calculate_tabular_statistics(self, data: TabularDataType) -> None:
        """
        The Context delegates some work to the Strategy object instead of
        implementing multiple versions of the algorithm on its own.
        """
        result = self._strategy.describe(data)
        return result


class PolarsTabularAnalyses(TabularAnalysesStrategy):
    def describe(self, data: pl.DataFrame) -> List[TabularStatistics]:
        statistics = data.describe()
        stats_structured =  self._harmonized_statistics_structure(statistics)
        return stats_structured

    def _harmonized_statistics_structure(self, statistics_data: pl.DataFrame) -> List[TabularStatistics]:
        tabular_statistics = []
        for column in statistics_data.columns:
            if column != "statistic":
                count = statistics_data.filter(pl.col("statistic") == "count").select(pl.col(column))
                highest_quantile = statistics_data.filter(pl.col("statistic") == "75%").select(pl.col(column))
                middle_quantile = statistics_data.filter(pl.col("statistic") == "50%").select(pl.col(column))
                lowest_quantile = statistics_data.filter(pl.col("statistic") == "25%").select(pl.col(column))
                max = statistics_data.filter(pl.col("statistic") == "max").select(pl.col(column))
                min = statistics_data.filter(pl.col("statistic") == "min").select(pl.col(column))
                # polars sets max and min in categorical columns not how we want it so fix them here as None if they are srtings
                if isinstance(max.item(), str) and isinstance(min.item(), str):
                    max = None
                    min = None
                else:
                    max = max.item()
                    min = min.item()

                mean = statistics_data.filter(pl.col("statistic") == "mean").select(pl.col(column))
                std = statistics_data.filter(pl.col("statistic") == "std").select(pl.col(column))
                
                tab_stats = TabularStatistics(column_name=column,
                                            count=count.item(),
                                            highest_quantile = highest_quantile.item(),
                                            middle_quantile = middle_quantile.item(),
                                            lowest_quantile = lowest_quantile.item(),
                                            max = max,
                                            min = min,
                                            mean = mean.item(),
                                            std = std.item()
                                            )
                
                tabular_statistics.append(tab_stats)

        return tabular_statistics


class PandasTabularAnalyses(TabularAnalysesStrategy):
    def describe(self, data: pd.DataFrame) -> TabularStatistics:
        statistics = data.describe(include='all')
        stats_structured =  self._harmonized_statistics_structure(statistics)
        return stats_structured
    
    def _harmonized_statistics_structure(self, statistics_data: pd.DataFrame) -> TabularStatistics:
        tabular_statistics = []
        statistics_data = statistics_data.where(statistics_data.notnull(), None)
        for column in statistics_data:
            count = statistics_data[column].loc[["count"]]
            highest_quantile = statistics_data[column].loc[["75%"]]
            middle_quantile = statistics_data[column].loc[["50%"]]
            lowest_quantile = statistics_data[column].loc[["25%"]]
            max = statistics_data[column].loc[["max"]]
            min = statistics_data[column].loc[["min"]]
            mean = statistics_data[column].loc[["mean"]]
            std = statistics_data[column].loc[["std"]]

            tab_stats = TabularStatistics(column_name=column,
                                                count=count.item(),
                                                highest_quantile = highest_quantile.item(),
                                                middle_quantile = middle_quantile.item(),
                                                lowest_quantile = lowest_quantile.item(),
                                                max = max.item(),
                                                min = min.item(),
                                                mean = mean.item(),
                                                std = std.item()
                                                )
            tabular_statistics.append(tab_stats)

        return tabular_statistics
