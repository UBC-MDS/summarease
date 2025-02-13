import pytest
import pandas as pd
import altair as alt
from summarease.summarize_target import summarize_target_df, summarize_target_balance_plot

# Nonplot test --------------------------------------------------------------------

def test_categorical_correct_proportions():
    """
    Test categorical proportion correctness.
    """
    data = pd.DataFrame({"target": ["x", "y", "z", "x", "y", "y"]})
    result = summarize_target_df(data, "target", "categorical", threshold=0.2)
    expected_proportions = [2/6, 3/6, 1/6]
    assert result["proportion"].tolist() == expected_proportions

    assert (result["threshold"] == 0.2).all()  

def test_categorical_class_imbalance():
    """
    Test categorical class imbalance.
    """
    data = pd.DataFrame({"target": ["x", "y", "z", "x", "y", "y"]})
    result = summarize_target_df(data, "target", "categorical", threshold=0.2)
    assert result["imbalanced"].tolist() == [False, True, True]
    assert (result["threshold"] == 0.2).all()  

def test_categorical_default_threshold():
    """
    Test categorical default threshold.
    """
    data = pd.DataFrame({"target": ["x", "y", "z", "x", "y", "y"]})
    result = summarize_target_df(data, "target", "categorical")
    assert "imbalanced" in result.columns
    assert (result["threshold"] == 0.2).all()

def test_categorical_empty_dataset():
    """
    Tests if the function correctly handles an empty categorical dataset.
    """
    data = pd.DataFrame({"target": []})
    result = summarize_target_df(data, "target", "categorical", threshold=0.2)
    assert result.empty
    assert "threshold" in result.columns

def test_categorical_missing_column():
    """
    Tests if the function raises a KeyError when the specified target column is missing.
    """
    data = pd.DataFrame({"other_column": [1, 2, 3]})
    with pytest.raises(KeyError):
        summarize_target_df(data, "target", "categorical")

def test_numerical_descriptive_statistics():
    """
    Tests whether the function correctly computes descriptive 
    statistics (mean and standard deviation) for a numerical target variable.
    """
    data = pd.DataFrame({"target": [1, 2, 3, 4, 5]})
    with pytest.warns(UserWarning, match="Threshold is not used for numerical targets."):
        result = summarize_target_df(data, "target", "numerical", threshold=0.5)
    assert result.loc["target", "mean"] == 3
    assert result.loc["target", "std"] == pytest.approx(1.5811, 0.0001)

def test_categorical_extremely_imbalanced():
    """
    Tests if the function correctly identifies an extremely imbalanced 
    categorical target variable where one class dominates (99 occurrences of "x" and 1 of "y").
    """
    data = pd.DataFrame({"target": ["x"] * 99 + ["y"]})
    result = summarize_target_df(data, "target", "categorical", threshold=0.2)
    assert result["imbalanced"].tolist() == [True, True]

def test_categorical_equal_proportions():
    """
    Tests if the function correctly determines that all classes 
    are balanced when they have equal proportions.
    """
    data = pd.DataFrame({"target": ["x", "y", "z"] * 10})
    result = summarize_target_df(data, "target", "categorical", threshold=0.2)
    assert result["imbalanced"].tolist() == [False, False, False]

def test_numerical_identical_values():
    """
    Tests if the function correctly identifies a numerical target variable 
    where all values are identical, resulting in a standard deviation of zero.
    """
    data = pd.DataFrame({"target": [5, 5, 5, 5, 5]})
    with pytest.warns(UserWarning, match="Threshold is not used for numerical targets."):
        result = summarize_target_df(data, "target", "numerical", threshold=0.5)
    assert result.loc["target", "std"] == 0

def test_numerical_empty_dataset():
    """
    Tests if the function correctly handles an empty numerical dataset,
    returning an empty DataFrame.
    """
    data = pd.DataFrame({"target": []})
    result = summarize_target_df(data, "target", "numerical")
    assert result.empty

def test_invalid_target_type():
    """
    Tests if the function raises a ValueError when an invalid target type is provided.
    """
    data = pd.DataFrame({"target": [1, 2, 3]})
    with pytest.raises(ValueError):
        summarize_target_df(data, "target", "invalid_type")

def test_numerical_with_threshold_warning():
    """
    Tests whether the function raises a warning when a threshold 
    is provided for a numerical target variable.
    """
    data = pd.DataFrame({"target": [1, 2, 3, 4, 5]})
    with pytest.warns(UserWarning, match="Threshold is not used for numerical targets."):
        summarize_target_df(data, "target", "numerical", threshold=0.5)

