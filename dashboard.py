import streamlit as st
import pandas as pd
import datetime
import time
import re
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from datetime import datetime, timedelta
import plotly.express as px

excel_file_url1 = r'Excel_file_to_upload/ComplainReport13112024.xlsx'
excel_file_url = r'Excel_file_to_upload/Python_Scan_and_Gos_sales_analytics_2022.xlsx'
recentFile= None
parsedDf = None
selected_column= None


# Add an on-change event handler
def on_change():
     
     st.write(f"You selected the '{st.session_state['selected_teams']}' column.")
     with st.expander("Additional Dashboard Section"):        
        FilterData(st.session_state['selected_teams'])


def FilterData(team):
    data = st.session_state.current_data
    count = data[data['team'].isin(st.session_state.selected_teams)]['Ticket ID'].count()
    waitTime = data[data['team'].isin(st.session_state.selected_teams)]['wait_time'].sum()
    transferred = data[data['team'].isin(st.session_state.selected_teams)]['Transferred From']
    st.write(f"Team {team} Total Ticket {count}")
    st.write(f"Team {team} Total wait Time {waitTime}")
    st.dataframe(transferred, use_container_width=True, hide_index=True)



def dataCalculate(dataFrame):         
            # Specify the columns to parse and save
            parse_column = 'Team wise History'
            save_column = 'Ticket ID'

            # Initialize a list to store parsed data
            parsed_data = []

            # Function to parse the data
            def parse_data(data):
                pattern = r"@@FD:(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) , T:(.*?), WT:(\d+) D (\d+) H (\d+) M (\d+) S"
                matches = re.findall(pattern, data)
                parsed_entries = []
                for match in matches:
                    date_str, team, days, hours, minutes, seconds = match
                    date = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
                    wait_time = timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))
                    wait_time2= (int(days)*24*60)+(int(hours)*60)+(int(minutes))
                    parsed_entries.append({
                        "date": date,
                        "team": team,
                        "days": days,
                        "hours": hours,
                        "minutes": minutes,
                        "seconds": seconds,
                        "wait_time": wait_time2
                    })
                return parsed_entries

            # Loop through the specified column to parse the data and save another column entry
            for index, entry in dataFrame[parse_column].dropna().items():
                parsed_entries = parse_data(entry)
                save_entry = dataFrame.at[index, save_column]
                #previous_team = None (so that it is not blank)
                previous_team = "Initiated"
                for parsed_entry in parsed_entries:
                    parsed_data.append([save_entry, parsed_entry['date'], parsed_entry['team'], previous_team, parsed_entry['days'], parsed_entry['hours'], parsed_entry['minutes'], parsed_entry['seconds'], parsed_entry['wait_time']])
                    previous_team = parsed_entry['team']

            # Create a DataFrame to save the parsed data and the saved column entries
            parsed_df = pd.DataFrame(parsed_data, columns=[save_column, 'date', 'team', 'Transferred From', 'days', 'hours', 'minutes', 'seconds', 'wait_time'])
            # Save the DataFrame to a new Excel file
            #check            
            
            # Load the parsed data from the Excel file
            df = parsed_df
            # Create a graph for the number of entries per team
            fig1 = plt.figure(figsize=(10, 6))
            df['team'].value_counts().plot(kind='bar')
            plt.title('Number of Entries per Team')
            plt.xlabel('Team')
            plt.ylabel('Number of Entries')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.close()

            # Create a graph for the total wait time per team
            df['wait_time'] = pd.to_timedelta(df['wait_time'])            
            total_wait_time_per_team = df.groupby('team')['wait_time'].sum()

            fig2 = plt.figure(figsize=(10, 6))
            total_wait_time_per_team.plot(kind='bar')
            plt.title('Total Wait Time per Team')
            plt.xlabel('Team')
            plt.ylabel('Total Wait Time')
            plt.xticks(rotation=45)
            plt.tight_layout()          
            plt.close()

            # Create a graph for the average wait time per team 
            average_wait_time_per_team = df.groupby('team')['wait_time'].mean()

            fig3 = plt.figure(figsize=(10, 6))
            average_wait_time_per_team.plot(kind='bar')
            plt.title('Average Wait Time per Team')
            plt.xlabel('Team')
            plt.ylabel('Average Wait Time')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.close()
            return parsed_df,fig1, fig2, fig3
        



