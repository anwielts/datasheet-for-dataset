"""Entry point for datasheet creation."""

from __future__ import annotations

from typing import Literal

import pandas as pd
import polars as pl

from dfd.dataset import TabularDataContext
from dfd.dataset.analyses import TabularAnalysesStrategy


class Datasheet:
    """Create and store insights for a tabular dataset."""

    def __init__(
        self,
        data: pd.DataFrame | pl.DataFrame,
        analysis: TabularAnalysesStrategy | Literal['auto', 'pandas', 'polars'] | None = 'auto',
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
        self.data_statistics = self._context.calculate_tabular_statistics(self.data)

    def _setup_layout(self) -> None:  # placeholder for future layout logic
        return None

    def create_datasheet(self) -> None:
        self._run_analyses()
        self._setup_layout()

    def store_datasheet(self) -> None:  # storage will be handled by compiler utilities
        return None
