from pathlib import Path

import pandas as pd

from dfd import Datasheet, build_datasheet, generate_template


def analyze_dataframe_in_python() -> None:
    df = pd.DataFrame(
        {
            'customer_id': [1, 2, 3, 4],
            'monthly_spend': [99.5, 120.0, 75.25, 88.0],
            'segment': ['startup', 'enterprise', 'startup', 'smb'],
        }
    )

    sheet = Datasheet(data=df)
    sheet.create_datasheet()

    for stat in sheet.data_statistics:
        print(f'{stat.column_name}: mean={stat.mean_val}, std={stat.std_val}')


def build_markdown_datasheet() -> None:
    data_dir = Path('examples/data')
    data_dir.mkdir(parents=True, exist_ok=True)
    dataset_path = data_dir / 'customers.csv'

    df = pd.DataFrame(
        {
            'customer_id': range(1, 6),
            'monthly_spend': [120.0, 99.5, 87.0, 130.25, 110.75],
            'segment': ['enterprise', 'startup', 'smb', 'enterprise', 'startup'],
        }
    )
    df.to_csv(dataset_path, index=False)

    template_path = generate_template('examples/data/datasheet_template.md')
    output_path = build_datasheet(
        dataset_path=str(dataset_path),
        output_path='examples/data/datasheet.md',
        template_path=None,
        dataset_name='Sample Customers',
    )

    print(f'Template saved to {template_path}')
    print(f'Compiled datasheet saved to {output_path}')


if __name__ == '__main__':
    analyze_dataframe_in_python()
    build_markdown_datasheet()
