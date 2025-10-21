from pathlib import Path

import pandas as pd
import polars as pl

from dfd.create import Datasheet
from dfd.dataset.analyses import TabularStatistics
from dfd.dataset.pandas_strategy import PandasTabularAnalyses
from dfd.dataset.polars_strategy import PolarsTabularAnalyses

# create test data
d = {'a': [1, 2], 'b': ['A', 'B']}
df_pd = pd.DataFrame(data=d)
df_pl = pl.DataFrame(d)

# expected tabular statistics for polars and pandas - keep in mind they differ
tab_stats_pl = [
    TabularStatistics(
        column_name='a',
        count=2.0,
        highest_quantile=2.0,
        middle_quantile=2.0,
        lowest_quantile=1.0,
        max_val=2.0,
        min_val=1.0,
        mean_val=1.5,
        std_val=0.7071067811865476,
    ),
    TabularStatistics(
        column_name='b',
        count=2.0,
        highest_quantile=None,
        middle_quantile=None,
        lowest_quantile=None,
        max_val=None,
        min_val=None,
        mean_val=None,
        std_val=None,
    ),
]

tab_stats_pd = [
    TabularStatistics(
        column_name='a',
        count=2.0,
        highest_quantile=1.75,
        middle_quantile=1.5,
        lowest_quantile=1.25,
        max_val=2.0,
        min_val=1.0,
        mean_val=1.5,
        std_val=0.7071067811865476,
    ),
    TabularStatistics(
        column_name='b',
        count=2.0,
        highest_quantile=None,
        middle_quantile=None,
        lowest_quantile=None,
        max_val=None,
        min_val=None,
        mean_val=None,
        std_val=None,
    ),
]


def test_datasheet_creation():
    polars_based_datasheet = Datasheet(data=df_pl, analysis=PolarsTabularAnalyses())
    stats_pl = polars_based_datasheet.create_datasheet()
    assert stats_pl == tab_stats_pl
    assert polars_based_datasheet.statistics == tab_stats_pl

    pandas_based_datasheet = Datasheet(data=df_pd, analysis=PandasTabularAnalyses())
    stats_pd = pandas_based_datasheet.create_datasheet()
    assert stats_pd == tab_stats_pd
    assert pandas_based_datasheet.data_statistics == tab_stats_pd


def test_datasheet_from_path_and_export(tmp_path):
    dataset_file = tmp_path / 'sample.csv'
    df_pd.to_csv(dataset_file, index=False)

    datasheet = Datasheet.from_path(
        str(dataset_file),
        backend='pandas',
        dataset_name='Sample Dataset',
        analysis='pandas',
    )

    output_file = tmp_path / 'datasheet.md'
    result = datasheet.to_markdown(output_path=str(output_file), version='0.1')

    assert Path(result) == output_file
    content = output_file.read_text(encoding='utf-8')
    assert 'Total rows: 2' in content
    assert 'Mean: 1.5000' in content
