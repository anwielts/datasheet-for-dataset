import pandas as pd
import polars as pl
import pytest

from dfd.create import Datasheet


# create test data
d = {"a": [1, 2], "b": [3, 4]}
df_pd = pd.DataFrame(data=d)
df_pl = pl.DataFrame(d)


def test_datasheet_creation():
    # should both work fine
    pandas_based_datasheet = Datasheet(data=df_pd)
    polars_based_datasheet = Datasheet(data=df_pl)

    # should raise an error
    with pytest.raises(ValueError):
        dict_based_datasheet = Datasheet(data=d)
