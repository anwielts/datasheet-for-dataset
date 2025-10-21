from typing import TYPE_CHECKING, TypeAlias
from typing_extensions import Literal, get_args, Any

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