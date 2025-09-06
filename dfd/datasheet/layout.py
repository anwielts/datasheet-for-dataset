"""Definitions of how the datasheet should look like"""
from pydantic import BaseModel


class Section(BaseModel):
    heading: str


def _check_for_required_sections(sections: list[Section], required_sections: list[str]):
    """
    Validates that all required sections are present in the provided sections list.

    Args:
        sections (list[Section]): A list of Section objects containing headings to validate.
        required_sections (list[str]): A list of required headings for the basic datasheet layout.

    Raises:
        ValueError: If any required section is missing from the sections list.
    """
    section_headings = [section.heading.lower() for section in sections]
    missing_sections = [req for req in required_sections if req.lower() not in section_headings]
    
    if missing_sections:
        required_heading_error = (
            f'Missing required sections: {missing_sections}. '
            f'Required sections are: {required_sections}'
        )
        raise ValueError(required_heading_error)


class BaseLayout:
    """Base layout class as described in the paper "Datasheets for Datasets", https://arxiv.org/pdf/1803.09010.

    This class is responsible for managing and validating the layout of a datasheet based on predefined sections.

    Attributes:
        sections (list[Section]): A list of Section objects representing different parts of the datasheet.
        required_sections (list[str] | None): A list of section names that are considered mandatory. Defaults to common mandatory sections such as motivation, composition, collection process, processing steps, uses, distribution, and maintenance.

    Methods:
        __init__(self, sections: list[Section], required_sections: list[str] | None = None):
            Initializes the BaseLayout object with a list of sections and optional required sections.
    """
    # Layout as describe in the paper "Datasheets for Datasets", https://arxiv.org/pdf/1803.09010
    def __init__(self,
                 sections: list[Section],
                 required_sections: list[str] | None = None):
        self.sections = sections
        if required_sections is None:
            required_sections = ['motivation',
                                  'composition',
                                  'collection_process',
                                  'preprocessing',
                                  'uses',
                                  'distribution',
                                  'maintenance']
        self.required_sections = required_sections
        _check_for_required_sections(self.sections, self.required_sections)


class SafetyEU:
    """Define the layout in such a way that is resembles the material
    security datasheet for materials and chemicals needed in the EU
    """
    def __init__(self):
        pass
