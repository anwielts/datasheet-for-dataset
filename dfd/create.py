"""Entry point for datasheet creation"""
from enum import Enum
from typing import Union

import pandas as pd
import polars as pl

from dfd.dataset import ImageAnalyses, SoundAnalyses, TabularAnalyses
from dfd.datasheet.layout import BaseLayout, SafetyEU
from dfd.datasheet.structures import DatasheetInformationCard

from dfd.utils import store_as_html, store_as_pdf


class Analysis(Enum):
    IMAGE = 1
    SOUND = 2
    TABULAR = 3


class Datasheet:
    def __init__(self, data: Union[pd.DataFrame, pl.DataFrame], analysis=None, layout=None):
        self.analysis = analysis
        self.layout = layout
        if isinstance(data, pd.DataFrame) or isinstance(data, pl.DataFrame):
            self.data = data
            if not self.analysis:
                self._run_analyses(analysis_type=Analysis.TABULAR)
            if not self.layout:
                self._setup_layout()
        else:
            raise ValueError("Parameter 'data' is none of the supported types pd.DataFrame, pl.DataFrame")
        # define input data domain
        # define layout to use
        # define structure to use

    def _run_analyses(self, analysis_type: Analysis):
        if analysis_type is Analysis.TABULAR.value:
            pass
        # run specified analyses

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
