import plotly.express as px


# Graph width
GRAPH_WIDTH = 550


def create_scatter_plot2(data_frame):
    # Group by age and sum the total spend
    grouped_df = data_frame.groupby(['age', 'gender'])['total'].sum().reset_index()

    # Define color mapping for male and female
    color_mapping = {'male': 'blue', 'female': 'red'}
    # Create a scatter plot using plotly express
    fig = px.scatter(grouped_df, x='age', y='total',
                     labels={'age': 'Age', 'total': 'Total Spend'},
                     title='Age vs. Total Spend',
                     width=GRAPH_WIDTH,
                     color_discrete_map=color_mapping,
                     color='gender')

    # Add legend for item names
    fig.update_layout(legend_title_text='Items')

    # Return the scatter plot
    return fig






