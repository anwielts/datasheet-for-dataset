"""Entry point for datasheet creation"""
from typing import Union

import pandas as pd
import polars as pl

from dfd.dataset import TabularDataContext, PolarsTabularAnalyses, PandasTabularAnalyses


class Datasheet:
    def __init__(self, data: Union[pd.DataFrame, pl.DataFrame], analysis: None,layout=None):
        self.analysis = analysis
        self.layout = layout
        self.data = data
        self.data_statistics = None
        self.datasheet_info_cards = None
        # define input data domain
        # define layout to use
        # define structure to use

    def _run_analyses(self):
        context = TabularDataContext(self.analysis)
        self.data_statistics = context.calculate_tabular_statistics(self.data)

    def _setup_layout():
        # setup specified layout
        pass

    def create_datasheet(self):
        self._run_analyses()
        # self._setup_layout
        # self._create_structure

    def store_datasheet(self):
        # store_as_html/store_as_pdf
        pass
