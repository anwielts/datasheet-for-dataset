from typing_extensions import Literal, get_args

# Types
DatasetBackend = Literal['auto', 'pandas', 'polars']

# Constants
ALLOWED_BACKENDS = set(get_args(DatasetBackend))
SUPPORTED_DATA_EXTENSIONS: set[str] = {'.csv', '.tsv', '.parquet', '.json'}