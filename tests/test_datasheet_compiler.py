from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from dfd.datasheet.compiler import DatasheetCompiler
from dfd.datasheet.manager import TemplateManager


def test_compiler_populates_automated_sections():
    df = pd.DataFrame({'value': [1, 2, 3], 'category': ['a', 'b', 'c']})

    manager = TemplateManager()
    structure = manager.create_datasheet_structure()
    structure.cards[0].text = 'Motivation answer'

    with TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        template_file = tmp_path / 'filled_template.md'
        output_file = tmp_path / 'compiled.md'

        manager.save_structure_as_template(structure, template_file)

        compiler = DatasheetCompiler()
        compiler.compile_from_template(
            template_path=str(template_file),
            dataset=df,
            output_path=str(output_file),
            dataset_name='Test Dataset',
            version='0.1'
        )

        content = output_file.read_text(encoding='utf-8')

    assert '[This section will be automatically populated' not in content
    assert '[Please provide your answer here]' not in content.split('### Dataset Statistics')[1]
    assert 'Mean: 2.0000' in content
    assert 'Columns with numeric summary: 1' in content
    assert 'Detailed statistics for every column are listed below.' in content
    assert content.count('### Dataset Statistics') == 1
