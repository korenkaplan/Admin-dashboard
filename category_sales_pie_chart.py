import streamlit as st
import pandas as pd
import plotly.express as px

# The size of the inner hole inside the pie chart
inner_hole_size = 0.3
# width of the chart
width = 500


def create_pie_chart(data_frame):
    """
    Create a pie chart to visualize the total sales by category.

    Args:
        data_frame (pd.DataFrame): The DataFrame containing the data.

    Returns:
        plotly.graph_objects.Figure: The pie chart.
    """
    is_one_category_selected = len(data_frame['category'].unique()) == 1

    # Get unique categories from the DataFrame
    categories = data_frame['category'].unique()

    # Create a select option for the category
    selected_category = categories[0] if is_one_category_selected else 'All Categories'

    # Get the filtered pie graph by the selected category
    fig = filter_data_from_selected_category(selected_category, data_frame)

    # Return the chart
    return fig


def filter_data_from_selected_category(selected_category, data_frame):
    """
    Filter the data based on the selected category and create a pie chart.

    Args:
        selected_category (str): The selected category or 'All Categories' if none selected.
        data_frame (pd.DataFrame): The DataFrame containing the data.

    Returns:
        plotly.graph_objects.Figure: The pie chart.
    """
    if selected_category == 'All Categories':
        # Group by category and calculate the sum of the total
        category_totals = data_frame.groupby('category')['total'].sum().reset_index()

        # Create a pie chart with Plotly Express
        return px.pie(category_totals, title='Distribution of sales per category', values='total', names='category',
                      hole=inner_hole_size, width=width)

    else:
        # Filter the DataFrame based on the selected category
        filtered_df = data_frame[data_frame['category'] == selected_category]
        # Create a pie chart with Plotly Express
        return px.pie(filtered_df, title=f'Distribution of sales per item in {selected_category}', values='total',
                      names='item_name', hole=inner_hole_size, width=width)
