"""Datasheet compilation system for combining manual and automated content."""

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl

from dfd.create import Datasheet
from dfd.dataset.analyses import TabularDataContext, TabularStatistics

from .manager import TemplateManager
from .structures import CardType, DatasheetInformationCard, DatasheetSection, DatasheetStructure


def _format_number(value: float | None) -> str:
    """Format a number for display in the datasheet.
    
    Args:
        value: The number to format
    
    Returns:
        Formatted string representation of the number
    """
    if value is None:
        return 'N/A'
    if isinstance(value, float):
        return f'{value:.4f}'
    return f'{value}'


class DatasheetCompiler:
    """Compiles complete datasheets by combining manual content with automated analysis."""

    def __init__(self):
        self.template_manager = TemplateManager()

    def compile_from_template(
        self,
        template_path: str,
        dataset: 'pd.DataFrame | pl.DataFrame',
        output_path: str,
        dataset_name: str | None = None,
        version: str = '1.0'
    ) -> str:
        """Compile a complete datasheet from a filled template and dataset.
        
        Args:
            template_path: Path to the filled markdown template
            dataset: The tabular dataset to analyze
            output_path: Path where to save the compiled datasheet
            dataset_name: Name of the dataset (optional)
            version: Version of the datasheet
            
        Returns:
            Path to the compiled datasheet
        """
        # Load the filled template
        structure = self.template_manager.load_filled_template(template_path)

        # Update metadata
        if dataset_name:
            structure.title = f'Datasheet for {dataset_name}'
        structure.version = version
        structure.date_created = datetime.now().strftime('%Y-%m-%d')

        # Add automated analysis cards
        self._add_automated_analysis(structure, dataset)

        # Generate and save the compiled datasheet
        self.template_manager.save_structure_as_template(structure, output_path)

        return output_path

    def compile_from_scratch(
        self,
        dataset: 'pd.DataFrame | pl.DataFrame',
        output_path: str,
        dataset_name: str,
        manual_content: dict[str, str] | None = None,
        version: str = '1.0'
    ) -> str:
        """Compile a datasheet from scratch with minimal manual input.
        
        Args:
            dataset: The tabular dataset to analyze
            output_path: Path where to save the compiled datasheet
            dataset_name: Name of the dataset
            manual_content: Optional dictionary of manual content by section
            version: Version of the datasheet
            
        Returns:
            Path to the compiled datasheet
        """
        # Create base structure
        structure = DatasheetStructure(
            title=f'Datasheet for {dataset_name}',
            version=version,
            date_created=datetime.now().strftime('%Y-%m-%d')
        )

        # Add template cards with manual content if provided
        template_structure = self.template_manager.create_datasheet_structure()
        for card in template_structure.cards:
            card_copy = card.model_copy(deep=True)
            if manual_content:
                key = self._generate_content_key(card_copy)
                if key in manual_content:
                    card_copy.text = manual_content[key]
            structure.add_card(card_copy)

        # Add automated analysis cards
        self._add_automated_analysis(structure, dataset)

        # Generate and save the compiled datasheet
        self.template_manager.save_structure_as_template(structure, output_path)

        return output_path

    def create_datasheet_with_analysis(
        self,
        dataset: 'pd.DataFrame | pl.DataFrame',
        dataset_name: str,
        output_path: str,
        template_path: str | None = None
    ) -> Datasheet:
        """Create a Datasheet object with integrated analysis.
        
        Args:
            dataset: The tabular dataset to analyze
            dataset_name: Name of the dataset
            output_path: Path where to save the datasheet
            template_path: Optional path to filled template
            
        Returns:
            Configured Datasheet object
        """
        # Create datasheet structure
        if template_path:
            structure = self.template_manager.load_filled_template(template_path)
        else:
            structure = self.template_manager.create_datasheet_structure()

        # Update metadata
        structure.title = f'Datasheet for {dataset_name}'
        structure.date_created = datetime.now().strftime('%Y-%m-%d')

        # Convert structure to information cards for Datasheet
        info_cards = []
        for card in structure.cards:
            if card.card_type != CardType.AUTOMATED:
                info_cards.append(card)

        # Create Datasheet object with correct parameters
        if isinstance(dataset, pd.DataFrame):
            from dfd.dataset.analyses import PandasTabularAnalyses
            strategy = PandasTabularAnalyses()
        else:
            from dfd.dataset.analyses import PolarsTabularAnalyses
            strategy = PolarsTabularAnalyses()

        datasheet = Datasheet(
            data=dataset,
            analysis=None
        )

        return datasheet

    def _add_automated_analysis(
        self,
        structure: DatasheetStructure,
        dataset: 'pd.DataFrame | pl.DataFrame'
    ) -> None:
        """Add automated analysis cards to the datasheet structure.
        
        Args:
            structure: The datasheet structure to enhance
            dataset: The dataset to analyze
        """
        analysis_context = TabularDataContext(strategy='auto')
        stats_list = analysis_context.calculate_tabular_statistics(dataset)
        summary_stat = self._select_summary_stat(stats_list)

        stats_description = self._format_statistics_description(summary_stat, dataset, stats_list)
        stats_card = structure.find_card(
            section=DatasheetSection.AUTOMATED_ANALYSIS,
            sub_heading='Dataset Statistics'
        )

        if stats_card and (summary_stat or stats_list):
            stats_card.populate_automated(stats_description, stats_list)
            if summary_stat:
                stats_card.metadata['summary_column'] = summary_stat.column_name
        elif stats_list:
            fallback = DatasheetInformationCard.create_automated(
                section=DatasheetSection.AUTOMATED_ANALYSIS,
                heading='Dataset Statistics',
                description=stats_description,
                result_data=stats_list
            )
            structure.add_card(fallback)

        quality_description = self._format_quality_assessment(dataset)
        quality_card = structure.find_card(
            section=DatasheetSection.AUTOMATED_ANALYSIS,
            sub_heading='Data Quality Assessment'
        )
        if quality_card:
            quality_card.populate_automated(quality_description, [])
        else:
            quality = DatasheetInformationCard.create_automated(
                section=DatasheetSection.AUTOMATED_ANALYSIS,
                heading='Data Quality Assessment',
                description=quality_description,
                result_data=[]
            )
            structure.add_card(quality)

        self._fill_automated_placeholders(structure)

    def _select_summary_stat(
        self,
        statistics: list[TabularStatistics]
    ) -> TabularStatistics | None:
        """Select a representative statistical summary from the list.

        Args:
            statistics: List of TabularStatistics objects
        
        Returns:
            A representative TabularStatistics object or None if none found
        """
        for stat in statistics:
            if stat.mean_val is not None or stat.std_val is not None:
                return stat
        return statistics[0] if statistics else None

    def _format_statistics_description( # TODO: Use formatting function of class
        self,
        stats: TabularStatistics | None,
        dataset: 'pd.DataFrame | pl.DataFrame',
        statistics: list[TabularStatistics]
    ) -> str:
        """Format a markdown description of dataset statistics.

        Args:
            stats: A representative TabularStatistics object or None
            dataset: The dataset being analyzed
            statistics: List of all TabularStatistics objects

        Returns:
            Formatted markdown string summarizing dataset statistics
        """
        rows, cols = dataset.shape
        numeric_columns = sum(1 for stat in statistics if stat.mean_val is not None)

        lines = [
            '**Dataset Overview:**',
            f'- Total rows: {rows:,}',
            f'- Total columns: {cols}',
        ]

        lines.extend(['', '**Statistical Summary:**', f'- Columns with numeric summary: {numeric_columns}'])

        if stats is None: # TODO: Use formatting function of class
            lines.append('- No numeric columns detected for automatic summary.')
        else:
            lines.append(f'- Column analysed: `{stats.column_name}`')
            lines.append(f'- Count: {_format_number(stats.count)}')
            lines.append(f'- Mean: {_format_number(stats.mean_val)}')
            lines.append(f'- Standard Deviation: {_format_number(stats.std_val)}')
            lines.append(f'- Minimum: {_format_number(stats.min_val)}')
            lines.append(f'- Maximum: {_format_number(stats.max_val)}')
            lines.append(f'- 25th Percentile: {_format_number(stats.lowest_quantile)}')
            lines.append(f'- Median (50th Percentile): {_format_number(stats.middle_quantile)}')
            lines.append(f'- 75th Percentile: {_format_number(stats.highest_quantile)}')
            lines.append('')
            lines.append(
                '*Detailed statistics for every column are listed below.*'
            )

        return '\n'.join(lines)

    def _format_quality_assessment(self, dataset: 'pd.DataFrame | pl.DataFrame') -> str: # TODO: Use formatting function of class
        """Format a markdown description of dataset quality.

        Args:
            dataset: The dataset being analyzed

        Returns:
            Formatted markdown string summarizing dataset quality
        """
        '''if isinstance(dataset, pl.DataFrame):
            pandas_df = dataset.to_pandas()
        else:
            pandas_df = dataset

        missing_count = int(pandas_df.isna().sum().sum())
        total_cells = int(pandas_df.size) if pandas_df.size else 0
        missing_percentage = (missing_count / total_cells) * 100 if total_cells else 0.0
        complete_rows = int(pandas_df.dropna().shape[0]) if pandas_df.shape[1] else len(pandas_df)

        dtype_counts = {
            str(dtype): int(count)
            for dtype, count in pandas_df.dtypes.astype(str).value_counts().items()
        }

        lines = [
            '**Data Completeness:**',
            f'- Missing values: {missing_count:,} ({missing_percentage:.2f}% of total cells)',
            f'- Complete rows: {complete_rows:,}',
            '',
            '**Data Types Distribution:**'
        ]

        if dtype_counts:
            for dtype, count in dtype_counts.items():
                suffix = 'column' if count == 1 else 'columns'
                lines.append(f'- {dtype}: {count} {suffix}')
        else:
            lines.append('- No columns detected.')

        return '\n'.join(lines)'''
        return 'Automated data quality assessment will be available in a future release.'

    def _fill_automated_placeholders(self, structure: DatasheetStructure) -> None:
        """Fill in placeholder cards for pending automated analyses.

        Args:
            structure: The datasheet structure to enhance
        """
        pending_messages = {
            'Distribution Analysis': 'Automated distribution analysis will be available in a future release.',
            'Missing Data Analysis': 'Automated missing-data diagnostics will be available in a future release.',
            'Correlation Analysis': 'Automated correlation analysis will be available in a future release.',
            'Any other automated insights?': 'Use this space for custom automated insights or notes.',
        }

        for sub_heading, message in pending_messages.items():
            card = structure.find_card(
                section=DatasheetSection.AUTOMATED_ANALYSIS,
                sub_heading=sub_heading
            )
            if card is None:
                continue
            if card.card_type == CardType.AUTOMATED and card.auto_populated:
                continue
            card.card_type = CardType.AUTOMATED
            card.text = message
            card.result_data = []
            card.auto_populated = False

    def _generate_content_key(self, card: DatasheetInformationCard) -> str:
        """Generate a key for manual content lookup.

        Args:
            card: The information card

        Returns:
            Content key string
        """
        if card.sub_heading:
            return f'{card.heading}::{card.sub_heading}'
        return card.heading