def test_numerical_large_range():
    """
    Tests if the function correctly handles a numerical target variable 
    with a large range of values (1e8 to 5e8).
    """
    data = pd.DataFrame({"target": [1e8, 2e8, 3e8, 4e8, 5e8]})
    with pytest.warns(UserWarning, match="Threshold is not used for numerical targets."):
        result = summarize_target_df(data, "target", "numerical", threshold=0.5)
    assert not result.empty

def test_invalid_threshold():
    """
    Tests if the function raises a ValueError when an invalid threshold 
    (negative or greater than 1) is provided.
    """
    data = pd.DataFrame({"target": ["x", "x", "z", "x", "y", "z"]})
    with pytest.raises(ValueError):
        summarize_target_df(data, "target", "categorical", threshold=-0.1)
    with pytest.raises(ValueError):
        summarize_target_df(data, "target", "categorical", threshold=1.5)

def test_numerical_without_threshold():
    """
    Tests if the function correctly processes a numerical target variable 
    when no threshold is provided.
    """
    data = pd.DataFrame({"target": [1, 2, 3, 4, 5]})
    summarize_target_df(data, "target", "numerical", threshold=None)

# Plot test --------------------------------------------------------------------

def test_summarize_target_balance_plot_expected():
    """
    Test the function with a typical input DataFrame.
    """
    # Create a sample DataFrame
    summary_df = pd.DataFrame({
        'class': ['A', 'B', 'C'],
        'proportion': [0.4, 0.4, 0.2],
        'imbalanced': [False, False, True],
        'threshold': [0.2, 0.2, 0.2]
    })
    # Generate the plot
    chart = summarize_target_balance_plot(summary_df)
    # Validate that the output is Altair Chart
    assert isinstance(chart, alt.LayerChart), "The function should return an Altair LayerChart."

def test_summarize_target_balance_plot_empty():
    """
    Test the function with an empty DataFrame.
    """
    # Empty DataFrame
    empty_df = pd.DataFrame(columns=['class', 'proportion', 'imbalanced', 'threshold'])
    # Generate the plot
    chart = summarize_target_balance_plot(empty_df)
    # Validate that the chart displays an empty message
    assert isinstance(chart, alt.Chart), "The function should return an Altair Chart for an empty DataFrame."
    assert chart.mark == 'text', "The chart should display a message for empty data."

def test_summarize_target_balance_plot_imbalanced():
    """
    Test the function with an extremely imbalanced case.
    """
    summary_df = pd.DataFrame({
        'class': ['A', 'B'],
        'proportion': [0.9, 0.1],
        'imbalanced': [True, True],
        'threshold': [0.2, 0.2]
    })
    chart = summarize_target_balance_plot(summary_df)
    # Validate the presence of the imbalanced indicator
    assert isinstance(chart, alt.LayerChart), "The function should return an Altair LayerChart."

def test_summarize_target_balance_plot_invalid_columns():
    """
    Test the function with a DataFrame missing required columns.
    """
    invalid_df = pd.DataFrame({
        'class': ['A', 'B', 'C'],
        'proportion': [0.4, 0.4, 0.2]
    })
    # The function should raise a ValueError
    with pytest.raises(ValueError, match="Input DataFrame must contain columns: class, imbalanced, proportion, threshold"):
        summarize_target_balance_plot(invalid_df)

def test_summarize_target_balance_plot_extra_columns():
    """
    Test the function with additional, irrelevant columns.
    """
    summary_df = pd.DataFrame({
        'class': ['A', 'B', 'C'],
        'proportion': [0.4, 0.4, 0.2],
        'imbalanced': [False, False, True],
        'threshold': [0.2, 0.2, 0.2],
        'extra': [1, 2, 3]  # Irrelevant column
    })
    # Generate the plot
    chart = summarize_target_balance_plot(summary_df)
    # Validate that the chart still works
    assert isinstance(chart, alt.LayerChart), "The function should return an Altair LayerChart."

def test_summarize_target_balance_plot_large_threshold():
    """
    Test the function with a high threshold.
    """
    summary_df = pd.DataFrame({
        'class': ['A', 'B', 'C'],
        'proportion': [0.35, 0.35, 0.3],
        'imbalanced': [False, False, False],
        'threshold': [0.5, 0.5, 0.5]
    })
    chart = summarize_target_balance_plot(summary_df)
    # Validate that the expected range is correctly computed
    assert isinstance(chart, alt.LayerChart), "The function should return an Altair LayerChart."

def test_summarize_target_balance_plot_zero_classes():
    """
    Test the function with a DataFrame having zero class.
    """
    zero_class_df = pd.DataFrame(columns=['class', 'proportion', 'imbalanced', 'threshold'])
    chart = summarize_target_balance_plot(zero_class_df)
    # Validate the chart displays a message for empty data
    assert isinstance(chart, alt.Chart), "The function should return an Altair Chart for an empty DataFrame."
    assert chart.mark == 'text', "The chart should display a message for empty data."
