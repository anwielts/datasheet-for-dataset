"""Command-line interface for datasheet generation."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from dfd.create import Datasheet
from dfd._common import DatasetBackend

app = typer.Typer(
    help="Generate datasheets for tabular datasets.",
    rich_markup_mode="markdown",
)


@app.command()
def template(
    output: Annotated[
        str,
        typer.Option(
            "--output", "-o",
            help="Output path for the template file"
        )
    ] = "datasheet_template.md",
):
    """Generate an empty datasheet template."""
    try:
        output_file = Datasheet.generate_template(output)
    except (OSError, ValueError) as exc:
        print(f"❌ Failed to generate template: {exc}")
        raise typer.Exit(code=1)

    print("✅ Template generated")
    print(f"📄 Saved to: {output_file}")
    print("\nNext steps:")
    print("  - Fill in the template with dataset context")
    print("  - Run `dfd build --data <file> --template <filled_template>` to merge analysis")


@app.command()
def build(
    data: Annotated[
        str,
        typer.Option(
            "--data", "-d",
            help="Path to the dataset (CSV/TSV/Parquet/JSON)"
        )
    ],
    template: Annotated[
        str | None,
        typer.Option(
            "--template", "-t",
            help="Path to a filled template markdown file"
        )
    ] = None,
    output: Annotated[
        str,
        typer.Option(
            "--output", "-o",
            help="Output path for the compiled datasheet"
        )
    ] = "complete_datasheet.md",
    name: Annotated[
        str | None,
        typer.Option(
            "--name", "-n",
            help="Dataset name to show in the datasheet heading"
        )
    ] = None,
    version: Annotated[
        str,
        typer.Option(
            "--version", "-v",
            help="Datasheet version string"
        )
    ] = "1.0",
    backend: Annotated[
        DatasetBackend,
        typer.Option(
            "--backend",
            help="Dataframe backend used for loading and analysing the dataset",
            case_sensitive=False,
        )
    ] = "auto",
):
    """Compile a datasheet for a tabular dataset."""
    # Convert string backend to enum if needed, though Typer handles Enums well if hinted correctly.
    # DatasetBackend is likely a StrEnum or similar based on usage.
    
    try:
        datasheet = Datasheet.from_path(
            data,
            backend=backend,
            dataset_name=name,
            analysis=backend,
        )
        result = datasheet.to_markdown(
            output_path=output,
            template_path=template,
            version=version,
        )
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"❌ Failed to build datasheet: {exc}")
        raise typer.Exit(code=1)

    print("✅ Datasheet created")
    print(f"📄 Saved to: {Path(result).absolute()}")
    if not template:
        print("ℹ️ Generated using automated analysis only (no manual template provided).")


def typer_main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    typer_main()

