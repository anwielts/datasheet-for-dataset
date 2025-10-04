"""Public Python API for datasheet generation."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd
import polars as pl

from dfd.datasheet.compiler import DatasheetCompiler
from dfd.datasheet.manager import TemplateManager

DatasetBackend = Literal['auto', 'pandas', 'polars']
SUPPORTED_DATA_EXTENSIONS = {'.csv', '.tsv', '.parquet', '.json'}


def generate_template(output_path: str | None = None) -> str:
    """Generate an empty datasheet template and return its path."""
    manager = TemplateManager()
    output = Path(output_path) if output_path else Path('datasheet_template.md')
    output.parent.mkdir(parents=True, exist_ok=True)
    manager.generate_empty_template(str(output))
    return str(output.absolute())


def load_tabular_dataset(path: str, backend: DatasetBackend = 'auto') -> pd.DataFrame | pl.DataFrame:
    """Load a dataset into a pandas or polars DataFrame."""
    file_path = Path(path)
    if not file_path.exists():
        msg = f'Dataset file not found: {file_path}'
        raise FileNotFoundError(msg)

    extension = file_path.suffix.lower()
    if extension not in SUPPORTED_DATA_EXTENSIONS:
        msg = (
            f'Unsupported dataset format: {extension or "<none>"}. '
            'Supported formats: CSV, TSV, Parquet, and JSON.'
        )
        raise ValueError(msg)

    if backend == 'polars':
        if extension in {'.csv', '.tsv'}:
            separator = '\t' if extension == '.tsv' else ','
            return pl.read_csv(file_path, separator=separator)
        if extension == '.parquet':
            return pl.read_parquet(file_path)
        msg = 'Polars backend supports CSV, TSV, and Parquet inputs.'
        raise ValueError(msg)

    if extension == '.csv':
        return pd.read_csv(file_path)
    if extension == '.tsv':
        return pd.read_csv(file_path, sep='\t')
    if extension == '.parquet':
        return pd.read_parquet(file_path)
    return pd.read_json(file_path)


def build_datasheet(
    dataset_path: str,
    output_path: str,
    template_path: str | None = None,
    dataset_name: str | None = None,
    version: str = '1.0',
    backend: DatasetBackend = 'auto'
) -> str:
    """Compile a datasheet for a tabular dataset."""
    dataset = load_tabular_dataset(dataset_path, backend)
    compiler = DatasheetCompiler()

    if template_path:
        return compiler.compile_from_template(
            template_path=template_path,
            dataset=dataset,
            output_path=output_path,
            dataset_name=dataset_name or Path(dataset_path).stem,
            version=version
        )

    inferred_name = dataset_name or Path(dataset_path).stem
    return compiler.compile_from_scratch(
        dataset=dataset,
        output_path=output_path,
        dataset_name=inferred_name,
        manual_content=None,
        version=version
    )


__all__ = [
    'DatasetBackend',
    'SUPPORTED_DATA_EXTENSIONS',
    'build_datasheet',
    'generate_template',
    'load_tabular_dataset',
]
