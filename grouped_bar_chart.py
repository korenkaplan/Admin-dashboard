import datetime as dt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def create_grouped_bar_chart(data_frame):
    """
    Create a grouped bar chart to visualize the monthly spend by gender.

    Args:
        data_frame (pd.DataFrame): The DataFrame containing the data.

    Returns:
        plotly.graph_objects.Figure: The grouped bar chart.
    """
    # Convert order_date to datetime for manipulation
    data_frame['order_date'] = pd.to_datetime(data_frame['order_date'], format='mixed')

    # Extract the month from the order_date column
    data_frame['month'] = data_frame['order_date'].dt.month

    # Group by month and gender, and calculate the total amount
    grouped_df = data_frame.groupby(['month', 'gender'])['total'].sum().reset_index()

    # Create the grouped bar chart using Plotly Express
    fig = px.bar(grouped_df, x='month', y='total', color='gender',
                 labels={'month': 'Month', 'total': 'Total Spend'},
                 title='Monthly Spend By Gender', barmode='group', width=550)

    # Return the chart
    return fig
