"""Entry point for datasheet creation"""
from enum import Enum
from typing import Union

import pandas as pd
import polars as pl

from dfd.dataset import TabularDataContext, PolarsTabularAnalyses, PandasTabularAnalyses
from dfd.datasheet.layout import BaseLayout, SafetyEU
from dfd.datasheet.structures import DatasheetInformationCard

from dfd.utils import Utility


class Datasheet:
    def __init__(self, data: Union[pd.DataFrame, pl.DataFrame], analysis=None, layout=None):
        self.analysis = analysis
        self.layout = layout
        self.data = data
        if not self.analysis:
            if isinstance(data, pd.DataFrame):
                self._run_analyses(PandasTabularAnalyses())
            elif isinstance(data, pl.DataFrame):
                self._run_analyses(PolarsTabularAnalyses())
            else:
                raise ValueError("Parameter 'data' is none of the supported types pd.DataFrame, pl.DataFrame")
        self.data_statistics = None
        # define input data domain
        # define layout to use
        # define structure to use

    def _run_analyses(self, analysis_type):
        context = TabularDataContext(analysis_type)
        self.data_statistics = context.calculate_tabular_statistics(self.data)

    def _setup_layout():
        pass
        # setup specified layout

    def create_datasheet(self):
        pass
        # self._run_analyses
        # self._setup_layout
        # self._create_structure

    def store_datasheet(self):
        pass
        # store_as_html/store_as_pdf
