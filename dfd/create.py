"""Entry point for datasheet creation"""
from typing import Union

import pandas as pd
import polars as pl

from dfd.dataset import ImageAnalyses, SoundAnalyses, TabularAnalyses
from dfd.datasheet.layout import BaseLayout, SafetyEU
from dfd.datasheet.structures import HumanDatasheet, NonHumanDatasheet

from dfd.utils import store_as_html, store_as_pdf


class Datasheet:
    def __init__(self, data: Union[pd.DataFrame, pl.DataFrame]):
        if isinstance(data, pd.DataFrame) or isinstance(data, pl.DataFrame):
            self.data = data
        else:
            raise ValueError("Parameter 'data' is none of the supported types pd.DataFrame, pl.DataFrame")
        # define input data domain
        # define layout to use
        # define structure to use

    def _run_analyses():
        pass
        # run specified analyses

    def _setup_layout():
        pass
        # setup specified layout

    def _create_structure():
        pass
        # setup specified structure

    def create_datasheet(self):
        pass
        # self._run_analyses
        # self._setup_layout
        # self._create_structure

    def store_datasheet(self):
        pass
        # store_as_html/store_as_pdf
