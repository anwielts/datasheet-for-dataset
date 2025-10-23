[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]
[![Build and Publish](https://github.com/anwielts/datasheet-for-dataset/actions/workflows/build_and_publish.yml/badge.svg)](https://github.com/anwielts/datasheet-for-dataset/actions/workflows/build_and_publish.yml) [![Test and Lint](https://github.com/anwielts/datasheet-for-dataset/actions/workflows/test_and_lint.yml/badge.svg)](https://github.com/anwielts/datasheet-for-dataset/actions/workflows/test_and_lint.yml)
# datasheet-for-dataset

Automatically create standardized documentation ("datasheets") for the datasets used in your ML projects.

Status: Early preview (v0.x). The public API is evolving and subject to change.

## Features
- Focused support for tabular datasets with pandas and polars backends
- Automatic summary statistics and data quality diagnostics
- Markdown templates that combine manual answers with automated insights
- CLI and Python APIs for integrating datasheet generation into workflows

## Installation
Prerequisites: Python 3.10+

Install from PyPI:
```
pip install datasheet-for-dataset
```

### Install a suitable backend
To use this library correctly, install a supported backend. Currently available backends are `polars` (default) and `pandas`.

Install for development (editable) with optional dev tools:
```
# clone the repository
git clone https://github.com/anwielts/datasheet-for-dataset.git
cd datasheet-for-dataset

# install the package (and dev extras: pytest, ruff)
uv pip install -e ".[dev]"
```

## Quickstart

### CLI workflow
Generate a template, fill in the manual sections, and compile the final markdown datasheet:

```bash
# create an empty questionnaire
dfd template --output docs/datasheet_template.md

# after answering the questions in docs/datasheet_template.md, combine it with a dataset
dfd build \
  --data data/customers.csv \
  --template docs/datasheet_template.md \
  --output docs/datasheet.md \
  --name "Customer Churn" \
  --backend auto
```

### Python workflow
Use the programmatic API to analyse a dataframe or to build a datasheet directly from a dataset file:

```python
import pandas as pd

from dfd import Datasheet

df = pd.read_csv("data/customers.csv")

# access automated statistics in-memory
sheet = Datasheet(data=df)
for stat in sheet.analyse():
    print(stat.column_name, stat.mean_val)

# generate a template and export a full datasheet
Datasheet.generate_template("docs/datasheet_template.md")
compiled = Datasheet.from_path(
    "data/customers.csv",
    backend="auto",
    dataset_name="Customer Churn",
)
compiled.to_markdown(
    output_path="docs/auto_datasheet.md",
    template_path=None,
    version="1.0",
)
```

## Development
After setting up the project for development (see Installation), you can use the following commands:

### Install uv with:
```bash
pip install uv
```
### Lock dependencies / sync project
```bash
uv lock
uv sync
uv sync --extra dev
```

### Building the package
```bash
uv build
```

### Running Tests
```bash
# Run tests using hatch
uv run pytest
```

### Code Quality with Ruff
```bash
# Check for linting issues
uv run ruff check .

# Auto-fix linting issues where possible
uv run ruff check . --fix

# Format code (optional)
uv run ruff format .
```

## Links
- Homepage: https://github.com/anwielts/datasheet-for-dataset
- Issue tracker: https://github.com/anwielts/datasheet-for-dataset/issues
- Documentation: https://github.com/anwielts/datasheet-for-dataset/wiki

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
[issues-shield]: https://img.shields.io/github/issues/anwielts/datasheet-for-dataset.svg?style=for-the-badge
[issues-url]: https://github.com/anwielts/datasheet-for-dataset/issues
[license-shield]: https://img.shields.io/github/license/anwielts/datasheet-for-dataset.svg?style=for-the-badge
[license-url]: https://github.com/anwielts/datasheet-for-dataset/blob/main/LICENSE