def generateData():
        st.spinner()
        file = st.session_state['uploaded_file']
        sheet_name = 'ComplainReport'
        if file is not None:
           df = pd.read_excel(file, sheet_name=sheet_name)        
        st.success('File Uploaded Successfully', icon="✅")
        
        with st.spinner('please Wait for data...'):          
          data,fig1,fig2,fig3 = dataCalculate(df)
          time.sleep(7)          
          st.success("Done!")          
          dashboard_config(data,fig1,fig2,fig3) 
        return None

def create_sidebar_filters():
    """Create and manage all sidebar filters"""
    with st.sidebar:
        st.title("Dashboard Filters")

        # Only proceed with filters if data is loaded
        if not st.session_state.get('data_loaded', False):
            st.info("Please upload data to enable filters")
            return

        df = st.session_state.get('current_data')
        if df is None or df.empty:
            return

        st.markdown("### Date Range")
        # Convert date column to datetime if it's not already
        df['date'] = pd.to_datetime(df['date'])
        min_date = df['date'].dt.date.min()
        max_date = df['date'].dt.date.max()

        # Preset date range buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('Last 7 Days'):
                st.session_state.date_range = [
                    max_date - timedelta(days=7),
                    max_date
                ]
        with col2:
            if st.button('Last 30 Days'):
                st.session_state.date_range = [
                    max_date - timedelta(days=30),
                    max_date
                ]
        with col3:
            if st.button('All Time'):
                st.session_state.date_range = [min_date, max_date]

        # Custom date range picker
        date_range = st.date_input(
            "Select Custom Date Range",
            value=(
                st.session_state.get('date_range', [min_date, max_date])
            ),
            min_value=min_date,
            max_value=max_date,
            key='date_range'
        )

        st.markdown("### Team Selection")
        all_teams = df['team'].unique()
        selected_teams = st.multiselect(
            "Select Teams",
            options=all_teams,
            default=all_teams,
            on_change=on_change,
            key='selected_teams'
        )

        st.markdown("### Transfer Source")
        all_transfers = df['Transferred From'].unique()
        selected_transfers = st.multiselect(
            "Select Transfer Sources",
            options=all_transfers,
            default=all_transfers,
            key='selected_transfers'
        )

        st.markdown("### Wait Time Range")
        min_wait = float(df['wait_time'].min())
        max_wait = float(df['wait_time'].max())
        wait_time_range = st.slider(
            "Select Wait Time Range (hours)",
            min_value=min_wait,
            max_value=max_wait,
            value=(min_wait, max_wait),
            key='wait_time_range'
        )

        # Add a reset filters button
        if st.button('Reset All Filters'):
            st.session_state.date_range = [min_date, max_date]
            st.session_state.selected_teams = list(all_teams)
            st.session_state.selected_transfers = list(all_transfers)
            st.session_state.wait_time_range = (min_wait, max_wait)
            st.experimental_rerun()

        # Apply filters
        filtered_df = apply_filters(df)
        st.session_state.filtered_data = filtered_df
        if filtered_df is not None:
            st.markdown("### Filter Summary")
            st.info(f"Showing {len(filtered_df)} of {len(df)} records")

        return filtered_df


def apply_filters(df):
    """Apply all filters to the dataframe based on sidebar selections"""
    if df is None or df.empty:
        return None

    filtered_df = df.copy()
    
    # Convert date column to datetime if it's not already
    filtered_df['date'] = pd.to_datetime(filtered_df['date'])

    # Apply date range filter
    if 'date_range' in st.session_state and st.session_state.date_range is not None:
        start_date, end_date = st.session_state.date_range
        filtered_df = filtered_df[
            (filtered_df['date'].dt.date >= start_date) & 
            (filtered_df['date'].dt.date <= end_date)
        ]

    # Apply team filter
    if 'selected_teams' in st.session_state and st.session_state.selected_teams:
        filtered_df = filtered_df[filtered_df['team'].isin(st.session_state.selected_teams)]

    # Apply Transferred From filter
    if 'selected_transfers' in st.session_state and st.session_state.selected_transfers:
        filtered_df = filtered_df[filtered_df['Transferred From'].isin(st.session_state.selected_transfers)]

    # Apply wait time range filter
    if 'wait_time_range' in st.session_state:
        min_wait, max_wait = st.session_state.wait_time_range
        filtered_df = filtered_df[
            (filtered_df['wait_time'] >= min_wait) & 
            (filtered_df['wait_time'] <= max_wait)
        ]
     
    return filtered_df

