"""Datasheet compilation system for combining manual and automated content."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from dfd.dataset.analyses import TabularDataContext, TabularStatistics

from .manager import TemplateManager
from .structures import CardType, DatasheetInformationCard, DatasheetSection, DatasheetStructure

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl


class DatasheetCompiler:
    """Compiles complete datasheets by combining manual content with automated analysis."""

    def __init__(self) -> None:
        self.template_manager = TemplateManager()

    def compile(  # noqa: PLR0913
        self,
        *,
        dataset: 'pd.DataFrame | pl.DataFrame',
        statistics: list[TabularStatistics],
        output_path: str,
        dataset_name: str,
        version: str = '1.0',
        template_path: str | None = None,
        manual_content: dict[str, str] | None = None,
    ) -> str:
        """Compile a datasheet and write it to disk."""
        if template_path:
            structure = self.template_manager.load_filled_template(template_path)
        else:
            structure = self.template_manager.create_datasheet_structure()
            if manual_content:
                for card in structure.cards:
                    key = self._generate_content_key(card)
                    if key in manual_content:
                        card.text = manual_content[key]

        structure.title = f'Datasheet for {dataset_name}'
        structure.version = version
        structure.date_created = datetime.now(timezone.utc).strftime('%Y-%m-%d')

        self._add_automated_analysis(structure, dataset, statistics)

        self.template_manager.save_structure_as_template(structure, output_path)
        return output_path

    def compile_from_template(
        self,
        template_path: str,
        dataset: 'pd.DataFrame | pl.DataFrame',
        output_path: str,
        dataset_name: str | None = None,
        version: str = '1.0',
        statistics: list[TabularStatistics] | None = None,
    ) -> str:
        """Compile a complete datasheet from a filled template and dataset."""
        stats = statistics or self._calculate_statistics(dataset)
        name = dataset_name or 'Dataset'
        return self.compile(
            dataset=dataset,
            statistics=stats,
            output_path=output_path,
            dataset_name=name,
            version=version,
            template_path=template_path,
        )

    def compile_from_scratch(
        self,
        dataset: 'pd.DataFrame | pl.DataFrame',
        output_path: str,
        dataset_name: str,
        manual_content: dict[str, str] | None = None,
        version: str = '1.0',
        statistics: list[TabularStatistics] | None = None,
    ) -> str:
        """Compile a datasheet from scratch with minimal manual input."""
        stats = statistics or self._calculate_statistics(dataset)
        return self.compile(
            dataset=dataset,
            statistics=stats,
            output_path=output_path,
            dataset_name=dataset_name,
            version=version,
            manual_content=manual_content,
        )

    def _calculate_statistics(
        self,
        dataset: 'pd.DataFrame | pl.DataFrame',
    ) -> list[TabularStatistics]:
        """Calculate statistics using the default tabular context."""
        analysis_context = TabularDataContext(strategy='auto')
        return analysis_context.calculate_tabular_statistics(dataset)

    def _add_automated_analysis(
        self,
        structure: DatasheetStructure,
        dataset: 'pd.DataFrame | pl.DataFrame',
        statistics: list[TabularStatistics],
    ) -> None:
        """Add automated analysis cards to the datasheet structure."""
        summary_stat = self._select_summary_stat(statistics)
        stats_description = self._format_statistics_description(summary_stat, dataset, statistics)
        stats_card = structure.find_card(
            section=DatasheetSection.AUTOMATED_ANALYSIS,
            sub_heading='Dataset Statistics',
        )

        if stats_card and (summary_stat or statistics):
            stats_card.populate_automated(stats_description, statistics)
            if summary_stat:
                stats_card.metadata['summary_column'] = summary_stat.column_name
        elif statistics:
            fallback = DatasheetInformationCard.create_automated(
                section=DatasheetSection.AUTOMATED_ANALYSIS,
                heading='Dataset Statistics',
                description=stats_description,
                result_data=statistics,
            )
            structure.add_card(fallback)

        quality_description = self._format_quality_assessment(dataset)
        quality_card = structure.find_card(
            section=DatasheetSection.AUTOMATED_ANALYSIS,
            sub_heading='Data Quality Assessment',
        )
        if quality_card:
            quality_card.populate_automated(quality_description, [])
        else:
            quality = DatasheetInformationCard.create_automated(
                section=DatasheetSection.AUTOMATED_ANALYSIS,
                heading='Data Quality Assessment',
                description=quality_description,
                result_data=[],
            )
            structure.add_card(quality)

        self._fill_automated_placeholders(structure)

    @staticmethod
    def _select_summary_stat(
        statistics: list[TabularStatistics],
    ) -> TabularStatistics | None:
        """Select a representative statistical summary from the list."""
        for stat in statistics:
            if stat.mean_val is not None or stat.std_val is not None:
                return stat
        return statistics[0] if statistics else None

    def _format_statistics_description(
        self,
        stats: TabularStatistics | None,
        dataset: 'pd.DataFrame | pl.DataFrame',
        statistics: list[TabularStatistics],
    ) -> str:
        """Format a markdown description of dataset statistics."""
        rows, cols = dataset.shape
        numeric_columns = sum(1 for stat in statistics if stat.mean_val is not None)

        lines = [
            '**Dataset Overview:**',
            f'- Total rows: {rows:,}',
            f'- Total columns: {cols}',
            '',
            '**Statistical Summary:**',
            f'- Columns with numeric summary: {numeric_columns}',
        ]

        if stats is None:
            lines.append('- No numeric columns detected for automatic summary.')
        else:
            lines.extend(['', stats.markdown])

        lines.append('')
        lines.append('*Detailed statistics for every column are listed below.*')

        return '\n'.join(lines).strip()

    @staticmethod
    def _format_quality_assessment(
        dataset: 'pd.DataFrame | pl.DataFrame',
    ) -> str:
        """Format a markdown description of dataset quality."""
        rows, cols = dataset.shape
        return (
            'Automated data quality assessment will be available in a future release.\n'
            f'Current dataset shape: {rows:,} rows x {cols} columns.'
        )

    def _fill_automated_placeholders(self, structure: DatasheetStructure) -> None:
        """Fill in placeholder cards for pending automated analyses."""
        pending_messages = {
            'Distribution Analysis': 'Automated distribution analysis will be available in a future release.',
            'Missing Data Analysis': 'Automated missing-data diagnostics will be available in a future release.',
            'Correlation Analysis': 'Automated correlation analysis will be available in a future release.',
            'Any other automated insights?': 'Use this space for custom automated insights or notes.',
        }

        for sub_heading, message in pending_messages.items():
            card = structure.find_card(
                section=DatasheetSection.AUTOMATED_ANALYSIS,
                sub_heading=sub_heading,
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
        """Generate a key for manual content lookup."""
        if card.sub_heading:
            return f'{card.heading}::{card.sub_heading}'
        return card.heading
