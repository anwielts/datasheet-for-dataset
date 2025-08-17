[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]
[![Build and Publish](https://github.com/anwielts/datasheet-for-dataset/actions/workflows/build_and_publish.yml/badge.svg)](https://github.com/anwielts/datasheet-for-dataset/actions/workflows/build_and_publish.yml) [![Test and Lint](https://github.com/anwielts/datasheet-for-dataset/actions/workflows/test_and_lint.yml/badge.svg)](https://github.com/anwielts/datasheet-for-dataset/actions/workflows/test_and_lint.yml)
# datasheet-for-dataset

Automatically create standardized documentation ("datasheets") for the datasets used in your ML projects.

Status: Early preview (v0.x). The public API is evolving and subject to change.

## Features
- Define and generate dataset datasheets programmatically
- Extensible building blocks for different data domains (images, sound, tabular)
- Pluggable layouts and structures to match your documentation needs
- Python-first: integrate directly into your data/ML workflows

## Installation
Prerequisites: Python 3.10+

Install from PyPI:
```
pip install datasheet-for-dataset
```

Install for development (editable) with optional dev tools:
```
# clone the repository
git clone https://github.com/anwielts/datasheet-for-dataset.git
cd datasheet-for-dataset

# install the package (and dev extras: pytest, ruff)
pip install -e ".[dev]"
```

## Quickstart
Create a datasheet using the high-level API:
```
from dfd import Datasheet

# Initialize a datasheet
sheet = Datasheet()

# Build the datasheet (runs the configured pipeline)
sheet.create_datasheet()

# Persist the datasheet (e.g., as HTML or PDF; implementation WIP)
sheet.store_datasheet()
```

## Using analyses and layouts (preview)
You can leverage predefined analyses for specific data domains and choose a layout style. These building blocks are available today, and the configuration APIs will be expanded in future releases.
```
from dfd import Datasheet
from dfd.dataset import ImageAnalyses, SoundAnalyses, TabularAnalyses
from dfd.datasheet import SafetyEU, BaseLayout, HumanDatasheet, NonHumanDatasheet

image_analyses = ImageAnalyses()
layout = SafetyEU()           # or: BaseLayout()
structure = HumanDatasheet()  # or: NonHumanDatasheet()

sheet = Datasheet()
# Upcoming releases will provide a clear way to attach analyses/layout/structure
# e.g., sheet.configure(analyses=image_analyses, layout=layout, structure=structure)

sheet.create_datasheet()
sheet.store_datasheet()
```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository and create a new branch from main.
2. Set up the project locally (see Installation > development).
3. Ensure code quality and tests pass:
   - Lint/format: `ruff check .` (and optionally `ruff format` if you use Ruff formatting)
   - Tests: `pytest`
4. Open a pull request with a clear description of the change and any relevant context.

Tips:
- Keep PRs focused and small where possible.
- Add or update tests when you introduce behavior changes.
- Follow the existing code style and project conventions.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Links
- Homepage: https://github.com/anwielts/datasheet-for-dataset
- Issue tracker: https://github.com/anwielts/datasheet-for-dataset/issues

## Contact
- Maintainers: 
  - anwielts — 52626848+anwielts@users.noreply.github.com
  - Flippchen — 91947480+flippchen@users.noreply.github.com

For questions, ideas, or issues, please open a GitHub issue; for sensitive security concerns, consider contacting the maintainers by email.


[contributors-shield]: https://img.shields.io/github/contributors/anwielts/datasheet-for-dataset.svg?style=for-the-badge
[contributors-url]: https://github.com/anwielts/datasheet-for-dataset/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/anwielts/datasheet-for-dataset.svg?style=for-the-badge
[forks-url]: https://github.com/anwielts/datasheet-for-dataset/network/members
[stars-shield]: https://img.shields.io/github/stars/anwielts/datasheet-for-dataset.svg?style=for-the-badge
[stars-url]: https://github.com/anwielts/datasheet-for-dataset/stargazers
[issues-shield]: https://img.shields.io/github/issues/anwielts/datasheet-for-dataset.svg?style=for-the-badge
[issues-url]: https://github.com/anwielts/datasheet-for-dataset/issues
[license-shield]: https://img.shields.io/github/license/anwielts/datasheet-for-dataset.svg?style=for-the-badge
[license-url]: https://github.com/anwielts/datasheet-for-dataset/blob/main/LICENSE
