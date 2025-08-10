"""Defines datasheet information cards for the datasheet structure."""
from pydantic import BaseModel

from dfd.dataset.analyses import TabularStatistics


class DatasheetInformationCard(BaseModel):
    heading: str
    sub_heading: str
    text: str
    result_data: list[TabularStatistics] | None = None # can be extended in future versions
    # plot: plotDataType, can be None
