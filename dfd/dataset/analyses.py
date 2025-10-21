"""Tabular data analyses utilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Sequence, TypeVar, get_args

from pydantic import BaseModel

from dfd._common import DatasetBackend, ALLOWED_BACKENDS, DataFrameType

TabularDataType = TypeVar('TabularDataType', bound=DataFrameType)


def _format_number(value: float | None) -> str:
    """Format a number for markdown output.

    Args:
        value: The number to format.

    Returns:
        The formatted number as a string.
    """
    if value is None:
        return 'N/A'
    if isinstance(value, float):
        return f'{value:.4f}'
    return f'{value}'


class TabularStatistics(BaseModel):
    """Statistical analysis of a tabular data column."""
    column_name: str
    count: float | None = None
    highest_quantile: float | None = None
    middle_quantile: float | None = None
    lowest_quantile: float | None = None
    max_val: float | None = None
    min_val: float | None = None
    mean_val: float | None = None
    std_val: float | None = None

    @property
    def markdown(self) -> str:
        """Return the statistics as a markdown string."""
        lines: list[str] = [f'**Column: {self.column_name}**']
        lines.append(f'- Count: {_format_number(self.count)}')
        lines.append(f'- Mean: {_format_number(self.mean_val)}')
        lines.append(f'- Standard Deviation: {_format_number(self.std_val)}')
        lines.append(f'- Min: {_format_number(self.min_val)}')
        lines.append(f'- Max: {_format_number(self.max_val)}')
        lines.append(f'- 25th Percentile: {_format_number(self.lowest_quantile)}')
        lines.append(f'- Median: {_format_number(self.middle_quantile)}')
        lines.append(f'- 75th Percentile: {_format_number(self.highest_quantile)}')
        return '\n'.join(lines)

    @staticmethod
    def format_tabular_statistics_to_markdown(statistics: Sequence[TabularStatistics]) -> str:
        """Format a list of TabularStatistics to a markdown string.

        Args:
            statistics: The list of TabularStatistics to format.

        Returns:
            The formatted markdown string.
        """
        if not statistics:
            return ''
        lines = ['#### Statistical Analysis', '']
        for stat in statistics:
            lines.append(stat.markdown)
            lines.append('')
        return '\n'.join(lines).rstrip()


class TabularAnalysesStrategy(ABC, Generic[TabularDataType]):
    @abstractmethod
    def describe(self, data: TabularDataType) -> list[TabularStatistics]:
        """Return statistics for the given dataframe."""


class TabularDataContext:
    """Resolve an analysis strategy for the provided tabular data."""

    def __init__(
        self,
        strategy: TabularAnalysesStrategy | DatasetBackend | None = 'auto'
    ) -> None:
        self._strategy_specifier = strategy

    def _resolve_strategy(
        self,
        data: DataFrameType
    ) -> tuple[TabularAnalysesStrategy, DataFrameType]:
        """Resolve the analysis strategy and prepare the data if necessary.

        Args:
            data: The tabular data to analyze.

        Returns:
            A tuple of the resolved strategy and the prepared data.
        """
        if isinstance(self._strategy_specifier, TabularAnalysesStrategy):
            return self._strategy_specifier, data

        backend = 'auto' if self._strategy_specifier is None else self._strategy_specifier
        if backend not in ALLOWED_BACKENDS:
            msg = f'Unknown analysis backend: {backend!r}'
            raise ValueError(msg)

        if backend == 'auto':
            import pandas as pd
            if isinstance(data, pd.DataFrame):
                from dfd.dataset.pandas_strategy import PandasTabularAnalyses
                return PandasTabularAnalyses(), data
            import polars as pl
            if isinstance(data, pl.DataFrame):
                from dfd.dataset.polars_strategy import PolarsTabularAnalyses
                return PolarsTabularAnalyses(), data
            msg = f'Unsupported dataframe type: {type(data)!r}. Only pandas and polars are supported.'
            raise TypeError(msg)

        if backend == 'pandas':
            import pandas as pd
            if not isinstance(data, pd.DataFrame):
                msg = 'Only pandas DataFrame can be analyzed with pandas backend.'
                raise TypeError(msg)
            from dfd.dataset.pandas_strategy import PandasTabularAnalyses
            return PandasTabularAnalyses(), data

        if backend == 'polars':
            import polars as pl
            if not isinstance(data, pl.DataFrame):
                msg = 'Only polars DataFrame can be analyzed with polars backend.'
                raise TypeError(msg)
            from dfd.dataset.polars_strategy import PolarsTabularAnalyses
            return PolarsTabularAnalyses(), data

        msg = f'Unhandled backend: {backend!r}'
        raise ValueError(msg)

    def calculate_tabular_statistics(self, data: DataFrameType) -> list[TabularStatistics]:
        """Calculate tabular statistics for the provided data.

        Args:
            data: The tabular data to analyze.

        Returns:
            A list of TabularStatistics instances.
        """
        strategy, prepared = self._resolve_strategy(data)
        return strategy.describe(prepared)

