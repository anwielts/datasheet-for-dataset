"""Entry point for datasheet creation"""
from dataset import ImageAnalyses, SoundAnalyses, TabularAnalyses
from datasheet.layout import BaseLayout, SafetyEU
from datasheet.structures import HumanDatasheet, NonHumanDatasheet

from utils import store_as_html, store_as_pdf


class Datasheet:
    def __init__(self):
        pass
        # define input data domain
        # define layout to use
        # define structure to use

    def _run_analyses():
        pass
        # run specified analyses

    def _setup_layout():
        pass
        # setup sepcified layout

    def _create_structure():
        pass
        # setup sepcified structure

    def create_datasheet(self):
        pass
        # self._run_analyses
        # self._setup_layout
        # self._create_structure

    def store_datasheet(self):
        pass
        # store_as_html/store_as_pdf
