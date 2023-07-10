import streamlit as st
import datetime as dt
import pandas as pd
import plotly.express as px
# The size of the inner hole inside th pie chart
inner_hole_size = .3


def create_pie_chart(data_frame):
    """
        Create a pie chart to visualize the total sales by category.

        Args:
            data_frame (pd.DataFrame): The DataFrame containing the data.

        Returns:
            plotly.graph_objects.Figure: The pie chart.
    """
    # Group by category and calculate the sum of the total
    category_totals = data_frame.groupby('category')['total'].sum().reset_index()

    # Create a pie chart with Plotly Express
    fig = px.pie(category_totals, values='total', names='category')

    # Get unique categories from the DataFrame
    categories = data_frame['category'].unique()

    # Create a select option for the category
    selected_category = st.selectbox('Select a category', ['All Categories'] + list(categories))
    # Get the filtered pie graph by the selected category
    fig = filter_data_from_selected_category(selected_category, data_frame)

    # Return the chart
    return fig


def filter_data_from_selected_category(selected_category, data_frame):
    """
        Filter the data based on the selected category and create a pie chart.

        Args:
            selected_category (str): The selected category.
            data_frame (pd.DataFrame): The DataFrame containing the data.

        Returns:
            plotly.graph_objects.Figure: The pie chart.
    """
    if selected_category == 'All Categories':
        # Group by category and calculate the sum of the total
        category_totals = data_frame.groupby('category')['total'].sum().reset_index()

        # Create a pie chart with Plotly Express
        return px.pie(category_totals, values='total', names='category', hole=inner_hole_size)

    else:
        # Filter the DataFrame based on the selected category
        filtered_df = data_frame[data_frame['category'] == selected_category]
        # Group by item_name and calculate the sum of the total
        item_totals = filtered_df.groupby('item_name')['total'].sum().reset_index()
        # Create a pie chart with Plotly Express
        return px.pie(filtered_df, values='total', names='item_name', hole=inner_hole_size)