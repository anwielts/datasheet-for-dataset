"""Defines datasheet structures"""
from pydantic import BaseModel


class Section(BaseModel):
    heading: str
    qa_pair: list[tuple[str, str]]


class BaseDatasheet:
    def __init__(self, motivation: Section, 
                 composition: Section, 
                 collection_process: Section, 
                 processing_steps: Section, 
                 uses: Section, 
                 distribution: Section, 
                 maintenance: Section):
        self.motivation = motivation
        self.composition = composition
        self.collection_process = collection_process
        self.processing_steps = processing_steps
        self.uses = uses
        self.distribution = distribution
        self.maintenance = maintenance
        # Define base structure content such as
        # chapters
        # basic infos such as contact persons, org, ...


class HumanDatasheet:
    def __init__(self):
        pass
        # Define structure for a datasheet including human data
        # Include sections/questions about ethics and harmful content and so on


class NonHumanDatasheet:
    def __init__(self):
        pass
        # Define structure for a datasheet including non-human data
        # Exclude sections/questions about ethics and harmful content and so on
        # Include stuff which is important for stuff like sensor data and so on
