# datasheet-for-dataset
Automatically create standardized documentation for the dataset used in your ML project

## Getting started

### Quickstart

After installation you can use the lib out of the box in this way:
```
from dfd import Datasheet

# configure the datasheet you want to have
datasheet = Datasheet(...=...)

# create the datasheet
datasheet.create_datasheet()

# store it how you like it
datasheet.store_datasheet()
```

Additionally you can use the lib to leverage specific analyses and/or layouts (here analysis on a image dataset and using the EU safety datasheet layout):
```
from dfd import Datasheet
from dfd.dataset import ImageAnalyses
from dfd.datasheet import SafetyEU

image_analyses = ImageAnalyses(...=...)
safety_eu_layout = SafetyEU(...=...)

# configure the datasheet you want to have
datasheet = Datasheet(...=..., image_analyses, safety_eu_layout)

# create the datasheet
datasheet.create_datasheet()

# store it how you like it
datasheet.store_datasheet()
```
