"""Analyses to run depending on the type of data domain"""

from abc import ABC, abstractmethod
from typing import (
    Generic,
    Optional,
    TypeVar
)

import pandas as pd
import polars as pl
from pydantic import BaseModel

TabularDataType = TypeVar("TabularDataType")

class TabularStatistics(BaseModel):
    column_name: str
    count: Optional[float] = None
    highest_quantile: Optional[float] = None  # 75% percentile
    middle_quantile: Optional[float] = None   # 50% percentile
    lowest_quantile: Optional[float] = None   # 25% percentile
    max_val: Optional[float] = None
    min_val: Optional[float] = None
    mean_val: Optional[float] = None
    std_val: Optional[float] = None
    
    @property
    def markdown(self) -> str:
        """Convert this TabularStatistics instance to markdown format.
        
        Returns:
            str: Markdown representation of the statistics for this column.
        """
        lines = []
        lines.append(f"**Column: {self.column_name}**")
        lines.append(f"- Count: {self.count}")
        
        if self.mean_val is not None:
            lines.append(f"- Mean: {self.mean_val:.4f}")
        if self.std_val is not None:
            lines.append(f"- Standard Deviation: {self.std_val:.4f}")
        if self.min_val is not None:
            lines.append(f"- Min: {self.min_val}")
        if self.max_val is not None:
            lines.append(f"- Max: {self.max_val}")
        if self.lowest_quantile is not None:
            lines.append(f"- 25th Percentile: {self.lowest_quantile}")
        if self.middle_quantile is not None:
            lines.append(f"- Median: {self.middle_quantile}")
        if self.highest_quantile is not None:
            lines.append(f"- 75th Percentile: {self.highest_quantile}")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_tabular_statistics_to_markdown(statistics: list["TabularStatistics"]) -> str:
        """Format a list of TabularStatistics to markdown format.
        
        Args:
            statistics: List of TabularStatistics to format.
            
        Returns:
            str: Markdown representation of all statistics with section header.
        """
        if not statistics:
            return ""
        
        lines = []
        lines.append("#### Statistical Analysis")
        lines.append("")
        
        for stat in statistics:
            lines.append(stat.markdown)
            lines.append("")
        
        return "\n".join(lines)


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


class TabularAnalysesStrategy(ABC, Generic[TabularDataType]):
    """Tabular analyses strategy interface defining common methods for all tabular analyses."""
    @abstractmethod
    def describe(self, data: TabularDataType) -> list[TabularStatistics]:
        """Describes the tabular data.

        Args:
            data (TabularDataType): The input tabular data to be analyzed.

        Returns:
            list[TabularStatistics]: A list of TabularStatistics objects.
        """


class TabularDataContext:
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


    def calculate_tabular_statistics(self, data: TabularDataType) -> list[TabularStatistics]:
        """Calculate and return the statistical information of the given tabular data.

        Args:
            data (TabularDataType): The data for which to calculate statistics.

        Returns:
            The result of the dedicatedly implemented analysis description method.
        """
        return self._strategy.describe(data)


class PolarsTabularAnalyses(TabularAnalysesStrategy[pl.DataFrame]):
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
        return self._harmonized_statistics_structure(statistics)


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
            if column != 'statistic':
                count = statistics_data.filter(pl.col('statistic') == 'count').select(pl.col(column))
                highest_quantile = statistics_data.filter(pl.col('statistic') == '75%').select(pl.col(column))
                middle_quantile = statistics_data.filter(pl.col('statistic') == '50%').select(pl.col(column))
                lowest_quantile = statistics_data.filter(pl.col('statistic') == '25%').select(pl.col(column))
                max_val_col = statistics_data.filter(pl.col('statistic') == 'max').select(pl.col(column))
                min_val_col = statistics_data.filter(pl.col('statistic') == 'min').select(pl.col(column))
                # polars sets max and min in categorical columns not how we want it so fix them here as None if they are srtings
                if isinstance(max_val_col.item(), str) and isinstance(min_val_col.item(), str):
                    max_val = None
                    min_val = None
                else:
                    max_val = max_val_col.item()
                    min_val = min_val_col.item()

                mean_val_col = statistics_data.filter(pl.col('statistic') == 'mean').select(pl.col(column))
                std_val_col = statistics_data.filter(pl.col('statistic') == 'std').select(pl.col(column))

                tab_stats = TabularStatistics(column_name=column,
                                            count=count.item(),
                                            highest_quantile = highest_quantile.item(),
                                            middle_quantile = middle_quantile.item(),
                                            lowest_quantile = lowest_quantile.item(),
                                            max_val = max_val,
                                            min_val = min_val,
                                            mean_val = mean_val_col.item(),
                                            std_val = std_val_col.item()
                                            )

                tabular_statistics.append(tab_stats)

        return tabular_statistics


class PandasTabularAnalyses(TabularAnalysesStrategy[pd.DataFrame]):
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
        return self._harmonized_statistics_structure(statistics)


    def _harmonized_statistics_structure(self, statistics_data: pd.DataFrame) -> list[TabularStatistics]:
        """Harmonize the pandas DataFrame statistics into a structured list of TabularStatistics.

        Args:
            statistics_data (pd.DataFrame): The input pandas DataFrame containing statistical data.

        Returns:
            list[TabularStatistics]: A list of structured tabular statistics.
        """
        tabular_statistics = []
        statistics_data = statistics_data.where(statistics_data.notna(), None)
        for column in statistics_data:
            count = statistics_data[column].loc[['count']]
            highest_quantile = statistics_data[column].loc[['75%']]
            middle_quantile = statistics_data[column].loc[['50%']]
            lowest_quantile = statistics_data[column].loc[['25%']]
            max_val_col = statistics_data[column].loc[['max']]
            min_val_col = statistics_data[column].loc[['min']]
            mean_val_col = statistics_data[column].loc[['mean']]
            std_val_col = statistics_data[column].loc[['std']]

            tab_stats = TabularStatistics(column_name=column,
                                                count=count.item(),
                                                highest_quantile = highest_quantile.item(),
                                                middle_quantile = middle_quantile.item(),
                                                lowest_quantile = lowest_quantile.item(),
                                                max_val = max_val_col.item(),
                                                min_val = min_val_col.item(),
                                                mean_val = mean_val_col.item(),
                                                std_val = std_val_col.item()
                                                )
            tabular_statistics.append(tab_stats)

        return tabular_statistics
