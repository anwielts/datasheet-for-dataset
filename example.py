import pandas as pd
import polars as pl

from dfd.create import Datasheet
from dfd.dataset.analyses import PandasTabularAnalyses, PolarsTabularAnalyses, TabularDataContext
from dfd.datasheet.structures import DatasheetInformationCard

if __name__ == '__main__':
    # How to use the datasheet for dataset lib

    # Provided questionnaire
    datasheet_infos = [DatasheetInformationCard(heading='Example section 1', sub_heading='Intro', text='Example showcasing lib usage.'),
                       DatasheetInformationCard(heading='Example section 1', sub_heading='Motivation', text='One example speaks m9ore than 1000 words.'),
                       DatasheetInformationCard(heading='Example section 2', sub_heading='Data', text='Descriptive statistics for tabular example data.')]

    # provide example data, run tabular data analyses
    d = {'a': [1, 2], 'b': ['A', 'B']}
    df_pd = pd.DataFrame(data=d)
    df_pl = pl.DataFrame(d)

    # you can run the analysis on polars dataframes
    context = TabularDataContext(PolarsTabularAnalyses())
    stats_pl = context.calculate_tabular_statistics(df_pl)

    # or you can also run the analysis on pandas dataframes
    context = TabularDataContext(PandasTabularAnalyses())
    stats_pd = context.calculate_tabular_statistics(df_pd)

    # Create Datasheet
    datasheet = Datasheet(data=df_pl, analysis=PolarsTabularAnalyses())
    datasheet.datasheet_info_cards = datasheet_infos
    datasheet.create_datasheet()
    datasheet.datasheet_info_cards[2].result_data = datasheet.data_statistics
