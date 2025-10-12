"""Command-line interface for datasheet generation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dfd.api import DatasetBackend, build_datasheet, generate_template


def _build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description='Generate datasheets for tabular datasets.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Examples:\n'
            '  dfd template --output docs/datasheet_template.md\n'
            '  dfd build --data data/customers.csv --template filled_template.md --output docs/datasheet.md\n'
            '  dfd build --data data/customers.csv --output docs/auto_datasheet.md --backend polars'
        )
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    template_parser = subparsers.add_parser('template', help='Generate an empty datasheet template')
    template_parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output path for the template file (default: datasheet_template.md)'
    )

    build_parser = subparsers.add_parser('build', help='Compile a datasheet for a tabular dataset')
    build_parser.add_argument('--data', '-d', required=True, help='Path to the dataset (CSV/TSV/Parquet/JSON)')
    build_parser.add_argument('--template', '-t', help='Path to a filled template markdown file')
    build_parser.add_argument('--output', '-o', default='complete_datasheet.md', help='Output path for the compiled datasheet')
    build_parser.add_argument('--name', '-n', help='Dataset name to show in the datasheet heading')
    build_parser.add_argument('--version', '-v', default='1.0', help='Datasheet version string')
    build_parser.add_argument(
        '--backend',
        choices=['auto', 'pandas', 'polars'],
        default='auto',
        help='Dataframe backend used for loading and analysing the dataset'
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI.

    Args:
        argv: List of command-line arguments. If None, uses sys.argv.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == 'template':
        try:
            output_file = generate_template(args.output)
        except (OSError, ValueError) as exc:
            print(f'❌ Failed to generate template: {exc}')
            return 1

        print('✅ Template generated')
        print(f'📄 Saved to: {output_file}')
        print('\nNext steps:')
        print('  - Fill in the template with dataset context')
        print('  - Run `dfd build --data <file> --template <filled_template>` to merge analysis')
        return 0

    if args.command == 'build':
        backend: DatasetBackend = args.backend
        try:
            result = build_datasheet(
                dataset_path=args.data,
                output_path=args.output,
                template_path=args.template,
                dataset_name=args.name,
                version=args.version,
                backend=backend
            )
        except (FileNotFoundError, ValueError, RuntimeError) as exc:
            print(f'❌ Failed to build datasheet: {exc}')
            return 1

        print('✅ Datasheet created')
        print(f'📄 Saved to: {Path(result).absolute()}')
        if not args.template:
            print('ℹ️ Generated using automated analysis only (no manual template provided).') # noqa: RUF001
        return 0

    parser.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main())