def create_summary_section(df):
    """
    Generate the summary section of the dashboard based on the provided DataFrame.
    """
    if df is None or df.empty:
        total_customers = 0.00
        avrg_time_wait = 0.00
        average_review_rating = 0.00
        teams = 0.00

    # Calculate summary metrics
    else:
        df['wait_time'] = df['wait_time'].astype(int)
        total_customers = len(df['Ticket ID'].unique())
        avrg_time_wait = df['wait_time'].mean()
        average_review_rating = df['wait_time'].median()
        teams = len(df['team'].unique())
    
    # Define box styles
    colors = ["#4C5270", "#F652A0", "#36EEE0", "#059DC0"]
    box_styles = [
        {"background-color": colors[0], "color": "white", "font-size": "20px"},
        {"background-color": colors[1], "color": "white", "font-size": "20px"},
        {"background-color": colors[2], "color": "white", "font-size": "15px"},
        {"background-color": colors[3], "color": "white", "font-size": "15px"}
    ]

    # Define customer_info data
    customer_info = [
        {"top_text": "Total Tickets", "bottom_text": f"{total_customers:,}"},
        {"top_text": "Total Teams", "bottom_text": f"{teams:,}"},
        {"top_text": "Average Wait Time", "bottom_text": f"{avrg_time_wait:.2f} sec"},
        {"top_text": "Average Resolution Time", "bottom_text": f"{average_review_rating:.2f} sec"}
        
    ]

    # Create the summary section
    summary_container = st.container()
    with summary_container:
        st.subheader("Summary")

        customer_count_cols = st.columns(4)
        for i in range(4):
            with customer_count_cols[i]:
                st.markdown(
                    f"<div style='{'; '.join([f'{prop}: {value}' for prop, value in box_styles[i].items()])}; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; padding: 10px; margin: 0px; height: 100px;'>"
                    f"<div style='font-size: 14px;'>{customer_info[i]['top_text']}</div>"
                    f"<div style='font-size: 34px; font-weight: bold; text-align: center;'>{customer_info[i]['bottom_text']}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

def init_dashboard(projection=['full_name', 'age', 'gender', 'item_name', 'category', 'item_tags', 'season', 'printing', 'price', 'amount', 'order_date']):
   
    st.set_page_config(page_title='Complaint Ticket Analytics', page_icon=':bar_chart:', layout='wide')
        
    recentFile = st.sidebar.file_uploader("Choose a file",type=["xlsx"],on_change=generateData,key='uploaded_file')
    
    # Merge all the sheets to a data frame
    # merged_df = merge_sheets_in_excel_file(df)
    # print(merged_df)
    # Start the dashboard configuration with the data frame
    dashboard_config()



def create_visualizations(fig1,fig2,fig3, fig4):
    """
    Create and display visualizations when data is available
    """
    # First row of visualizations
    left_col, right_col = st.columns(2)
    with left_col:
        st.plotly_chart(fig1, use_container_width=True)
    with right_col:
        st.plotly_chart(fig2, use_container_width=True)

    # Second row
    st.plotly_chart(fig3, use_container_width=True) 
    st.plotly_chart(fig4, use_container_width=True)     

def initialize_empty_df():
    """Initialize an empty DataFrame with predefined columns"""
    return pd.DataFrame({
        'TicketId': [],
        'date': [],
        'team': [],
        'Transferred From': [],
        'days': [],
        'hours': [],
        'minutes': [],
        'seconds': [],
        'wait_time': []
    })

def dashboard_config(main_data_frame=None,fig1=None,fig2=None,fig3=None):
               
    # Convert the birth_date column to age column for easier manipulations.
    # main_data_frame = convert_birth_date_to_age_column(main_data_frame)

    # Pass the data through the sidebar's filters. and get back the filtered data frame
    # filtered_data_frame = sidebar_config()

    # filtered_data_frame = main_data_frame

    # if (sidebar_config() is not None):
    #     filtered_data_frame = sidebar_config()

    # Convert the order date to format: dd/mm/yyyy
    # filtered_data_frame['order_date'] = filtered_data_frame['order_date'].dt.strftime('%m/%d/%Y')

    # The top row kpi(avg, total and  amount of  transactions), plus add the 'total' column to the data frame
    # top_row_kpi(filtered_data_frame)

    # Display the table data frame
    # if main_data_frame is not None:
    #   st.dataframe(main_data_frame, use_container_width=True, hide_index=True)
    #   column_options = main_data_frame['team']
      
    # else:
        
    #   df = pd.DataFrame({
    #     'TicketId': [],
    #     'date': [],
    #     'team': [],
    #     'Transferred From': [],
    #     'days': [],
    #     'hours': [],
    #     'minutes': [],
    #     'seconds': [],
    #     'wait_time': []

    # })
    #   st.dataframe(df, use_container_width=True, hide_index=True)
    #   column_options = []
      

    # Create the charts from the filtered data_frame
    # pie_chart, horizontal_bar, grouped_bar, scatter_plot = create_charts(filtered_data_frame)

    # Create a Divider under the main table
    

    # Create the first row containing the pie chart and the horizontal bar chart. the row divided to two columns
    # left_col, right_col = st.columns(2)
    # with left_col:
    #     st.plotly_chart(pie_chart)
    # with right_col:
    #     st.plotly_chart(horizontal_bar)

    # Create the second row containing the grouped bar chart and the scatter plot.the row divided to two columns
    # left_col, right_col = st.columns(2)
    # with left_col:
    #     st.plotly_chart(grouped_bar)
    # with right_col:
    #     st.plotly_chart(scatter_plot)

    filtered_df = create_sidebar_filters()
    header()
    summary_container = st.container()
    data_container = st.container()
    viz_container = st.container()
    
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
        st.session_state.filtered_data = None
    
    # Update session state when new data arrives
    if main_data_frame is not None and not main_data_frame.empty:
        st.session_state.data_loaded = True  
        st.session_state.current_data = main_data_frame
              
    elif 'current_data' not in st.session_state:
        st.session_state.current_data = initialize_empty_df()
    # Fill containers based on data state

    with summary_container:
        if st.session_state.data_loaded and filtered_df is not None:
            create_summary_section(filtered_df)
        else :    
            create_summary_section(st.session_state.current_data)
    
    with data_container:
        st.markdown("### data")
        if st.session_state.data_loaded:
            if 'filtered_data' in st.session_state and st.session_state.filtered_data is not None:
                filtered_df['wait_time'] = filtered_df['wait_time'].astype(int)
                st.session_state.filtered_data = filtered_df
                st.dataframe(st.session_state.filtered_data, use_container_width=True, hide_index=True)
            else:
                main_data_frame['wait_time'] = main_data_frame['wait_time'].astype(int)
                st.dataframe(main_data_frame, use_container_width=True, hide_index=True)
        else:
            st.dataframe(initialize_empty_df(), use_container_width=True, hide_index=True)
            st.info("Waiting for data to be loaded...")

    with viz_container:
        if st.session_state.data_loaded and 'current_data' in st.session_state and st.session_state.current_data is not None:
            # Create visualizations based on filtered data
            if 'filtered_data' in st.session_state and st.session_state.filtered_data is not None:
                data = st.session_state.filtered_data
            else :
                data = st.session_state.current_data    
            total_wait_time_per_team = data.groupby('team')['wait_time'].sum().reset_index()
            average_wait_time_per_team = data.groupby('team')['wait_time'].mean().reset_index()
            entries_per_team = data['team'].unique()
            entries_per_team = data['team'].value_counts().reset_index()
            entries_per_team.columns = ['team', 'count']
            fig1 = px.pie(average_wait_time_per_team, values='wait_time', names='team')
            fig2 = px.bar(st.session_state.current_data, x='team', y='wait_time')
            fig3 = px.scatter(st.session_state.current_data, x='date', y='wait_time', color='team')
            fig4 = px.bar(entries_per_team, x='team', y='count',
                          title='Number of Entries per Team',labels={'count': 'Number of Entries', 'team': 'Team'})
            create_visualizations(fig1, fig2, fig3, fig4)


def header():
    """
    Display the header of the sales dashboard.

    Returns:
        None
    """
    st.markdown("""
    <style>
    .header-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 30px;

    }
    .compact-title {
        font-size: 24px;
        margin: 0;
        padding: 0;
    }
    .stImage {
        margin: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create header container with flex layout
    st.markdown("""
    <div class="header-container">
        <img src="https://www.link3.net/assets/img/logo-dark.png" width="80" style="margin-right: 15px;">
        <h1 class="compact-title">Ticket Parser & Analytics</h1>
    </div>
    """, unsafe_allow_html=True)

def main():
    # projection = ['full_name', 'age', 'gender', 'item_name', 'category', 'item_tags', 'season', 'printing', 'price', 'amount', 'order_date']
    init_dashboard()


if __name__ == '__main__':
    main()    
