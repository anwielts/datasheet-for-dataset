"""Definitions of how the datasheet should look like"""
from typing import List, Optional

from dfd.datasheet.structures import DatasheetSection


def _check_for_required_sections(sections: List[DatasheetSection], required_sections: List[DatasheetSection]):
    """
    Validates that all required sections are present in the provided sections list.

    Args:
        sections (List[DatasheetSection]): A list of DatasheetSection objects containing sections to validate.
        required_sections (List[DatasheetSection]): A list of required sections for the basic datasheet layout.

    Raises:
        ValueError: If any required section is missing from the sections list.
    """
    missing_sections = [req for req in required_sections if req not in sections]
    
    if missing_sections:
        missing_names = [section.value for section in missing_sections]
        required_names = [section.value for section in required_sections]
        required_heading_error = (
            f'Missing required sections: {missing_names}. '
            f'Required sections are: {required_names}'
        )
        raise ValueError(required_heading_error)


class BaseLayout:
    """Base layout class as described in the paper "Datasheets for Datasets", https://arxiv.org/pdf/1803.09010.

    This class is responsible for managing and validating the layout of a datasheet based on predefined sections.

    Attributes:
        sections (List[DatasheetSection]): A list of DatasheetSection objects representing different parts of the datasheet.
        required_sections (List[DatasheetSection]): A list of sections that are considered mandatory.
        section_order (List[DatasheetSection]): The order in which sections should appear.

    Methods:
        __init__(self, sections: List[DatasheetSection], required_sections: Optional[List[DatasheetSection]] = None):
            Initializes the BaseLayout object with a list of sections and optional required sections.
    """
    # Layout as describe in the paper "Datasheets for Datasets", https://arxiv.org/pdf/1803.09010
    # Default section order based on the paper
    DEFAULT_SECTION_ORDER = [
        DatasheetSection.MOTIVATION,
        DatasheetSection.COMPOSITION,
        DatasheetSection.COLLECTION_PROCESS,
        DatasheetSection.PREPROCESSING,
        DatasheetSection.USES,
        DatasheetSection.DISTRIBUTION,
        DatasheetSection.MAINTENANCE,
        DatasheetSection.AUTOMATED_ANALYSIS
    ]
    
    def __init__(self,
                 sections: Optional[List[DatasheetSection]] = None,
                 required_sections: Optional[List[DatasheetSection]] = None,
                 section_order: Optional[List[DatasheetSection]] = None):
        
        if required_sections is None:
            required_sections = [
                DatasheetSection.MOTIVATION,
                DatasheetSection.COMPOSITION,
                DatasheetSection.COLLECTION_PROCESS,
                DatasheetSection.PREPROCESSING,
                DatasheetSection.USES,
                DatasheetSection.DISTRIBUTION,
                DatasheetSection.MAINTENANCE
            ]
        if sections is None:
            sections = required_sections
        self.sections = sections
        self.required_sections = required_sections
        self.section_order = section_order or self.DEFAULT_SECTION_ORDER
        _check_for_required_sections(self.sections, self.required_sections)
    
    def get_ordered_sections(self) -> List[DatasheetSection]:
        """Get sections in the defined order.
        
        Returns:
            List[DatasheetSection]: Sections in the correct order.
        """
        return self.section_order
    
    def get_section_by_type(self, section_type: DatasheetSection) -> Optional[DatasheetSection]:
        """Get a section by its type.
        
        Args:
            section_type: The section type to find.
            
        Returns:
            Optional[DatasheetSection]: The section if found, None otherwise.
        """
        for section in self.sections:
            if section == section_type:
                return section
        return None


class SafetyEU:
    """Define the layout in such a way that is resembles the material
    security datasheet for materials and chemicals needed in the EU
    """
    def __init__(self):
        pass
