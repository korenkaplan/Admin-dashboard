import streamlit as st
import datetime as dt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sidebar import sidebar_config
from category_sales_pie_chart import create_pie_chart
from scatter_graph import create_scatter_plot


def dashboard_config(transactions_user_df, projection):
    """
      Configure the sales dashboard.

      Args:
          transactions_user_df (pd.DataFrame): The DataFrame containing the transactions and user information.
          projection (list): The list of selected columns to project in the DataFrame.

      Returns:
          None
      """
    # Create the configuration for streamlit
    st.set_page_config(page_title='Sales Dashboard', page_icon=':bar_chart:', layout='wide')
    # header of the page
    header()
    # pass the data through the sidebar's filters.
    df_selection = sidebar_config(transactions_user_df[projection])
    # Convert the date to format: dd/mm/yyyy
    df_selection['order_date'] = df_selection['order_date'].dt.strftime('%m/%d/%Y')
    # The top row kpi(avg , total and Total transactions)
    top_row_kpi(df_selection)
    # Display the data frame
    st.dataframe(df_selection)

    # Create and display the pie chart
    fig = create_pie_chart(df_selection)
    st.plotly_chart(fig)

    grouped_bar = create_grouped_bar_chart(df_selection)
    st.plotly_chart(grouped_bar)

    # Create and display the scatter plot
    # scatter_plot = create_scatter_plot(df_selection)
    # st.plotly_chart(scatter_plot)


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


def top_row_kpi(data_frame):
    """
     Display key performance indicators (KPIs) in the top row.

     Args:
         data_frame (pd.DataFrame): The DataFrame containing the sales data.

     Returns:
         None
     """
    data_frame['total'] = data_frame['amount'] * data_frame['price']
    total_sum = int(data_frame['total'].sum())
    avg_sale = round(data_frame['total'].mean(), 1)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Total Sales:")
        st.subheader(f'💲 {total_sum}')
    with col2:
        st.subheader("Avg Sale:")
        st.subheader(f'💲 {avg_sale}')
    with col3:
        st.subheader("Total transactions:")
        st.subheader(f':hash: {len(data_frame)}')


def header():
    """
    Display the header of the sales dashboard.

    Returns:
        None
    """
    st.title(':bar_chart: Scan & Go Dashboard')
    st.markdown('---')

