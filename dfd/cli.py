"""Command-line interface for datasheet generation tool."""
import argparse
from pathlib import Path

from dfd.datasheet.compiler import DatasheetCompiler
from dfd.datasheet.manager import TemplateManager


def generate_template(output_path: str | None = None) -> str:
    """Generate an empty datasheet questionnaire template.
    
    Args:
        output_path: Optional path where to save the template. If None, saves to current directory.
        
    Returns:
        str: Path to the generated template file.
    """
    manager = TemplateManager()

    if output_path is None:
        output_path = 'datasheet_template.md'

    # Ensure the output directory exists
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Generate and save the template
    manager.generate_empty_template(str(output_file))

    return str(output_file.absolute())


def create_datasheet_from_template(template_path: str, data_path: str, output_path: str | None = None) -> str:
    """Create a complete datasheet from a filled template and dataset.
    
    Args:
        template_path: Path to the filled template file.
        data_path: Path to the dataset file (CSV, JSON, etc.).
        output_path: Optional path where to save the complete datasheet.
        
    Returns:
        str: Path to the generated datasheet file.
    """
    import pandas as pd

    try:
        # Load dataset
        if data_path.endswith('.csv'):
            dataset = pd.read_csv(data_path)
        elif data_path.endswith('.parquet'):
            dataset = pd.read_parquet(data_path)
        else:
            raise ValueError(f'Unsupported file format: {data_path}')

        # Set default output path if not provided
        if output_path is None:
            output_path = 'complete_datasheet.md'

        # Create compiler and compile datasheet
        compiler = DatasheetCompiler()
        result_path = compiler.compile_from_template(
            template_path=template_path,
            dataset=dataset,
            output_path=output_path
        )

        return str(Path(result_path).absolute())

    except Exception as e:
        raise RuntimeError(f'Error creating datasheet: {e}')


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Datasheet for Dataset - Semi-automatic datasheet generation tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generate an empty template
  dfd generate-template
  
  # Generate template to specific location
  dfd generate-template --output /path/to/my_template.md
  
  # Create datasheet from filled template and dataset (coming soon)
  dfd create-datasheet --template filled_template.md --data dataset.csv
'''
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Generate template command
    template_parser = subparsers.add_parser(
        'generate-template',
        help='Generate an empty datasheet questionnaire template'
    )
    template_parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output path for the template file (default: datasheet_template.md)'
    )

    # Create datasheet command (placeholder for future implementation)
    create_parser = subparsers.add_parser(
        'create-datasheet',
        help='Create a complete datasheet from template and dataset'
    )
    create_parser.add_argument(
        '--template', '-t',
        type=str,
        required=True,
        help='Path to the filled template file'
    )
    create_parser.add_argument(
        '--data', '-d',
        type=str,
        required=True,
        help='Path to the dataset file'
    )
    create_parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output path for the complete datasheet'
    )

    args = parser.parse_args()

    if args.command == 'generate-template':
        try:
            output_file = generate_template(args.output)
            print('✅ Empty datasheet template generated successfully!')
            print(f'📄 Template saved to: {output_file}')
            print('\n📝 Next steps:')
            print('   1. Open the template file and fill in the documentation sections')
            print("   2. Use 'dfd create-datasheet' to combine with your dataset (coming soon)")
        except Exception as e:
            print(f'❌ Error generating template: {e}')
            return 1

    elif args.command == 'create-datasheet':
        try:
            output_file = create_datasheet_from_template(
                args.template,
                args.data,
                args.output
            )
            print('✅ Complete datasheet generated successfully!')
            print(f'📄 Datasheet saved to: {output_file}')
        except NotImplementedError as e:
            print(f'🚧 {e}')
            return 1
        except Exception as e:
            print(f'❌ Error creating datasheet: {e}')
            return 1

    else:
        parser.print_help()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
