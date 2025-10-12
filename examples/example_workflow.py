#!/usr/bin/env python3
"""Comprehensive workflow example for the semi-automatic datasheet generation tool.

This example demonstrates the complete user workflow:
1. Generate empty questionnaire template
2. Fill documentation sections manually
3. Run automated analysis on dataset
4. Compile complete datasheet
"""

from pathlib import Path

import numpy as np
import pandas as pd

from dfd.datasheet.compiler import DatasheetCompiler

# Import our datasheet generation modules
from dfd.datasheet.manager import TemplateManager


def demonstrate_complete_workflow():
    """Demonstrate the complete datasheet generation workflow."""
    print('=' * 60)
    print('DATASHEET GENERATION TOOL - COMPLETE WORKFLOW EXAMPLE')
    print('=' * 60)
    print()

    # Step 1: Generate empty template
    print('Step 1: Generating empty datasheet template...')
    template_path = 'example_datasheet_template.md'

    manager = TemplateManager()
    template_content = manager.generate_empty_template(template_path)

    print(f'✓ Empty template generated: {template_path}')
    print(f"  Template contains {len(template_content.split('##')) - 1} main sections")
    print()

    # Step 2: Simulate filling the template (in real workflow, user would do this manually)
    print('Step 2: Simulating manual template completion...')
    filled_template_path = 'example_filled_template.md'

    # Create a sample filled template
    filled_content = create_sample_filled_template()
    Path(filled_template_path).write_text(filled_content, encoding='utf-8')

    print(f'✓ Filled template created: {filled_template_path}')
    print('  (In real workflow, user would manually fill this template)')
    print()

    # Step 3: Create sample dataset
    print('Step 3: Creating sample dataset...')
    dataset_path = 'example_dataset.csv'
    sample_dataset = create_sample_dataset()
    sample_dataset.to_csv(dataset_path, index=False)

    print(f'✓ Sample dataset created: {dataset_path}')
    print(f'  Dataset shape: {sample_dataset.shape}')
    print(f'  Columns: {list(sample_dataset.columns)}')
    print()

    # Step 4: Compile complete datasheet
    print('Step 4: Compiling complete datasheet with automated analysis...')
    output_path = 'complete_datasheet.md'

    compiler = DatasheetCompiler()
    result_path = compiler.compile_from_template(
        template_path=filled_template_path,
        dataset=sample_dataset,
        output_path=output_path,
        dataset_name='Sample Customer Dataset',
        version='1.0'
    )

    print(f'✓ Complete datasheet generated: {result_path}')
    print()

    # Step 5: Display results summary
    print('Step 5: Results Summary')
    print('-' * 30)

    final_content = Path(result_path).read_text(encoding='utf-8')
    sections = len([line for line in final_content.split('\n') if line.startswith('## ')])
    word_count = len(final_content.split())

    print('Final datasheet contains:')
    print(f'  - {sections} main sections')
    print(f'  - {word_count} words')
    print('  - Manual documentation + automated analysis')
    print()

    return {
        'template_path': template_path,
        'filled_template_path': filled_template_path,
        'dataset_path': dataset_path,
        'output_path': result_path
    }


