"""Pandas-based tabular data analyses strategy."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from dfd.dataset.analyses import TabularAnalysesStrategy, TabularStatistics

if TYPE_CHECKING:
    from collections.abc import Iterable


class PandasTabularAnalyses(TabularAnalysesStrategy[pd.DataFrame]):
    """Pandas-based implementation of tabular data analyses."""

    def describe(self, data: pd.DataFrame) -> list[TabularStatistics]:
        """Return statistics for the given pandas DataFrame.

        Args:
            data: The pandas DataFrame to analyze.

        Returns:
            A list of TabularStatistics instances.
        """
        statistics = data.describe(include='all')
        statistics = statistics.where(statistics.notna(), None)
        return list(self._to_statistics(statistics))

    def _to_statistics(self, statistics_data: pd.DataFrame) -> Iterable[TabularStatistics]:
        """Convert pandas describe DataFrame to TabularStatistics instances.

        Args:
            statistics_data: The DataFrame returned by pandas describe().

        Returns:
            An iterable of TabularStatistics instances.
        """
        for column in statistics_data.columns:
            series = statistics_data[column]

            def pick(label: str, series: pd.Series = series) -> float | int | None:
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
