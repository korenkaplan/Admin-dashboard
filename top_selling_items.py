import pandas as pd
import plotly.express as px


# Graph width
GRAPH_WIDTH: int = 550
# The column to sum
TOTAL_COLUMN_STR: str = 'total'


def create_horizontal_bar_chart(data_frame):
    """
    Create a horizontal bar chart to visualize the total amount of money from sales for each item.

    Args:
        data_frame (pd.DataFrame): The DataFrame containing the data.

    Returns:
        plotly.graph_objects.Figure: The horizontal bar chart.
    """
    # Group by item_name and calculate the total amount
    grouped_df = data_frame.groupby('item_name')[TOTAL_COLUMN_STR].sum().reset_index()
    # Sort the DataFrame by total amount in descending order and show the tail 10 (its ascending order so tail is max)
    grouped_df = grouped_df.sort_values(TOTAL_COLUMN_STR, ascending=True).tail(10)
    # Round the total values
    grouped_df[TOTAL_COLUMN_STR] = grouped_df[TOTAL_COLUMN_STR].round()
    # Create the horizontal bar chart using Plotly Express
    fig = px.bar(
        grouped_df,
        x=TOTAL_COLUMN_STR,
        y='item_name',
        orientation='h',
        labels={TOTAL_COLUMN_STR: 'Total Amount in 💲', 'item_name': 'Item Name'},
        title='Top 10 selling items',
        text=TOTAL_COLUMN_STR,
        width=GRAPH_WIDTH,
        )
    # Return the chart
    return fig
