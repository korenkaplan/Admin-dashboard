import streamlit as st
import datetime as dt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sidebar import sidebar_config
from category_sales_pie_chart import create_pie_chart
from scatter_graph import create_scatter_plot
from grouped_bar_chart import create_grouped_bar_chart


def dashboard_config(transactions_user_df, projection):
    """
      Configure the sales dashboard.

      Args:
          transactions_user_df (pd.DataFrame): The DataFrame containing the transactions and user information.
          projection (list): The list of selected columns to project in the DataFrame.

      Returns:
          None
      """

    # Create the configuration for the page
    st.set_page_config(page_title='Sales Dashboard', page_icon=':bar_chart:', layout='wide')

    # header of the page
    header()

    # pass the data through the sidebar's filters.
    df_selection = sidebar_config(transactions_user_df[projection])

    # Convert the date to format: dd/mm/yyyy
    df_selection['order_date'] = df_selection['order_date'].dt.strftime('%m/%d/%Y')



    # The top row kpi(avg , total and Total transactions), and add the 'total' column to the data frame
    top_row_kpi(df_selection)

    # Display the table data frame
    st.dataframe(df_selection)

    # Create the charts from the filtered data_frame
    pie_chart, horizontal_bar, grouped_bar, scatter_plot = create_charts(df_selection)



    st.markdown('---')

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(pie_chart)
    with col2:
        st.plotly_chart(horizontal_bar)


    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grouped_bar)
    with col2:
        st.plotly_chart(scatter_plot)





def create_charts(data_frame):
    pie_chart = create_pie_chart(data_frame)
    horizontal_bar = create_horizontal_bar_chart(data_frame)
    grouped_bar = create_grouped_bar_chart(data_frame)
    scatter_plot = create_scatter_plot(data_frame)
    return pie_chart, horizontal_bar, grouped_bar, scatter_plot


def create_horizontal_bar_chart(data_frame):
    """
    Create a horizontal bar chart to visualize the total amount of money from sales for each item.

    Args:
        data_frame (pd.DataFrame): The DataFrame containing the data.

    Returns:
        plotly.graph_objects.Figure: The horizontal bar chart.
    """
    # Group by item_name and calculate the total amount
    grouped_df = data_frame.groupby('item_name')['total'].sum().reset_index()
    # Sort the DataFrame by total amount in descending order
    grouped_df = grouped_df.sort_values('total', ascending=True).tail(10)
    # Round the total values to 2 decimal places
    grouped_df['rounded_total'] = grouped_df['total'].round()
    # Create the horizontal bar chart using Plotly Express
    fig = px.bar(
        grouped_df,
        x='total',
        y='item_name',
        orientation='h',
        labels={'total': 'Total Amount in 💲', 'item_name': 'Item Name'},
        title='Top 10 selling items',
        text='rounded_total',
        width=550,
        )


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

