import datetime as dt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px



def create_grouped_bar_chart(data_frame):
    """
    Create a grouped bar chart to visualize the total amount by month and gender.

    Args:
        data_frame (pd.DataFrame): The DataFrame containing the data.

    Returns:
        plotly.graph_objects.Figure: The grouped bar chart.
    """
    # Convert order_date to datetime
    data_frame['order_date'] = pd.to_datetime(data_frame['order_date'], format='mixed')

    # Extract the month from the order_date column
    data_frame['month'] = data_frame['order_date'].dt.month

    # Group by month and gender, and calculate the total amount
    grouped_df = data_frame.groupby(['month', 'gender'])['total'].sum().reset_index()

    # Create a bar trace for males
    trace_male = go.Bar(
        x=grouped_df[grouped_df['gender'] == 'male']['month'],
        y=grouped_df[grouped_df['gender'] == 'male']['total'],
        name='Male'
    )

    # Create a bar trace for females
    trace_female = go.Bar(
        x=grouped_df[grouped_df['gender'] == 'female']['month'],
        y=grouped_df[grouped_df['gender'] == 'female']['total'],
        name='Female'
    )

    # Create the layout for the chart
    layout = go.Layout(
        title='Total Amount by Month and Gender',
        xaxis=dict(title='Month'),
        yaxis=dict(title='Total Amount'),
        barmode='group'
    )

    # Create the figure and add the traces
    fig = go.Figure(data=[trace_male, trace_female], layout=layout)

    # Return the chart
    return fig