"""Common types and constants for the dfd package."""

from typing import TYPE_CHECKING, Literal, TypeAlias, get_args

from typing_extensions import Any

# Types
DatasetBackend = Literal['auto', 'pandas', 'polars']

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl

    DataFrameType = pd.DataFrame | pl.DataFrame
else:
    DataFrameType: TypeAlias = Any

# Constants
ALLOWED_BACKENDS = set(get_args(DatasetBackend))
SUPPORTED_DATA_EXTENSIONS: set[str] = {'.csv', '.tsv', '.parquet', '.json'}
