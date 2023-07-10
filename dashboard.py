import streamlit as st
import datetime as dt
import pandas as pd
import plotly.express as px
from sidebar import sidebar_config
from category_sales_pie_chart import create_pie_chart


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
    df_selection['order_date'] = df_selection['order_date'].dt.strftime('%d/%m/%Y')
    # The top row kpi(avg , total and Total transactions)
    top_row_kpi(df_selection)
    # show the data frame
    st.dataframe(df_selection)
    fig = create_pie_chart(df_selection)
    st.plotly_chart(fig)




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