def create_sample_filled_template() -> str:
    """Create a sample filled template with realistic content.

    Returns:
        Filled template content as string
    """
    return '''# Datasheet for Dataset

*This datasheet template is based on the paper ['Datasheets for Datasets' by Gebru et al.](https://arxiv.org/abs/1803.09010)*

**Dataset Name:** Sample Customer Dataset

**Date:** 2024-01-15

**Version:** 1.0

---

## Motivation

*The questions in this section are primarily intended to encourage dataset creators to clearly articulate their reasons for creating the dataset and to promote transparency about funding interests.*

### For what purpose was the dataset created?

This dataset was created to demonstrate the datasheet generation tool and provide a realistic example of customer data for testing machine learning models. The dataset contains synthetic customer information including demographics, purchase history, and satisfaction scores.

**Was there a specific task in mind?**

Yes, the dataset is designed for customer segmentation and churn prediction tasks.

**Was there a specific gap that needed to be filled?**

This fills the gap of having a clean, well-documented example dataset for demonstrating the datasheet generation workflow.

### Who created the dataset?

The dataset was created by the datasheet generation tool development team as part of the example workflow.

**Which team or research group?**

Datasheet Generation Tool Development Team

**On behalf of which entity (e.g., company, institution, organization)?**

Open source project for dataset documentation

### Who funded the creation of the dataset?

This is a synthetic dataset created for demonstration purposes with no external funding.

### Any other comments?

This dataset is entirely synthetic and created solely for demonstration purposes. It should not be used for any production machine learning tasks.

---

## Composition

*Dataset creators should read through the questions in this section prior to any data collection and then provide answers once collection is complete.*

### What do the instances that comprise the dataset represent?

Each instance represents a synthetic customer with their demographic information, purchase history, and satisfaction metrics.

### How many instances are there in total?

The dataset contains 1000 synthetic customer records.

### Does the dataset contain all possible instances or is it a sample?

This is a synthetic sample created for demonstration purposes.

### What data does each instance consist of?

Each instance contains:
- Customer ID
- Age
- Gender
- Income
- Purchase amount
- Satisfaction score
- Churn indicator

---

## Collection Process

*As with the previous section, dataset creators should read through these questions prior to any data collection to flag potential issues and then provide answers once collection is complete.*

### How was the data associated with each instance acquired?

The data was synthetically generated using random number generators with realistic distributions and correlations.

### What mechanisms or procedures were used to collect the data?

Python's numpy and pandas libraries were used to generate synthetic data with predefined statistical properties.

### If the dataset is a sample from a larger set, what was the sampling strategy?

Not applicable - this is entirely synthetic data.

---

## Preprocessing

*Dataset creators should read through these questions prior to any data collection to flag potential issues and then provide answers once collection is complete.*

### Was any preprocessing/cleaning/labeling of the data done?

Minimal preprocessing was applied:
- Ensured no missing values
- Applied realistic constraints (e.g., age between 18-80)
- Normalized satisfaction scores to 1-10 scale

### Was the "raw" data saved in addition to the preprocessed/cleaned/labeled data?

The data was generated directly in its final form.

---

## Uses

*These questions are intended to encourage dataset creators to reflect on the tasks for which the dataset should and should not be used.*

### Has the dataset been used for any tasks already?

This dataset is used for demonstrating the datasheet generation tool workflow.

### Is there a repository that links to any or all papers or systems that use the dataset?

No, this is a demonstration dataset.

### What (other) tasks could the dataset be used for?

The dataset could be used for:
- Learning data analysis techniques
- Testing visualization tools
- Demonstrating machine learning workflows

### Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?

Yes, being entirely synthetic, it may not reflect real-world data complexities and should not be used for production systems.

---

## Distribution

*Dataset creators should read through these questions prior to any data collection to flag potential issues and then provide answers once collection is complete.*

### Will the dataset be distributed to third parties outside of the entity?

Yes, as part of the open source datasheet generation tool.

### How will the dataset be distributed?

Through the project's GitHub repository as an example file.

### When will the dataset be distributed?

Immediately upon tool release.

### Will the dataset be distributed under a copyright or other intellectual property (IP) license?

Yes, under the same open source license as the main project.

---

## Maintenance

*These questions are intended to encourage dataset creators to plan for dataset maintenance and communicate this plan with dataset consumers.*

### Who will be supporting/hosting/maintaining the dataset?

The datasheet generation tool development team.

### How can the owner/curator/manager of the dataset be contacted?

Through the project's GitHub repository issues.

### Is there an erratum?

No errata at this time.

### Will the dataset be updated?

The dataset may be updated if needed for better demonstration purposes.

---
'''


