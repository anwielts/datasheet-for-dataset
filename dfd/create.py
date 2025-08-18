"""Entry point for datasheet creation"""
import pandas as pd
import polars as pl

from dfd.dataset import TabularDataContext


class Datasheet:
    """
    A class to create and store data insights from a given DataFrame.

    Parameters:
        data: pd.DataFrame or pl.DataFrame, the input data.
        analysis: None, placeholder for potential future analysis settings.
        layout: None, placeholder for future layout customization options.

    Attributes:
        analysis: None, placeholder attribute for analysis settings.
        layout: None, placeholder attribute for layout customization options.
        data: pd.DataFrame or pl.DataFrame, the input DataFrame.
        data_statistics: Dict[str, Any], calculated statistics of the data.
        datasheet_info_cards: List[Dict[str, str]], information cards for the datasheet.

    Methods:
        _run_analyses(): Runs the analyses on the provided data and calculates statistical insights.
        create_datasheet(): Runs the analyses and creates a structured datasheet.
        store_datasheet(): Stores the created datasheet as an HTML file or PDF document.
    """
    def __init__(self, data: pd.DataFrame | pl.DataFrame, analysis: None, layout=None):
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
