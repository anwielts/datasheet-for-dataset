"""High-level Datasheet interface for analysing and exporting tabular datasets."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from dfd.dataset import TabularDataContext
from dfd.datasheet.compiler import DatasheetCompiler
from dfd.datasheet.manager import TemplateManager

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl

    from dfd.dataset.analyses import TabularAnalysesStrategy, TabularStatistics

    DataFrameType = pd.DataFrame | pl.DataFrame
else:
    DataFrameType = Any

DatasetBackend = Literal['auto', 'pandas', 'polars']
SUPPORTED_DATA_EXTENSIONS: set[str] = {'.csv', '.tsv', '.parquet', '.json'}


class Datasheet:
    """Create, analyse, and persist datasheets for tabular datasets."""

    def __init__(
        self,
        data: DataFrameType,
        *,
        analysis: TabularAnalysesStrategy | Literal['auto', 'pandas', 'polars'] | None = 'auto',
        dataset_name: str | None = None,
        dataset_backend: DatasetBackend | None = None,
    ) -> None:
        self.data = data
        self.dataset_name = dataset_name
        self.dataset_backend = dataset_backend
        self._analysis_specifier = analysis
        self._context = TabularDataContext(analysis)
        self._statistics: list[TabularStatistics] | None = None

    @property
    def statistics(self) -> list[TabularStatistics] | None:
        """Return cached statistics, if available."""
        return self._statistics

    @property
    def data_statistics(self) -> list[TabularStatistics] | None:
        """Alias for backwards compatibility with the previous attribute name."""
        return self._statistics

    @classmethod
    def from_path(
        cls,
        dataset_path: str,
        *,
        backend: DatasetBackend = 'auto',
        analysis: TabularAnalysesStrategy[DataFrameType] | Literal['auto', 'pandas', 'polars'] | None = 'auto',
        dataset_name: str | None = None,
    ) -> Datasheet:
        """Create a Datasheet instance from a dataset file."""
        data, resolved_backend = cls.load_tabular_dataset(dataset_path, backend=backend)
        name = dataset_name or Path(dataset_path).stem
        return cls(
            data=data,
            analysis=analysis,
            dataset_name=name,
            dataset_backend=resolved_backend,
        )

    @staticmethod
    def generate_template(output_path: str | None = None) -> str:
        """Generate an empty datasheet template and return its path."""
        manager = TemplateManager()
        target = Path(output_path) if output_path else Path('datasheet_template.md')
        target.parent.mkdir(parents=True, exist_ok=True)
        manager.generate_empty_template(str(target))
        return str(target.absolute())

    @classmethod
    def load_tabular_dataset(
        cls,
        path: str,
        *,
        backend: DatasetBackend = 'auto',
    ) -> tuple[DataFrameType, DatasetBackend]:
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

        if backend in {'polars', 'auto'}:
            try:
                import polars as pl
            except ModuleNotFoundError as exc:
                if backend == 'polars':
                    msg = 'Polars backend requires the "polars" package to be installed.'
                    raise ImportError(msg) from exc
            else:
                if extension in {'.csv', '.tsv'}:
                    separator = '\t' if extension == '.tsv' else ','
                    return pl.read_csv(file_path, separator=separator), 'polars'
                if extension == '.parquet':
                    return pl.read_parquet(file_path), 'polars'
                if backend == 'polars':
                    msg = 'Polars backend supports CSV, TSV, and Parquet inputs.'
                    raise ValueError(msg)

        if backend in {'pandas', 'auto'}:
            try:
                import pandas as pd
            except ModuleNotFoundError as exc:
                msg = 'Pandas backend requires the "pandas" package to be installed.'
                raise ImportError(msg) from exc

            if extension == '.csv':
                return pd.read_csv(str(file_path)), 'pandas'
            if extension == '.tsv':
                return pd.read_csv(file_path, sep='\t'), 'pandas'
            if extension == '.parquet':
                return pd.read_parquet(file_path), 'pandas'
            if extension == '.json':
                return pd.read_json(file_path), 'pandas'

        msg = 'Pandas backend supports CSV, TSV, Parquet, and JSON inputs.'
        raise ValueError(msg)

    def _run_analyses(self) -> list[TabularStatistics]:
        """Run analyses on the dataset to extract statistics and insights."""
        self._statistics = self._context.calculate_tabular_statistics(self.data)
        return self._statistics

    def analyse(self) -> list[TabularStatistics]:
        """Public method for triggering analysis."""
        return self._run_analyses()

    def create_datasheet(self) -> list[TabularStatistics]:
        """Retained for backwards compatibility; delegates to analyse()."""
        return self.analyse()

    def ensure_statistics(self) -> list[TabularStatistics]:
        """Return cached statistics or generate them when missing."""
        if self._statistics is None:
            return self._run_analyses()
        return self._statistics

    def to_markdown(
        self,
        output_path: str,
        *,
        template_path: str | None = None,
        version: str = '1.0',
        manual_content: dict[str, str] | None = None,
    ) -> str:
        """Write the datasheet to disk using the compiler."""
        statistics = self.ensure_statistics()
        compiler = DatasheetCompiler()
        dataset_name = self.dataset_name or 'Dataset'
        return compiler.compile(
            dataset=self.data,
            statistics=statistics,
            output_path=output_path,
            dataset_name=dataset_name,
            version=version,
            template_path=template_path,
            manual_content=manual_content,
        )

    def store_datasheet(
        self,
        output_path: str,
        *,
        template_path: str | None = None,
        version: str = '1.0',
        manual_content: dict[str, str] | None = None,
    ) -> str:
        """Alias for to_markdown() to preserve the previous public API."""
        return self.to_markdown(
            output_path,
            template_path=template_path,
            version=version,
            manual_content=manual_content,
        )
