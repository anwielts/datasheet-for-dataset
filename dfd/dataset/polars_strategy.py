"""Polars-based tabular data analyses strategy."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import polars as pl

from dfd.dataset.analyses import TabularAnalysesStrategy, TabularStatistics


class PolarsTabularAnalyses(TabularAnalysesStrategy['pl.DataFrame']):
    """Polars-based implementation of tabular data analyses."""

    def describe(self, data: pl.DataFrame) -> list[TabularStatistics]:
        """Return statistics for the given polars DataFrame.

        Args:
            data: The polars DataFrame to analyze.

        Returns:
            A list of TabularStatistics instances.
        """

        results: list[TabularStatistics] = []
        for column in data.columns:
            series = data[column]
            non_null = series.drop_nulls()
            count = non_null.len()

            def quantile(q: float, non_null: pl.Series = non_null, count: int = count) -> float | None:
                if count == 0:
                    return None
                q_value = non_null.quantile(q, interpolation='nearest')

                if q_value is None:
                    return None
                return float(q_value)

            if series.dtype.is_numeric() and count > 0:
                # We cast to float, otherwise typechecking makes me crazy
                std_val = cast('float', non_null.std())
                mean_val = cast('float', non_null.mean())
                max_val = cast('float', non_null.max())
                min_val = cast('float', non_null.min())
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
