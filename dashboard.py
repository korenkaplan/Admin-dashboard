import streamlit as st
import pandas as pd
import datetime
from sidebar import sidebar_config
from category_sales_pie_chart import create_pie_chart
from scatter_graph import create_scatter_plot2
from grouped_bar_chart import create_grouped_bar_chart
from top_selling_items import create_horizontal_bar_chart

excel_file_url = r'C:\Users\Koren Kaplan\Desktop\לימודים\Projects\Python Final Project\AdminDash\Excel file to upload\Python_Scan_and_Gos_sales_analytics_2022.xlsx'
def init_dashboard(projection):
    """
    The start-up function wait for the user to upload the Excel file then start the dashboard
    Params:
     projection: the columns to project in the data frame
    Return:
         None
    """
    # Create the Tab configuration for the page
    st.set_page_config(page_title='Scan & Go 2022 Analytics', page_icon=':bar_chart:', layout='wide')
    # Create the main header of the page
    header()
    # # Create the container once the file is loaded the upload file container will disappear
    # holder = st.empty()
    # # The upload file container
    # uploaded_file = holder.file_uploader("Choose the Scan & Go analytics excel file ", type="xlsx", accept_multiple_files=False)
    # # Once the file is uploaded hide the container and start the dashboard configuration reading from the Excel file
    # if uploaded_file:
    #     # Hide the upload file container
    #     holder.empty()
    # Read the file (sheet_name=None -> read all the sheets in the file)
    df = pd.read_excel(excel_file_url, sheet_name=None)
    # Merge all the sheets to a data frame
    merged_df = merge_sheets_in_excel_file(df)
    # Start the dashboard configuration with the data frame
    dashboard_config(merged_df, projection)


def merge_sheets_in_excel_file(df):
    """
    Merge the sheets and perform a join on the user_id and item_id to the desired data frame
    Args:
     df: an unfiltered data frame
    Return:
         merged_df: a merged data frame
    """
    sheet_dict = {sheet_name: data_frame for sheet_name, data_frame in df.items()}
    merged_df = pd.merge(sheet_dict['users'], sheet_dict['transactions'], on='user_id')
    merged_df = pd.merge(merged_df, sheet_dict['items'], on='item_id')
    return merged_df


def dashboard_config(main_data_frame, projection):
    """
      Configure the sales dashboard. The main body of the page

      Args:
          main_data_frame (pd.DataFrame): The DataFrame containing the transactions and user information.
          projection (list): The list of string representing the selected columns to project in the DataFrame.

      Returns:
          None
      """


    # Convert the birth_date column to age column for easier manipulations.
    main_data_frame = convert_birth_date_to_age_column(main_data_frame)

    # Pass the data through the sidebar's filters. and get back the filtered data frame
    filtered_data_frame = sidebar_config(main_data_frame[projection])

    # Convert the order date to format: dd/mm/yyyy
    filtered_data_frame['order_date'] = filtered_data_frame['order_date'].dt.strftime('%m/%d/%Y')

    # The top row kpi(avg, total and  amount of  transactions), plus add the 'total' column to the data frame
    top_row_kpi(filtered_data_frame)

    # Display the table data frame
    st.dataframe(filtered_data_frame, use_container_width=True, hide_index=True)

    # Create the charts from the filtered data_frame
    pie_chart, horizontal_bar, grouped_bar, scatter_plot = create_charts(filtered_data_frame)

    # Create a Divider under the main table
    st.markdown('---')

    # Create the first row containing the pie chart and the horizontal bar chart. the row divided to two columns
    left_col, right_col = st.columns(2)
    with left_col:
        st.plotly_chart(pie_chart)
    with right_col:
        st.plotly_chart(horizontal_bar)

    # Create the second row containing the grouped bar chart and the scatter plot.the row divided to two columns
    left_col, right_col = st.columns(2)
    with left_col:
        st.plotly_chart(grouped_bar)
    with right_col:
        st.plotly_chart(scatter_plot)


def convert_birth_date_to_age_column(main_data_frame):

    # Convert birth_date column to datetime
    main_data_frame['birth_date'] = pd.to_datetime(main_data_frame['birth_date'])

    # Calculate age based on birthdate
    current_year = datetime.datetime.now().year
    main_data_frame['age'] = current_year - main_data_frame['birth_date'].dt.year

    return main_data_frame


def create_charts(data_frame: pd.DataFrame):
    """
    Creates various charts based on the filtered data frame.
    Args:
     data_frame (pd.DataFrame): The DataFrame containing the filtered data.
    Returns:
        tuple: A tuple containing the pie chart, horizontal bar chart, grouped bar chart, and scatter plot.
    """
    pie_chart = create_pie_chart(data_frame)
    horizontal_bar = create_horizontal_bar_chart(data_frame)
    grouped_bar = create_grouped_bar_chart(data_frame)
    scatter_plot = create_scatter_plot2(data_frame)
    return pie_chart, horizontal_bar, grouped_bar, scatter_plot


def top_row_kpi(data_frame):
    """
    Display key performance indicators (KPIs) in the top row. And add the total column to the
    data frame representing the total amount of the transaction.

    Args:
        data_frame (pd.DataFrame): The DataFrame containing the sales data.

    Returns:
        None
    """
    # The 'total' column from the data frame, string to avoid writing repeatedly
    total_col = 'total'
    # Calculate the total amount for each transaction by multiplying 'amount' and 'price' columns
    data_frame[total_col] = data_frame['amount'] * data_frame['price']

    # Check if only a single item is selected
    is_single_item_selected = len(data_frame.groupby('item_name').count()) <= 1

    # Calculate the total sum, average sale, total sales amount, and number of transactions
    total_sum = int(data_frame[total_col].sum())
    avg_sale = round(data_frame[total_col].mean(), 1)
    avg_sale = avg_sale if avg_sale > 0 else 0
    total_sales_amount = int(data_frame['amount'].sum())
    transactions_amount = len(data_frame)

    # Set the title and value based on whether a single item is selected or not
    if not is_single_item_selected:
        title = 'Total Transactions:'
        value = transactions_amount
    else:
        title = 'Total Units Sold:'
        value = total_sales_amount

    # Display the KPIs in three columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Total Sales:")
        st.subheader(f'💲 {total_sum}')
    with col2:
        st.subheader("Avg Sale:")
        st.subheader(f'💲 {avg_sale}')
    with col3:
        st.subheader(title)
        st.subheader(f':hash: {value}')


def header():
    """
    Display the header of the sales dashboard.

    Returns:
        None
    """
    st.title(':bar_chart: Scan & Go 2022 Sales Analytics')
    st.markdown('---')
