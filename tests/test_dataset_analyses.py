import pandas as pd
import polars as pl
import pytest

from dfd.dataset.analyses import TabularDataContext, PolarsTabularAnalyses, PandasTabularAnalyses
from dfd.dataset.analyses import TabularStatistics


# create test data
d = {"a": [1, 2], "b": ["A", "B"]}
df_pd = pd.DataFrame(data=d)
df_pl = pl.DataFrame(d)

# expected tabular statistics for polars and pandas - keep in mind they differ
tab_stats_pl = [TabularStatistics(column_name='a', count=2.0, highest_quantile=2.0, middle_quantile=2.0, lowest_quantile=1.0, max=2.0, min=1.0, mean=1.5, std=0.7071067811865476), 
             TabularStatistics(column_name='b', count=2.0, highest_quantile=None, middle_quantile=None, lowest_quantile=None, max=None, min=None, mean=None, std=None)]

tab_stats_pd = [TabularStatistics(column_name='a', count=2.0, highest_quantile=1.75, middle_quantile=1.5, lowest_quantile=1.25, max=2.0, min=1.0, mean=1.5, std=0.7071067811865476), 
             TabularStatistics(column_name='b', count=2.0, highest_quantile=None, middle_quantile=None, lowest_quantile=None, max=None, min=None, mean=None, std=None)]


def test_tabular_analyses():
    context = TabularDataContext(PolarsTabularAnalyses())
    stats_structure_pl = context.calculate_tabular_statistics(df_pl)
    assert stats_structure_pl == tab_stats_pl

    context = TabularDataContext(PandasTabularAnalyses())
    stats_structure_pd = context.calculate_tabular_statistics(df_pd)
    assert stats_structure_pd == tab_stats_pd
