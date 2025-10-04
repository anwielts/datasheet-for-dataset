"""Template management system for datasheet generation."""

from pathlib import Path

from .structures import CardType, DatasheetInformationCard, DatasheetSection, DatasheetStructure
from .template import DatasheetTemplate


class TemplateManager:
    """Manages datasheet templates and their conversion to structured cards."""

    def __init__(self):
        self.template = DatasheetTemplate()
        self._cached_structure: DatasheetStructure | None = None

    def generate_empty_template(self, output_path: str | None = None) -> str:
        """Generate an empty markdown template.

        Args:
            output_path: Optional path to save the template file

        Returns:
            The markdown template content
        """
        template_content = self.template.generate_empty_template()

        if output_path:
            Path(output_path).write_text(template_content, encoding='utf-8')

        return template_content

    def create_datasheet_structure(self) -> DatasheetStructure:
        """Create a DatasheetStructure with empty cards for all template sections.

        Returns:
            A DatasheetStructure containing cards for all template sections
        """
        if self._cached_structure is not None:
            return self._cached_structure.model_copy(deep=True)

        structure = DatasheetStructure(
            title='Dataset Datasheet',
            version='1.0',
            date_created='TBD'
        )

        # Get section names from the template
        section_names = self.template.get_section_names()

        for section_name in section_names:
            # Map section names to enum values
            section_enum = self._map_section_name(section_name)

            # Get subsections for this section
            subsection_names = self.template.get_subsection_names(section_name)

            if subsection_names:
                # Handle subsections
                for subsection_name in subsection_names:
                    card = DatasheetInformationCard.create_from_template(
                        section=section_enum,
                        heading=section_name,
                        sub_heading=subsection_name,
                        questions=[]  # Questions will be extracted from template content
                    )
                    if section_enum == DatasheetSection.AUTOMATED_ANALYSIS:
                        card.card_type = CardType.AUTOMATED
                        card.auto_populated = False
                        card.text = '[This section will be automatically populated by the compiler]'
                    structure.add_card(card)
            else:
                # Handle section without subsections
                card = DatasheetInformationCard.create_from_template(
                    section=section_enum,
                    heading=section_name,
                    sub_heading=None,
                    questions=[]
                )
                if section_enum == DatasheetSection.AUTOMATED_ANALYSIS:
                    card.card_type = CardType.AUTOMATED
                    card.auto_populated = False
                    card.text = '[This section will be automatically populated by the compiler]'
                structure.add_card(card)

        self._cached_structure = structure
        return structure.model_copy(deep=True)

    def load_filled_template(self, template_path: str) -> DatasheetStructure:
        """Load a filled template from a markdown file.

        Args:
            template_path: Path to the filled markdown template

        Returns:
            A DatasheetStructure with populated content
        """
        # Start with the base structure
        structure = self.create_datasheet_structure()

        # Parse the filled template
        content = Path(template_path).read_text(encoding='utf-8')
        filled_data = self._parse_filled_template(content)

        # Update cards with filled content
        for card in structure.cards:
            key = self._generate_card_key(card)
            if key in filled_data:
                card.text = filled_data[key]

        return structure

    def save_structure_as_template(self, structure: DatasheetStructure, output_path: str) -> None:
        """Save a DatasheetStructure as a markdown template.

        Args:
            structure: The datasheet structure to save
            output_path: Path where to save the template
        """
        markdown_content = structure.to_markdown()
        Path(output_path).write_text(markdown_content, encoding='utf-8')

    def get_section_names(self) -> list[str]:
        """Get all available section names.

        Returns:
            List of section names
        """
        return self.template.get_section_names()

    def get_subsection_names(self, section: str) -> list[str]:
        """Get subsection names for a given section.

        Args:
            section: The section name

        Returns:
            List of subsection names
        """
        return self.template.get_subsection_names(section)

    def _map_section_name(self, section_name: str) -> DatasheetSection:
        """Map section name to DatasheetSection enum.

        Args:
            section_name: The section name from template

        Returns:
            Corresponding DatasheetSection enum value
        """
        try:
            return DatasheetSection(section_name)
        except ValueError as exc:
            msg = f'Unknown section name: {section_name}'
            raise ValueError(msg) from exc

    def _parse_filled_template(self, content: str) -> dict[str, str]:
        """Parse a filled markdown template to extract answers.

        Args:
            content: The markdown content

        Returns:
            Dictionary mapping card keys to their filled content
        """
        filled_data = {}
        lines = content.split('\n')
        current_section = None
        current_subsection = None
        current_content = []

        for line in lines:
            line_stripped = line.strip()

            if line_stripped.startswith('## '):
                # Save previous content
                if current_section:
                    key = self._generate_key(current_section, current_subsection)
                    filled_data[key] = '\n'.join(current_content).strip()

                # Start new section
                current_section = line_stripped[3:].strip().lower().replace(' ', '_')
                current_subsection = None
                current_content = []

            elif line_stripped.startswith('### '):
                # Save previous subsection content
                if current_section and current_subsection:
                    key = self._generate_key(current_section, current_subsection)
                    filled_data[key] = '\n'.join(current_content).strip()

                # Start new subsection
                current_subsection = line_stripped[4:].strip()
                current_content = []

            elif line_stripped and not line_stripped.startswith('#'):
                if line_stripped == '---':
                    continue
                # Add content line
                current_content.append(line_stripped)

        # Save final content
        if current_section:
            key = self._generate_key(current_section, current_subsection)
            filled_data[key] = '\n'.join(current_content).strip()

        return filled_data

    def _generate_card_key(self, card: DatasheetInformationCard) -> str:
        """Generate a key for a card based on its section and subsection.

        Args:
            card: The datasheet information card

        Returns:
            A unique key for the card
        """
        return self._generate_key(card.heading, card.sub_heading)

    def _generate_key(self, section: str, subsection: str | None) -> str:
        """Generate a key from section and subsection names.

        Args:
            section: The section name
            subsection: The subsection name (optional)

        Returns:
            A unique key
        """
        if subsection:
            return f'{section}::{subsection}'
        return section
