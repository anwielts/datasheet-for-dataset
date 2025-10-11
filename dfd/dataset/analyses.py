"""Tabular data analyses utilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterable, Literal, Sequence, TypeAlias, TypeVar

import pandas as pd
import polars as pl
from pydantic import BaseModel

DataFrameType: TypeAlias = pd.DataFrame | pl.DataFrame
TabularDataType = TypeVar('TabularDataType', bound=DataFrameType)
allowed_backends = {'auto', 'pandas', 'polars'}

def _format_number(value: float | int | None) -> str:
    if value is None:
        return 'N/A'
    if isinstance(value, float):
        return f'{value:.4f}'
    return f'{value}'


class TabularStatistics(BaseModel):
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
    def format_tabular_statistics_to_markdown(statistics: Sequence['TabularStatistics']) -> str:
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
        strategy: TabularAnalysesStrategy | Literal['auto', 'pandas', 'polars'] | None = 'auto'
    ) -> None:
        self._strategy_specifier = strategy

    def _resolve_strategy(
        self,
        data: DataFrameType
    ) -> tuple[TabularAnalysesStrategy, DataFrameType]:
        if isinstance(self._strategy_specifier, TabularAnalysesStrategy):
            return self._strategy_specifier, data

        backend = 'auto' if self._strategy_specifier is None else self._strategy_specifier
        if backend not in allowed_backends:
            msg = f'Unknown analysis backend: {backend!r}'
            raise ValueError(msg)

        if backend == 'auto':
            if isinstance(data, pd.DataFrame):
                return PandasTabularAnalyses(), data
            if isinstance(data, pl.DataFrame):
                return PolarsTabularAnalyses(), data
            msg = f'Unsupported dataframe type: {type(data)!r}. Only pandas and polars are supported.'
            raise TypeError(msg)

        elif backend == 'pandas':
            if not isinstance(data, pd.DataFrame):
                if isinstance(data, pl.DataFrame):
                    converted = data.to_pandas()
                else:
                    converted = pd.DataFrame(data)
            else:
                converted = data
            return PandasTabularAnalyses(), converted

        elif backend == 'polars':
            if not isinstance(data, pl.DataFrame):
                if isinstance(data, pd.DataFrame):
                    converted = pl.DataFrame(data)
                else:
                    converted = pl.DataFrame(data)
            else:
                converted = data
        
        return PolarsTabularAnalyses(), converted
        
        else:
            raise ValueError(f'Unhandled backend: {backend!r}')

    def calculate_tabular_statistics(self, data: DataFrameType) -> list[TabularStatistics]:
        strategy, prepared = self._resolve_strategy(data)
        return strategy.describe(prepared)


class PandasTabularAnalyses(TabularAnalysesStrategy[pd.DataFrame]):
    def describe(self, data: pd.DataFrame) -> list[TabularStatistics]:
        statistics = data.describe(include='all')
        statistics = statistics.where(statistics.notna(), None)
        return list(self._to_statistics(statistics))

    def _to_statistics(self, statistics_data: pd.DataFrame) -> Iterable[TabularStatistics]:
        for column in statistics_data.columns:
            series = statistics_data[column]

            def pick(label: str) -> float | int | None:
                if label not in series.index:
                    return None
                value = series.loc[label]
                if pd.isna(value):
                    return None
                return value

            yield TabularStatistics(
                column_name=column,
                count=pick('count'),
                highest_quantile=pick('75%'),
                middle_quantile=pick('50%'),
                lowest_quantile=pick('25%'),
                max_val=pick('max'),
                min_val=pick('min'),
                mean_val=pick('mean'),
                std_val=pick('std')
            )


def to_float(value: float | int | None) -> float | None:
    if value is None:
        return None
    val = float(value)
    return val

class PolarsTabularAnalyses(TabularAnalysesStrategy[pl.DataFrame]):
    def describe(self, data: pl.DataFrame) -> list[TabularStatistics]:
        results: list[TabularStatistics] = []
        for column in data.columns:
            series = data[column]
            non_null = series.drop_nulls()
            count = float(non_null.len())

            if series.dtype.is_numeric():
                quantile = lambda q: to_float(non_null.quantile(q, interpolation='linear')) if non_null.len() else None
                mean_val = to_float(non_null.mean())
                std_val = to_float(non_null.std())
                max_val = to_float(non_null.max())
                min_val = to_float(non_null.min())
                highest = quantile(0.75)
                middle = quantile(0.5)
                lowest = quantile(0.25)
            else:
                mean_val = None
                std_val = None
                max_val = None
                min_val = None
                highest = None
                middle = None
                lowest = None

            results.append(
                TabularStatistics(
                    column_name=column,
                    count=count,
                    highest_quantile=highest,
                    middle_quantile=middle,
                    lowest_quantile=lowest,
                    max_val=max_val,
                    min_val=min_val,
                    mean_val=mean_val,
                    std_val=std_val,
                )
            )

        return results
