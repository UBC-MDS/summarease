# summarease

[![Documentation Status](https://readthedocs.org/projects/passwordler/badge/?version=latest)](https://passwordler.readthedocs.io/en/latest/?badge=latest)

## Project Summary

Summarease is a package designed to provide quick insights into a dataset by summarizing its key features. It offers functions that help users understand the structure of the data, making it easier to plan data cleaning and exploratory data analysis (EDA) tasks.

## Package Features

- `summarize_dtypes`:  
  Summarize the data types in the dataset.

- `summarize_target`:  
  Summarize and evaluate the target variable for categorical or numerical types. Generate a summary or proportion table for numerical or categorical target. Generate a visualization for categorical balance check.

- `summarize_numeric`:  
  Summarize the numeric variables in the dataset by providing the summary statistics (e.g., mean, standard deviation, min, max, etc.) for each numeric column or plotting the correlation heatmap to visualize the relationships between numeric variables. Generate density plots for each numeric column in the provided dataset. Generate a correlation heatmap for the specified numeric columns in a dataset.

- `summarize`:  
  Summarize generates a comprehensive PDF report for a dataset, including statistical summaries, visualizations, and target variable analysis. It supports customizable options like sample observations, automatic data cleaning, and flexible summarization methods (tables, plots, or both). Perfect for automating exploratory data analysis (EDA).

## Fit Within Python Ecosystem

Summarease is a lightweight and compact Python package designed for efficiency and ease of use. Despite its simplicity, it offers users great flexibility to customize the output format, whether through detailed tables or insightful visualizations.

Related packages with similar functionalities:  
1. [sweetviz](https://github.com/fbdesignpro/sweetviz)  
2. [ydata-profiling](https://github.com/ydataai/ydata-profiling)
3. [dtale](https://github.com/man-group/dtale)  

## Installation

```bash
$ pip install summarease
```
To install the development version from git, use:
```bash
$ pip install git+https://github.com/UBC-MDS/summarease.git
```

## Usage

First, import the `summarize` function from `summarease.summarize` module.

```python
from summarease.summarize import summarize
```

Next depending on the way you want summarize your datasets (whether using tables or plots) you can run the following commands:

#### For generating a report using plots:

The below code will generate a report that contains dominantly plots describing the numeric columns, target variable, correlation heatmap and a table summarizing the data types included in the data.

```python
summarize(
    dataset=iris_df, 
    dataset_name="Iris Dataset Summary", 
    description="Iris Dataset can be found on the UCI Machine Learning Repository",
    summarize_by="plot",
    target_variable="target",
    target_type="categorical",
    output_file="iris_summary.pdf",
    output_dir="./dataset_summary/"
)
```

#### For generating a report using tables:

The below code will generate a report that contains tables describing the numeric columns, target variable and data types.

```python
summarize(
    dataset=iris_df, 
    dataset_name="Iris Dataset Summary", 
    description="Iris Dataset can be found on the UCI Machine Learning Repository",
    summarize_by="table",
    target_variable="target",
    target_type="categorical",
    output_file="iris_summary.pdf",
    output_dir="./dataset_summary/"
)
```

To get in-depth idea of the function you can always run the following code:

```python
help(summarize)
```

If you find an error or inconsistency, please refer to the **Contributing** header.

## Contributing

Interested in contributing? Check out the contributing guidelines. 

Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`summarease` is licensed under the terms of the MIT license.

## Contributors

`summarease` was created by Hrayr Muradyan, Yun Zhou, Stephanie Wu, and Zuer Zhong.

## Credits

`summarease` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
