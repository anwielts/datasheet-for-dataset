"""Definitions of how the datasheet should look like"""
from pydantic import BaseModel


class Section(BaseModel):
    heading: str


def _check_for_required_sections(sections: list[Section], required_sections: list[str]):
    for section in sections:
        if section.heading.lower() not in required_sections:
            raise ValueError(f"Provided section/heading {section.heading} which is not in the" 
                                f"required {required_sections} sections/headings for the basic datasheet for dataset layout.")


class BaseLayout:
    """Layout as describe in the paper "Datasheets for Datasets", https://arxiv.org/pdf/1803.09010"""
    def __init__(self,
                 sections: list[Section],
                 required_sections=["motivation",
                                    "composition", 
                                    "collection_process", 
                                    "processing_steps", 
                                    "uses", 
                                    "distribution", 
                                    "maintenance"]):
        self.sections = sections
        self.required_sections = required_sections
        _check_for_required_sections(self.sections, self.required_sections)


class SafetyEU:
    """Define the layout in such a way that is resembles the material 
    security datasheet for materials and chemicals needed in the EU"""
    def __init__(self):
        pass
