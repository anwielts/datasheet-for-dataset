"""Defines datasheet structures"""
from pydantic import BaseModel


class DatasheetInformationCard(BaseModel):
    heading: str
    sub_heading: str
    text: str
    # result_data: resultDataType, can be None
    # plot: plotDataType, can be None