def create_sample_dataset() -> pd.DataFrame:
    """Create a sample dataset for demonstration.

    Returns:
        Sample pandas DataFrame
    """
    # Set random seed for reproducibility
    rng = np.random.default_rng(42)

    n_samples = 1000

    # Generate synthetic customer data
    data = {
        'customer_id': range(1, n_samples + 1),
        'age': rng.normal(40, 12, n_samples).astype(int).clip(18, 80),
        'gender': rng.choice(['Male', 'Female', 'Other'], n_samples, p=[0.45, 0.45, 0.1]),
        'income': rng.lognormal(10.5, 0.5, n_samples).astype(int),
        'purchase_amount': rng.exponential(100, n_samples).round(2),
        'satisfaction_score': rng.normal(7.5, 1.5, n_samples).clip(1, 10).round(1),
        'churn': rng.choice([0, 1], n_samples, p=[0.8, 0.2])
    }

    df = pd.DataFrame(data)

    # Use numpy's Generator for reproducibility and better random control
    rng = np.random.default_rng(42)

    # Add some correlations to make it more realistic
    # Higher income tends to have higher satisfaction
    high_income_mask = df['income'] > df['income'].quantile(0.75)
    df.loc[high_income_mask, 'satisfaction_score'] += rng.normal(0.5, 0.3, high_income_mask.sum())
    df['satisfaction_score'] = df['satisfaction_score'].clip(1, 10).round(1)

    # Lower satisfaction increases churn probability
    low_satisfaction_value = 5
    low_satisfaction_mask = df['satisfaction_score'] < low_satisfaction_value
    df.loc[low_satisfaction_mask, 'churn'] = rng.choice([0, 1], low_satisfaction_mask.sum(), p=[0.3, 0.7])

    return df


def demonstrate_programmatic_usage():
    """Demonstrate programmatic usage of the datasheet generation system."""
    print('\n' + '=' * 60)
    print('PROGRAMMATIC USAGE EXAMPLE')
    print('=' * 60)

    # Create sample data
    sample_data = create_sample_dataset()

    # Method 1: Using TemplateManager directly
    print('\nMethod 1: Using TemplateManager')
    print('-' * 30)

    manager = TemplateManager()

    # Generate template
    template_content = manager.generate_empty_template()
    print(f'Generated template with {len(template_content)} characters')

    # Create datasheet structure
    structure = manager.create_datasheet_structure()
    print(f'Created structure with {len(structure.cards)} cards')

    # Method 2: Using DatasheetCompiler
    print('\nMethod 2: Using DatasheetCompiler')
    print('-' * 30)

    compiler = DatasheetCompiler()

    # Compile from scratch with minimal manual content
    manual_content = {
        'Motivation': 'This dataset demonstrates the datasheet generation tool.',
        'Composition': 'Contains 1000 synthetic customer records.'
    }

    result_path = compiler.compile_from_scratch(
        dataset=sample_data,
        output_path='programmatic_datasheet.md',
        dataset_name='Programmatic Example Dataset',
        manual_content=manual_content
    )

    print(f'Generated datasheet: {result_path}')

    # Method 3: Integration with existing Datasheet class
    print('\nMethod 3: Integration with Datasheet class')
    print('-' * 30)

    datasheet_obj = compiler.create_datasheet_with_analysis(
        dataset=sample_data,
        dataset_name='Integration Example',
        output_path='integrated_datasheet.md'
    )

    print('Name of datasheet:', datasheet_obj.dataset_name)
    print('Created Datasheet object with analysis integration')
    print('Datasheet contains automated statistical analysis')


if __name__ == '__main__':
    # Run the complete workflow demonstration
    results = demonstrate_complete_workflow()

    # Show programmatic usage
    demonstrate_programmatic_usage()

    print('\n' + '=' * 60)
    print('ALL EXAMPLES COMPLETED SUCCESSFULLY!')
    print('=' * 60)
    print('\nGenerated files:')
    for key, path in results.items():
        if Path(path).exists():
            print(f'  ✓ {key}: {path}')
        else:
            print(f'  ✗ {key}: {path} (not found)')
