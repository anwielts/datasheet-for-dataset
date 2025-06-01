"""Defines datasheet structures"""


class BaseDatasheet:
    def __init__(self):
        pass
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
