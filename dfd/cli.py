"""Command-line interface for datasheet generation."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich import print
from rich.panel import Panel

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
        print(f"[bold red]❌ Failed to generate template:[/bold red] {exc}")
        raise typer.Exit(code=1)

    print("[bold green]✅ Template generated[/bold green]")
    print(f"📄 Saved to: [bold blue]{output_file}[/bold blue]")
    
    print(Panel.fit(
        "  - Fill in the template with dataset context\n"
        "  - Run [bold cyan]dfd build --data <file> --template <filled_template>[/bold cyan] to merge analysis",
        title="Next steps",
        border_style="green"
    ))


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
        print(f"[bold red]❌ Failed to build datasheet:[/bold red] {exc}")
        raise typer.Exit(code=1)

    print("[bold green]✅ Datasheet created[/bold green]")
    print(f"📄 Saved to: [bold blue]{Path(result).absolute()}[/bold blue]")
    if not template:
        print("[yellow]ℹ️ Generated using automated analysis only (no manual template provided).[/yellow]")


def typer_main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    typer_main()

