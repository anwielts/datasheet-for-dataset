"""Entry point for datasheet creation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl

from dfd.dataset import TabularDataContext
from dfd.dataset.analyses import TabularAnalysesStrategy


class Datasheet:
    """Create and store insights for a tabular dataset."""

    def __init__(
        self,
        data: pd.DataFrame | pl.DataFrame,
        analysis: TabularAnalysesStrategy[pd.DataFrame | pl.DataFrame] | Literal['auto', 'pandas', 'polars'] | None = 'auto',
        layout: None = None,
        dataset_name: str | None = None
    ) -> None:
        self.layout = layout
        self.data = data
        self.dataset_name = dataset_name
        self._context = TabularDataContext(analysis)
        self.data_statistics = None
        self.datasheet_info_cards = None

    def _run_analyses(self) -> None:
        """Run analyses on the dataset to extract statistics and insights."""
        self.data_statistics = self._context.calculate_tabular_statistics(self.data)

    def _setup_layout(self) -> None:  # placeholder for future layout logic
        """Setup the layout for the datasheet based on the provided or default layout."""
        return

    def create_datasheet(self) -> None:
        """Create the datasheet by running analyses and setting up the layout."""
        self._run_analyses()
        self._setup_layout()

    def store_datasheet(self) -> None:  # storage will be handled by compiler utilities
        """Store the created datasheet in the desired format."""
        return
