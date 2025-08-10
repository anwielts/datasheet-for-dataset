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

TabularDataType = Union[pd.DataFrame, pl.DataFrame]


class BaseAnalyses:
    def __init__(self):
        # Define base analyses which should be run regardless of the data domain
        pass


class ImageAnalyses:
    def __init__(self):
        # Define base analyses which should be run on image datasets
        pass


class SoundAnalyses:
    def __init__(self):
        # Define base analyses which should be run on sound datasets
        pass


class TabularAnalysesStrategy(ABC):
    """Tabular analyses strategy interface defining common methods for all tabular analyses."""
    @abstractmethod
    def describe(self, data: TabularDataType) -> None:
        """Describes the tabular data.

        Args:
            data (TabularDataType): The input tabular data to be analyzed.

        Returns:
            None
        """
        pass


class TabularDataContext():
    """Tabular data context defining the interfaces to clients.

    Attributes:
        _strategy (TabularAnalysesStrategy): The strategy used for calculating tabular statistics.
    """
    def __init__(self, strategy: TabularAnalysesStrategy) -> None:
        """Initialize a new instance of TabularDataContext with the specified strategy."""
        self._strategy = strategy


    @property
    def strategy(self) -> TabularAnalysesStrategy:
        """Get the current strategy used for calculating tabular statistics.

        Returns:
            TabularAnalysesStrategy: The current strategy.
        """
        return self._strategy


    @strategy.setter
    def strategy(self, strategy: TabularAnalysesStrategy) -> None:
        """Set a new strategy for calculating tabular statistics.

        Args:
            strategy (TabularAnalysesStrategy): A tabular analysis strategy.

        Returns:
            None
        """
        self._strategy = strategy


    def calculate_tabular_statistics(self, data: TabularDataType) -> None:
        """Calculate and return the statistical information of the given tabular data.

        Args:
            data (TabularDataType): The data for which to calculate statistics.

        Returns:
            The result of the dedicatedly implemented analysis description method.
        """
        result = self._strategy.describe(data)
        return result


class PolarsTabularAnalyses(TabularAnalysesStrategy):
    """Polars-based implementation of Tabular Analyses Strategy.

    This class extends the `TabularAnalysesStrategy` to analyze tabular data using polars.
    """
    def describe(self, data: pl.DataFrame) -> list[TabularStatistics]:
        """
        Describes the given dataframe by calculating various statistical measures such as count,
        mean, standard deviation, min, max, and 23%/50%/75% quantiles.

        Parameters:
            data (pl.DataFrame): The input Polars DataFrame to be analyzed.

        Returns:
            list[TabularStatistics]: A list of TabularStatistics objects containing
                                    computed statistics for each column.
        """
        statistics = data.describe()
        stats_structured =  self._harmonized_statistics_structure(statistics)
        return stats_structured


    def _harmonized_statistics_structure(self, statistics_data: pl.DataFrame) -> list[TabularStatistics]:
        """
        Constructs a structured representation of the given statistics data.

        Parameters:
            statistics_data (pl.DataFrame): The input DataFrame containing statistical information.

        Returns:
            list[TabularStatistics]: A list of TabularStatistics objects.
        """
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
    """Pandas-based implementation of Tabular Analyses Strategy.

    This class extends the `TabularAnalysesStrategy` to analyze tabular data using pandas.
    """
    def describe(self, data: pd.DataFrame) -> list[TabularStatistics]:
        """Describe the given DataFrame and return a list of statistics.

        Args:
            data (pd.DataFrame): The input DataFrame for analysis.

        Returns:
            list[TabularStatistics]: A list of tabular statistics including count, highest quantile,
                                    middle quantile, lowest quantile, maximum, minimum, mean, and standard deviation.
        """
        statistics = data.describe(include='all')
        stats_structured =  self._harmonized_statistics_structure(statistics)
        return stats_structured


    def _harmonized_statistics_structure(self, statistics_data: pd.DataFrame) -> list[TabularStatistics]:
        """Harmonize the pandas DataFrame statistics into a structured list of TabularStatistics.

        Args:
            statistics_data (pd.DataFrame): The input pandas DataFrame containing statistical data.

        Returns:
            list[TabularStatistics]: A list of structured tabular statistics.
        """
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
