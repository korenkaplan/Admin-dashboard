import streamlit as st
import pandas as pd
import os
import numpy as np
import datetime
import time
import re
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from datetime import datetime, timedelta, date
import plotly.express as px
import random
from pathlib import Path

excel_file_url1 = r'Excel_file_to_upload/ComplainReport13112024.xlsx'
excel_file_url = r'Excel_file_to_upload/Python_Scan_and_Gos_sales_analytics_2022.xlsx'
recentFile= None
parsedDf = None
selected_column= None
#st.config.set_option('server.maxUploadSize', 1024)
os.environ['STREAMLIT_SERVER_MAX_UPLOAD_SIZE'] = '1024' 

# Add an on-change event handler
def on_change():
     

    # st.write(f"You selected the '{st.session_state['selected_teams']}' column.")
    # with st.expander("Additional Dashboard Section"):        
    #     FilterData(st.session_state['selected_teams'])
    return None      


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
            
            return parsed_df,fig1, fig2, fig3


def concat_dataframes_with_columns(df1, df2, columns_to_merge):    
    # Select specified columns from both DataFrames
    selected_df1 = df1[columns_to_merge]
    selected_df2 = df2[columns_to_merge]
    
    # Concatenate vertically while preserving original data
    merged_df = pd.concat([selected_df1, selected_df2], ignore_index=True)
    
    return merged_df   


def extractMisData():        
        if 'uploaded_file_mis' in st.session_state and st.session_state.uploaded_file_mis is not None:
          file = st.session_state['uploaded_file_mis']
        extension = Path(file.name).suffix  
        df_mis = None
        if file is not None: 
           with st.spinner('please Wait for data...'):          
             time.sleep(1) 
             # if extension == '.xlsx':
                # df_mis = pd.read_excel(file)
             # elif extension == '.xls':
                # converted_path = xls_to_xlsx(file)
                # df_mis = pd.read_excel(converted_path)
             try: 
                df_mis = pd.read_excel(file,engine='openpyxl')

             except Exception as e :
                raise st.warning("Inavalid File, please upload required valid files!")    
             if df_mis is not None : 
                # df_mis['Ticket Generate Date & Time'] = df_mis['Ticket Generate Date & Time'].apply(custom_datetime_parser)   
                st.session_state.df_mis = df_mis
                st.success('File Uploaded Successfully', icon="✅")                
             if ('df_mis' in st.session_state and st.session_state.df_mis is not None) and ('df_rsm' in st.session_state and st.session_state.df_rsm is not None) :                        
                print("working MIS")
                #    dashboard_config(df_mis)        
                st.success('File Uploaded Successfully', icon="✅")                                                   
        else :
            with st.spinner('please Wait for data...'):          
             time.sleep(1)          
            st.warning("please upload required valid files!")                     
        return None


def extractRsmData():
        if 'uploaded_file_rsm' in st.session_state and st.session_state.uploaded_file_rsm is not None:
           file = st.session_state['uploaded_file_rsm']
        extension = Path(file.name).suffix  
        df_rsm = None
        if file is not None:  
           with st.spinner('please Wait for data...'):          
             time.sleep(1) 
             # if extension == '.xlsx':
                # df_rsm = pd.read_excel(file)
             # elif extension == '.xls':
                # converted_path = xls_to_xlsx(file)
                # df_rsm = pd.read_html(file)
             try :    
                df_rsm = pd.read_excel(file, engine='openpyxl')   
                df_rsm = df_rsm.rename(columns={
                            'SL/NO': 'S/N',
                            'RefNO': 'Ticket ID',
                            'Customer Name': 'Client Name',
                            'Complain Source': 'Source Of Info',
                            'Task Category': 'Opening Category',
                            'Task Nature': 'Opening Nature',
                            'Receive Date': 'Ticket Generate Date & Time',
                            'Description': 'Comments',
                            'Area': 'Area',
                            'Support Office': 'Support Office',
                            'Support Type': 'Support Type',
                            'Complete By': 'Closed By',
                            'Status': 'Status',
                            'Customer ID': 'Client Id',
                            'BTS': 'BTS Name',
                            'Last Comments': 'Last Comments',
                            'Closing Nature': 'Close Category',
                            'Complete Date': 'Solved Date',
                            'OLT': 'OLT Name',
                            'BRAS': 'BRAS'

                        })
                df_rsm['Distributor Name'] = df_rsm['BRAS']
                df_rsm['Delay Reason']= df_rsm['OLT Name'] 
                df_rsm['Total Down Time(Minute)']= [random.randint(1, 100) for _ in range(len(df_rsm))]
                df_rsm['Commission Rate']= [random.randint(1, 100) for _ in range(len(df_rsm))]

             except Exception as e :
                st.warning('Invalid file, please upload valid file')   
             if df_rsm is not None :
                st.session_state.df_rsm = df_rsm  
                st.success('File Uploaded Successfully', icon="✅")           
             if ('df_mis' in st.session_state and st.session_state.df_mis is not None) and ('df_rsm' in st.session_state and st.session_state.df_rsm is not None) :                                                   
                columns_to_merge = ['S/N','Ticket ID','Client Name','Source Of Info','Opening Category',
                                       'Opening Nature','Ticket Generate Date & Time','Comments','Area','Support Office',
                                       'Support Type','Closed By','Status','Client Id','BTS Name','Last Comments','Close Category',
                                       'Solved Date','OLT Name','BRAS']
                merged_df = concat_dataframes_with_columns(st.session_state.df_mis,st.session_state.df_rsm,columns_to_merge)
                #st.dataframe(merged_df, use_container_width=True, hide_index=True)     
             else : 
                st.warning("please upload required valid files!")                                            
        else :
            with st.spinner('please Wait for data...'):          
             time.sleep(1)          
            st.warning("please upload required valid files!")                      
        return None  

def custom_datetime_parser(dt):
    """
    Custom function to swap month and day in datetime object
    
    Args:
        dt (datetime): Input datetime object
    
    Returns:
        datetime: Parsed datetime object with swapped month and day
    """
    try:
        # Extract year, month, day
        year = dt.year
        month = dt.month
        day = dt.day
        
        # Swap month and day
        new_datetime = pd.Timestamp(year=year, month=day, day=month, 
                                    hour=dt.hour, 
                                    minute=dt.minute, 
                                    second=dt.second)
        
        return new_datetime
    
    except Exception as e:
        print(f"Error parsing {dt}: {e}")
        return pd.NaT

def create_sidebar_filters(flag):
    """Create and manage all sidebar filters"""
    filter_container = st.container()
    with filter_container:
        st.markdown("Dashboard Filters")
        df = None
        if ((flag=='MIS') and 'df_mis' in st.session_state and st.session_state.df_mis is not None):
            with st.expander("Advanced data filter panel", expanded=True):
                # if ('selected_bts' not in st.session_state and 'down_time_range' not in st.session_state
                # and 'selected_area' not in st.session_state and 'selected_bras' not in st.session_state
                # and 'selected_office' not in st.session_state and 'date_range' not in st.session_state
                # and 'time_range_mis' not in st.session_state) :
                #     st.session_state['selected_bts'] = []
                #     st.session_state.selected_office = []
                #     st.session_state.selected_categories = []
                #     st.session_state.selected_olts = []
                #     st.session_state.selected_area = []
                #     st.session_state.selected_bras = []
                #     st.session_state.selected_olts = []
                #     st.session_state.down_time_range = float(0),float(100)
                #     st.session_state.date_range = None
                col_main_1, col_main_2, col_main_3 = st.columns(3)
                df = st.session_state.df_mis
                filtered_df = None
                min_date = None
                max_date = None
                max_hours_mis = None
                # df['Ticket Generate Date & Time'] = df['Ticket Generate Date & Time'].str.strip()
                if 'date_range' not in st.session_state:
                    df['Ticket Generate Date & Time'] = df['Ticket Generate Date & Time'].apply(custom_datetime_parser)                                              
                    st.session_state.df_mis = df
                    min_date = df['Ticket Generate Date & Time'].dt.date.min()
                    max_date = df['Ticket Generate Date & Time'].dt.date.max()                
                    max_hours_mis = (max_date - min_date).total_seconds() / 3600 
                    st.session_state.date_range = (min_date, max_date)
                    st.session_state.time_range_mis = (0,max_hours_mis)
                                    
                # df['Ticket Generate Date & Time'] = df['Ticket Generate Date & Time'].dt.strftime('%d-%m-%y')
                # print(df['Ticket Generate Date & Time'])
                # print(f"printing {min_date}, {max_date}") 
                min_date = df['Ticket Generate Date & Time'].dt.date.min()
                max_date = df['Ticket Generate Date & Time'].dt.date.max()                
                max_hours_mis = (max_date - min_date).total_seconds() / 3600 
                with col_main_1:                    
                    all_c_category = df['Client Category'].unique()
                    selected_categories = st.multiselect(
                        "Select Client Category",
                        options=all_c_category,
                        # default=all_c_category,
                        on_change=on_change,
                        key='selected_categories'
                    )                   
                with col_main_2:
                  try: 
                        date_range = st.date_input(
                            "Select Custom Date Range",
                            value=(
                                st.session_state.get('date_range', [min_date, max_date])
                            ),
                            on_change=on_change,
                            min_value=min_date,
                            max_value=max_date,
                            key='date_range'
                        )                       
                  except Exception as e:
                        print("inside exception")
                        print(e)
                        print(f"  {min_date} ,, {max_date}")
                        print(st.session_state.date_range)
                                   
                   
                with col_main_3:
                    all_bts = df['BTS Name'].unique()
                    selected_bts = st.multiselect(
                        "Select BTS",
                        options=all_bts,
                        # default=["All"],
                        on_change=on_change,
                        key='selected_bts'
                    )                     
                # st.markdown("### Filter With Date Range")
                # min_date = df['Ticket Generate Date & Time'].dt.date.min()
                # max_date = df['Ticket Generate Date & Time'].dt.date.max()
                # total_days = (max_date - min_date).days
                # # min_wait = float(df['wait_time'].min())
                # # max_wait = float(df['wait_time'].max())
                # date_range_slider = st.slider(
                #     "Select Date Range (days)",
                #     min_value=0,
                #     max_value=total_days,
                #     value=(0, total_days),
                #     step=1,
                #     key='date_time_slider_range'
                # )
                # start_date = min_date + timedelta(days=date_range_slider[0])
                # end_date = min_date + timedelta(days=date_range_slider[1])

                # Add a reset filters button
                col_main_4, col_main_5, col_main_6 = st.columns(3)
                with col_main_4:
                    all_support_office = df['Support Office'].unique()
                    selected_office = st.multiselect(
                        "Select Support Office",
                        options=all_support_office,
                        # default=all_support_office,
                        on_change=on_change,
                        key='selected_office'
                    )   
                   
                with col_main_5: 
                    all_bras = df['BRAS'].unique()
                    selected_bras = st.multiselect(
                        "Select BRAS",
                        options=all_bras,
                        # default=all_bras,
                        on_change=on_change,
                        key='selected_bras'
                    ) 
                
                with col_main_6:
                    all_areas = df['Area'].unique()
                    selected_area = st.multiselect(
                        "Select Area",
                        options=all_areas,
                        # default=all_areas,
                        on_change=on_change,
                        key='selected_area'
                    )  
                col_main_7, col_main_8 = st.columns([3,2])  
                with col_main_7: 
                    # min_date = df['Ticket Generate Date & Time'].dt.date.min()
                    # max_date = df['Ticket Generate Date & Time'].dt.date.max()
                    # min_wait = float(df['wait_time'].min())
                    # max_wait = float(df['wait_time'].max())
                    min_time = float(df['Total Down Time(Minute)'].min())
                    max_time = float(df['Total Down Time(Minute)'].max())
                    wait_time_range = st.slider(
                        "Select down Time Range (Minutes)",
                        min_value=min_time,
                        max_value=max_time,
                        value=(min_time, max_time),
                        key='down_time_range'
                    ) 
                # with col_main_8: 
                #     if st.button('Reset All Filters'):            
                #         st.session_state['selected_bts'] = []
                #         st.session_state.selected_office = None
                #         st.session_state.selected_categories = None
                #         st.session_state.selected_olts = None
                #         st.session_state.selected_area = None
                #         st.session_state.selected_bras = None
                #         st.session_state.selected_olts = None
                #         st.session_state.down_time_range = (min_time, max_time)
                #         st.session_state.date_range = [min_date, max_date]
                #         st.rerun() 

                min_time = float(0)
                max_time = max_hours_mis
                wait_time_range = st.slider(
                        "Select Time Range (Hours)",
                        min_value=min_time,
                        max_value=max_time,
                        value=(min_time, max_time),
                        key='time_range_mis'
                    )         
          
                # Apply filters
                filtered_df = apply_filters(df,'MIS')
                st.session_state.filtered_data = filtered_df
                if filtered_df is not None:
                    st.info(f"Showing {len(filtered_df)} of {len(df)} records")

        elif(flag=='RSM' and 'df_rsm' in st.session_state and st.session_state.df_rsm is not None):            
            with st.expander("Advanced data filter panel", expanded=True):
                col_main_1, col_main_2, col_main_3, col_main_4  = st.columns(4)
                df = st.session_state.df_rsm
                filtered_df = None    
                min_date_rsm = None  
                max_date_rsm = None  
                max_hours_rsm = float(24)                           
                if 'date_range_rsm' not in st.session_state:                    
                   df['Ticket Generate Date & Time'] = df['Ticket Generate Date & Time'].apply(custom_datetime_parser)                                              
                   st.session_state.df_rsm = df
                   min_date_rsm = df['Ticket Generate Date & Time'].dt.date.min()
                   max_date_rsm = df['Ticket Generate Date & Time'].dt.date.max()                
                   max_hours_rsm = (max_date_rsm - min_date_rsm).total_seconds() / 3600                    
                   st.session_state.date_range_rsm = (min_date_rsm,max_date_rsm) 
                   st.session_state.time_range = (0,max_hours_rsm) 
                   if int(max_hours_rsm) >= 0 and int(max_hours_rsm) <1 :
                      max_hours_rsm = float(24) 
                      st.session_state.time_range = (0,max_hours_rsm)   
                min_date_rsm = df['Ticket Generate Date & Time'].dt.date.min()
                max_date_rsm = df['Ticket Generate Date & Time'].dt.date.max()                
                max_hours_rsm = (max_date_rsm - min_date_rsm).total_seconds() / 3600     
                if int(max_hours_rsm) >= 0 and int(max_hours_rsm) <1 :
                      max_hours_rsm = float(24)                          
                with col_main_1:                    
                    # Apply filters
                    all_teams = df['Team Name'].unique()
                    selected_bts = st.multiselect(
                        "Select Teams",
                        options=all_teams,
                        # default=["All"],
                        on_change=on_change,
                        key='selected_teams_rsm'
                    )  
                                  
                with col_main_2:
                    date_range = st.date_input(
                        "Select Custom Date Range",
                        value=(
                            st.session_state.get('date_range_rsm', [min_date_rsm, max_date_rsm])
                        ),
                        min_value=min_date_rsm,
                        max_value=max_date_rsm,
                        key='date_range_rsm'
                    )                   
                   
                with col_main_3:
                    all_bts = df['BTS Name'].unique()
                    selected_bts = st.multiselect(
                        "Select BTS",
                        options=all_bts,
                        # default=["All"],
                        on_change=on_change,
                        key='selected_bts_rsm'
                    )  
                with col_main_4 :                    
                    all_status = df['Status'].unique()
                    selected_area = st.multiselect(
                        "Select Status",
                        options=all_status,
                        # default=all_areas,
                        on_change=on_change,
                        key='selected_status_rsm'
                    )                        
                # st.markdown("### Filter With Date Range")
                # min_date = df['Ticket Generate Date & Time'].dt.date.min()
                # max_date = df['Ticket Generate Date & Time'].dt.date.max()
                # total_days = (max_date - min_date).days
                # # min_wait = float(df['wait_time'].min())
                # # max_wait = float(df['wait_time'].max())
                # date_range_slider = st.slider(
                #     "Select Date Range (days)",
                #     min_value=0,
                #     max_value=total_days,
                #     value=(0, total_days),
                #     step=1,
                #     key='date_time_slider_range'
                # )
                # start_date = min_date + timedelta(days=date_range_slider[0])
                # end_date = min_date + timedelta(days=date_range_slider[1])

                # Add a reset filters button
                col_main_5, col_main_6, col_main_7, col_main_8 = st.columns(4)
                with col_main_5:
                    all_support_office = df['Support Office'].unique()
                    selected_office = st.multiselect(
                        "Select Support Office",
                        options=all_support_office,
                        # default=all_support_office,
                        on_change=on_change,
                        key='selected_office_rsm'
                    )   
                   
                with col_main_6: 
                    all_task_nature = df['Opening Nature'].unique()
                    selected_bras = st.multiselect(
                        "Select Task Nature",
                        options=all_task_nature,
                        # default=all_bras,
                        on_change=on_change,
                        key='selected_task_nature_rsm'
                    ) 
                
                with col_main_7:
                    all_areas = df['Area'].unique()
                    selected_area = st.multiselect(
                        "Select Area",
                        options=all_areas,
                        # default=all_areas,
                        on_change=on_change,
                        key='selected_area_rsm'
                    )  
                with col_main_8:
                    all_com_sources = df['Source Of Info'].unique()
                    selected_area = st.multiselect(
                        "Select complain sources",
                        options=all_com_sources,
                        # default=all_areas,
                        on_change=on_change,
                        key='selected_com_sources_rsm'
                    )                         
                col_main_9, col_main_10, col_main_11, col_main_12 = st.columns(4)

                with col_main_9:
                    all_close_categories = df['Close Category'].unique()
                    selected_area = st.multiselect(
                        "Select close categories",
                        options=all_close_categories,
                        # default=all_areas,
                        on_change=on_change,
                        key='selected_close_categories_rsm'
                    ) 
                with col_main_10:
                    all_support_types = df['Support Type'].unique()
                    selected_area = st.multiselect(
                        "Select support types",
                        options=all_support_types,
                        # default=all_areas,
                        on_change=on_change,
                        key='selected_support_types_rsm'
                    )  

                with col_main_11:
                    all_task_categories = df['Opening Category'].unique()
                    selected_bts = st.multiselect(
                        "Select task categories",
                        options=all_task_categories,
                        # default=["All"],
                        on_change=on_change,
                        key='selected_task_categories_rsm'
                    )  
                # with col_main_12:
                #     # if st.button('Reset All Filters'):            
                #     #     # st.session_state.selected_support_types_rsm = list(all_support_types)
                #     #     # st.session_state.selected_office_rsm = list(all_support_office)
                #     #     # st.session_state.selected_task_categories_rsm = list(all_task_categories)
                #     #     # st.session_state.selected_support_types_rsm = list(all_support_types)
                #     #     # st.session_state.selected_area_rsm = list(all_areas)
                #     #     # st.session_state.selected_close_categories_rsm = list(all_close_categories)
                #     #     # st.session_state.down_time_range = (min_time, max_time)
                #     #     # st.session_state.date_range = [min_date, max_date]
                #     #     # st.experimental_rerun()  
                #     # # min_date = df['Ticket Generate Date & Time'].dt.date.min()
                #     # # max_date = df['Ticket Generate Date & Time'].dt.date.max()
                #     # # min_wait = float(df['wait_time'].min())
                #     # # max_wait = float(df['wait_time'].max())
                min_time_rsm = float(0)
                max_time_rsm = max_hours_rsm
                wait_time_range = st.slider(
                        "Select Time Range (Minutes)",
                        min_value=min_time_rsm,
                        max_value=max_time_rsm,
                        value=(min_time_rsm, max_time_rsm),
                        key='time_range'
                    )         

                filtered_df = apply_filters(df,'RSM')
                st.session_state.filtered_data = filtered_df
                if filtered_df is not None:
                    st.info(f"Showing {len(filtered_df)} of {len(df)} records")                                                           
        else :
            st.info("Please upload data to enable filters")
            return          

        return filtered_df


def apply_filters(df,flag):
    """Apply all filters to the dataframe based on sidebar selections"""
    if df is None or df.empty:
        return None
    filtered_df = None
    if(flag=='MIS'): 
        filtered_df = df.copy()    
        # Convert date column to datetime if it's not already        
        # Apply date range filter
        if 'date_range' in st.session_state and st.session_state.date_range is not None:           
            count = len(st.session_state.date_range)            
            if count>=2:
                start_date, end_date = st.session_state.date_range
                max_hours = (end_date - start_date).total_seconds() / 3600
                print(f"{filtered_df['Ticket Generate Date & Time'].dt.date}")
                print(f"printing {start_date}  {end_date}")
                st.session_state.time_range = (float(0),max_hours)
                filtered_df = filtered_df[
                    (filtered_df['Ticket Generate Date & Time'].dt.date >= start_date) & 
                    (filtered_df['Ticket Generate Date & Time'].dt.date <= end_date)
                    
                ]
            else:
                filter_date = st.session_state.date_range[0]
                print(f"printing filter {filter_date} ")
                st.session_state.time_range = (float(0),float(24))
                filtered_df = filtered_df[
                    (filtered_df['Ticket Generate Date & Time'].dt.date >= filter_date) & 
                    (filtered_df['Ticket Generate Date & Time'].dt.date <= filter_date)
                            
                ]                                  
        

        # Apply team filter
        if 'selected_selected_bts' in st.session_state and st.session_state.selected_selected_bts:
            filtered_df = filtered_df[filtered_df['BTS Name'].isin(st.session_state.selected_selected_bts)]

        # Apply team filter
        if 'selected_office' in st.session_state and st.session_state.selected_office:
            filtered_df = filtered_df[filtered_df['Support Office'].isin(st.session_state.selected_office)]


        # Apply team filter
        if 'selected_olts' in st.session_state and st.session_state.selected_olts:
            filtered_df = filtered_df[filtered_df['OLT Name'].isin(st.session_state.selected_olts)]

        # Apply team filter
        if 'selected_categories' in st.session_state and st.session_state.selected_categories:
            filtered_df = filtered_df[filtered_df['Client Category'].isin(st.session_state.selected_categories)]  

        if 'selected_area' in st.session_state and st.session_state.selected_area:
            filtered_df = filtered_df[filtered_df['Area'].isin(st.session_state.selected_area)]  

        
        if 'selected_bras' in st.session_state and st.session_state.selected_bras:
            filtered_df = filtered_df[filtered_df['BRAS'].isin(st.session_state.selected_bras)]   


        if 'time_range_mis' in st.session_state and st.session_state.time_range_mis:
            min_time, max_time = st.session_state.time_range_mis           
            filtered_df = filtered_df[
                (filtered_df['Ticket Generate Date & Time'].dt.hour >= min_time) & 
                (filtered_df['Ticket Generate Date & Time'].dt.hour <= max_time)
            ]                       

        # Apply wait time range filter
        # if 'wait_time_range' in st.session_state:
        #     min_wait, max_wait = st.session_state.wait_time_range
        #     filtered_df = filtered_df[
        #         (filtered_df['wait_time'] >= min_wait) & 
        #         (filtered_df['wait_time'] <= max_wait)
        #     ]
        

    elif(flag=='RSM'):  
        filtered_df = df.copy()
        
        # Convert date column to datetime if it's not already
        filtered_df['Ticket Generate Date & Time'] = pd.to_datetime(filtered_df['Ticket Generate Date & Time'])

        # Apply date range filter
        if 'date_range_rsm' in st.session_state and st.session_state.date_range_rsm is not None:  
            count = len(st.session_state.date_range_rsm)            
            if count>=2:
                start_date, end_date = st.session_state.date_range_rsm
                max_hours = (end_date - start_date).total_seconds() / 3600
                # st.session_state.time_range = (float(0),max_hours)
                filtered_df = filtered_df[
                    (filtered_df['Ticket Generate Date & Time'].dt.date >= start_date) & 
                    (filtered_df['Ticket Generate Date & Time'].dt.date <= end_date)
                   
                ]
            else:
                filter_date = st.session_state.date_range_rsm[0]
                #st.session_state.time_range = (float(0),float(24))
                filtered_df = filtered_df[
                        (filtered_df['Ticket Generate Date & Time'].dt.date >= filter_date) & 
                        (filtered_df['Ticket Generate Date & Time'].dt.date <= filter_date)
                        
                ]                                  

        # Apply team filter
        if 'selected_bts_rsm' in st.session_state and st.session_state.selected_bts_rsm:
            filtered_df = filtered_df[filtered_df['BTS Name'].isin(st.session_state.selected_bts_rsm)]

        # Apply team filter
        if 'selected_office_rsm' in st.session_state and st.session_state.selected_office_rsm:
            filtered_df = filtered_df[filtered_df['Support Office'].isin(st.session_state.selected_office_rsm)]


        # Apply team filter
        if 'selected_support_types_rsm' in st.session_state and st.session_state.selected_support_types_rsm:
            filtered_df = filtered_df[filtered_df['Support Type'].isin(st.session_state.selected_support_types_rsm)] 

        if 'selected_area_rsm' in st.session_state and st.session_state.selected_area_rsm:
            filtered_df = filtered_df[filtered_df['Area'].isin(st.session_state.selected_area_rsm)]  
       
        if 'selected_status_rsm' in st.session_state and st.session_state.selected_status_rsm:
            filtered_df = filtered_df[filtered_df['Status'].isin(st.session_state.selected_status_rsm)]

        if 'selected_task_categories_rsm' in st.session_state and st.session_state.selected_task_categories_rsm:
            filtered_df = filtered_df[filtered_df['Opening Category'].isin(st.session_state.selected_task_categories_rsm)]    

        if 'selected_task_nature_rsm' in st.session_state and st.session_state.selected_task_nature_rsm:
            filtered_df = filtered_df[filtered_df['Opening Nature'].isin(st.session_state.selected_task_nature_rsm)]  

        if 'selected_teams_rsm' in st.session_state and st.session_state.selected_teams_rsm:
            filtered_df = filtered_df[filtered_df['Team Name'].isin(st.session_state.selected_teams_rsm)]     

        if 'selected_close_categories_rsm' in st.session_state and st.session_state.selected_close_categories_rsm:
            filtered_df = filtered_df[filtered_df['Close Category'].isin(st.session_state.selected_close_categories_rsm)]  

        if 'selected_com_sources_rsm' in st.session_state and st.session_state.selected_com_sources_rsm:
            filtered_df = filtered_df[filtered_df['Source Of Info'].isin(st.session_state.selected_com_sources_rsm)]    

        if 'time_range' in st.session_state and st.session_state.time_range:
            min_time, max_time = st.session_state.time_range
            print(f"printing {st.session_state.time_range}")
            filtered_df = filtered_df[
                (filtered_df['Ticket Generate Date & Time'].dt.hour >= min_time) & 
                (filtered_df['Ticket Generate Date & Time'].dt.hour <= max_time)
            ]                          
        
        if filtered_df is not None :
            st.session_state.filtered_data_rsm = filtered_df

    return filtered_df

def create_summary_section(df):
    """
    Generate the summary section of the dashboard based on the provided DataFrame.
    """
    if df is None or df.empty:
        total_tickets = 0.00
        total_completed = 0.00
        total_pending = 0.00
        total_distributor = 0.00
        total_source = 0.00
        total_delay_reason = 0.00
        total_downtime = 0.00
        total_commission_rate = 0.00

    # Calculate summary metrics
    else:
        # df['wait_time'] = df['wait_time'].astype(int)
        total_tickets = len(df['Ticket ID'].unique())
        total_completed = len(df[df["Status"] == "Close"])
        total_pending = len(df[df["Status"] == "Pending"])
        total_distributor = len(df['Distributor Name'].unique())
        total_source = len(df['Source Of Info'].unique())
        total_delay_reason = len(df['Delay Reason'].unique())
        total_downtime = df['Total Down Time(Minute)'].sum()
        total_commission_rate = df['Commission Rate'].sum()
    
    # Define box styles
    colors = ["#4C5270", "#F652A0", "#36EEE0", "#059DC0","#4C5270", "#F652A0", "#36EEE0", "#059DC0"]
    box_styles = [
        {"background-color": colors[0], "color": "white", "font-size": "20px"},
        {"background-color": colors[1], "color": "white", "font-size": "20px"},
        {"background-color": colors[2], "color": "white", "font-size": "15px"},
        {"background-color": colors[3], "color": "white", "font-size": "15px"},
        {"background-color": colors[4], "color": "white", "font-size": "20px"},
        {"background-color": colors[5], "color": "white", "font-size": "20px"},
        {"background-color": colors[6], "color": "white", "font-size": "15px"},
        {"background-color": colors[7], "color": "white", "font-size": "15px"}
    ]

    # Define customer_info data
    customer_info = [
        {"top_text": "Total Tickets", "bottom_text": f"{total_tickets:,}"},
        {"top_text": "Total Completed", "bottom_text": f"{total_completed:,}"},
        {"top_text": "Total Pending", "bottom_text": f"{total_pending:,}"},
        {"top_text": "Total Distributor", "bottom_text": f"{total_distributor:,}"},
        {"top_text": "Total Dealy Reason", "bottom_text": f"{total_delay_reason:,}"},
        {"top_text": "Total Complaint Source", "bottom_text": f"{total_source:,}"},
        {"top_text": "Average Down Time", "bottom_text": f"{total_downtime:.2f} min"},
        {"top_text": "Average Commission Rate", "bottom_text": f"{total_commission_rate:.2f}"}
        
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
        st.markdown(f"</br>",unsafe_allow_html=True)

        customer_count_cols2 = st.columns(4)        
        for i in range(4):
            with customer_count_cols2[i]:
                st.markdown(
                    f"<div style='{'; '.join([f'{prop}: {value}' for prop, value in box_styles[i+4].items()])}; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; padding: 10px; margin: 0px; height: 100px;'>"
                    f"<div style='font-size: 14px;'>{customer_info[i+4]['top_text']}</div>"
                    f"<div style='font-size: 34px; font-weight: bold; text-align: center;'>{customer_info[i+4]['bottom_text']}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )    



def create_summary_section_RSM(df):
    """
    Generate the summary section of the dashboard based on the provided DataFrame.
    """
    if df is None or df.empty:
        total_tickets = 0.00
        total_completed = 0.00
        total_pending = 0.00
        total_source = 0.00

    # Calculate summary metrics
    else:
        # df['wait_time'] = df['wait_time'].astype(int)
        total_tickets = len(df['Ticket ID'].unique())
        total_completed = len(df[df["Status"] == "Complete"])
        total_pending = len(df[df["Status"] == "Incomplete"])
        total_source = len(df['Source Of Info'].unique())
    
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
        {"top_text": "Total Tickets", "bottom_text": f"{total_tickets:,}"},
        {"top_text": "Total Completed", "bottom_text": f"{total_completed:,}"},
        {"top_text": "Total Pending", "bottom_text": f"{total_pending:,}"},
        {"top_text": "Total Complaint Source", "bottom_text": f"{total_source:,}"}      
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
    with st.sidebar:
        with st.expander("Upload MIS File 📂", expanded=False):  # expanded=True means open by default
            mis_file = st.file_uploader(
                "Choose your file",
                type=['xlsx'],
                on_change=extractMisData,
                key='uploaded_file_mis'
            )

        with st.expander("Upload RSM File 📂", expanded=False):  # expanded=True means open by default
            rsm_file = st.file_uploader(
                "Choose your file",
                type=['xlsx'],
                on_change=extractRsmData,
                key='uploaded_file_rsm'
            )    
         
    # Merge all the sheets to a data frame
    # merged_df = merge_sheets_in_excel_file(df)
    # print(merged_df)
    # Start the dashboard configuration with the data frame
    dashboard_config()


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



def create_visualizations(fig1,fig2,fig3, fig4, fig5, fig6, fig7, fig8, fig9):
    """
    Create and display visualizations when data is available
    """
    # First row of visualizations
    left_col, right_col = st.columns(2)
    with left_col:
        st.plotly_chart(fig1, use_container_width=True)
    with right_col:
        st.plotly_chart(fig6, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)    
    # Second row
    left_col, right_col = st.columns(2)
    with left_col:
        st.plotly_chart(fig5, use_container_width=True)
    with right_col:
        st.plotly_chart(fig4, use_container_width=True)

    left_col, right_col = st.columns(2)
    with left_col:
        st.plotly_chart(fig3, use_container_width=True)
    with right_col:
        st.plotly_chart(fig7, use_container_width=True)    

    st.plotly_chart(fig8, use_container_width=True)
    st.plotly_chart(fig9, use_container_width=True)

# def initialize_empty_df():
#     """Initialize an empty DataFrame with predefined columns"""
#     return pd.DataFrame({
#         'TicketId': [],
#         'date': [],
#         'team': [],
#         'Transferred From': [],
#         'days': [],
#         'hours': [],
#         'minutes': [],
#         'seconds': [],
#         'wait_time': []
#     })


def create_visualizations_RSM(fig1,fig2,fig3, fig4, fig5, fig6, fig7, fig8):
    """
    Create and display visualizations when data is available
    """
    # First row of visualizations    
    st.plotly_chart(fig7, use_container_width=True,theme=None)    
    st.plotly_chart(fig1, use_container_width=True)  
    st.plotly_chart(fig8, use_container_width=True,theme=None)   
    st.plotly_chart(fig6, use_container_width=True)
    left_col, right_col = st.columns(2)
    with left_col:
        st.plotly_chart(fig5, use_container_width=True)
    with right_col:
        st.plotly_chart(fig4, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)    
    # Second row    
    st.plotly_chart(fig3, use_container_width=True)
    
# def initialize_empty_df():
#     """Initialize an empty DataFrame with predefined columns"""
#     return pd.DataFrame({
#         'TicketId': [],
#         'date': [],
#         'team': [],
#         'Transferred From': [],
#         'days': [],
#         'hours': [],
#         'minutes': [],
#         'seconds': [],
#         'wait_time': []
#     })
def create_duration_categories():
    """
    Generate duration categories from 30 minutes to 12 hours
    with incremental 1-hour intervals.
    """
    categories = [
        '0-30 mins',
        '30-60 mins',
        '1-2 hours',
        '2-3 hours',
        '3-4 hours',
        '4-5 hours',
        '5-6 hours',
        '6-7 hours',
        '7-8 hours',
        '8-9 hours',
        '9-10 hours',
        '10-11 hours',
        '11-12 hours',
        'More than 12 hours'
    ]
    
    # Create corresponding bin edges
    bins = [
        0, 30, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720, float('inf')
    ]
    
    return bins, categories

def mis_dashboard_content(main_data_frame: None):
        filtered_df = create_sidebar_filters('MIS')
        summary_container = st.container()
        data_container = st.container()
        viz_container = st.container()

           
        with summary_container:
            if st.session_state.df_mis is not None and filtered_df is not None:
                create_summary_section(filtered_df)
            else :    
                create_summary_section(st.session_state.df_mis)
        
        with data_container:
            st.markdown("### data")
            if st.session_state.df_mis is not None:
                if 'filtered_data_mis' in st.session_state and st.session_state.filtered_data_mis is not None:
                    # filtered_df['wait_time'] = filtered_df['wait_time'].astype(int)
                    st.session_state.filtered_data_mis = filtered_df
                    st.dataframe(st.session_state.filtered_data_mis, use_container_width=True, hide_index=True)
                else:
                    for col in st.session_state.df_mis.columns:
                            # Convert numpy integers to Python integers
                            if st.session_state.df_mis[col].dtype in [np.int64, np.int32]:
                                st.session_state.df_mis[col] = st.session_state.df_mis[col].astype(int)
                            # Convert numpy floats to Python floats
                            elif st.session_state.df_mis[col].dtype in [np.float64, np.float32]:
                                st.session_state.df_mis[col] = st.session_state.df_mis[col].astype(float)
                            # Convert any object types that might cause issues
                            elif st.session_state.df_mis[col].dtype == 'object':
                                st.session_state.df_mis[col] = st.session_state.df_mis[col].astype(str)
                    # main_data_frame['wait_time'] = main_data_frame['wait_time'].astype(int)
                    st.dataframe(st.session_state.df_mis, use_container_width=True, hide_index=True)
            else:
                st.info("Waiting for data to be loaded...")

        with viz_container:
            if  'df_mis' in st.session_state and st.session_state.df_mis is not None:
                # Create visualizations based on filtered data
                if 'filtered_data_mis' in st.session_state and st.session_state.filtered_data_mis is not None:
                    data = st.session_state.filtered_data_mis
                else :
                    data = st.session_state.df_mis   
                bins, categories = create_duration_categories()     
                total_down_time_bts = data.groupby('BTS Name')['Total Down Time(Minute)'].sum().reset_index()
                average_down_time_per_office = data.groupby('Support Office')['Total Down Time(Minute)'].mean().reset_index()
                entries_per_BTS = data['BTS Name'].unique()
                entries_per_BTS = data['BTS Name'].value_counts().reset_index()
                entries_per_BTS.columns = ['BTS Name', 'count']
                entries_per_status = data['Status'].unique()
                entries_per_status = data.groupby('Status')['Ticket ID'].count().reset_index()
                entries_per_status.columns = ['Status', 'count']
                entries_per_OLT = data['OLT Name'].unique()
                entries_per_OLT = data['OLT Name'].value_counts().reset_index()
                entries_per_OLT.columns = ['OLT Name', 'count']
                entries_per_BRAS = data['BRAS'].unique()
                entries_per_BRAS = data['BRAS'].value_counts().reset_index()
                entries_per_BRAS.columns = ['BRAS', 'count']

                entries_per_opening_nature = data['Opening Nature'].unique()
                entries_per_opening_nature = data['Opening Nature'].value_counts().reset_index()
                entries_per_opening_nature.columns = ['Opening Nature', 'count']

                entries_per_Closing_nature = data['Close Category'].unique()
                entries_per_Closing_nature = data['Close Category'].value_counts().reset_index()
                entries_per_Closing_nature.columns = ['Close Category', 'count']

                entries_per_client_category = data['Client Category'].unique()
                entries_per_client_category = data['Client Category'].value_counts().reset_index()
                entries_per_client_category.columns = ['Client Category', 'count']

                data['Duration Category'] = pd.cut(
                data['Total Down Time(Minute)'], 
                bins=bins,
                labels=categories
                )
                down_time_counts = data['Duration Category'].value_counts().sort_index()
        

                fig1 = px.bar(average_down_time_per_office, x='Total Down Time(Minute)', y='Support Office',title='Average Down Time Per Support Office')
                fig2 = px.bar(entries_per_OLT, x='OLT Name',y='count', color='OLT Name', title='Total Ticket Count Per OLT')
                fig3 = px.bar(entries_per_BRAS, x='BRAS', y='count', color='BRAS',title='Total Ticket Count Per BRAS')
                fig4 = px.bar( x=down_time_counts.index, y=down_time_counts.values,
                            title='Down time wise total Tickets',labels={'x': 'Duration', 'y': 'Number of Tickets'})
                fig5 = px.bar(entries_per_BTS, x='BTS Name', y='count',
                            title='Number of Entries per BTS',labels={'count': 'Number of Entries', 'BTS Name': 'BTS'})
                fig6 = px.pie(entries_per_status, names='Status', values='count',
                            title='Total Tickets Per Status',labels={'count': 'Number of Tickets', 'Status': 'Ticket Status'})  
                fig7 = px.bar(entries_per_opening_nature, x='Opening Nature', y='count',
                            title='Number of Entries per Opening Nature',labels={'count': 'Number of Entries', 'Opening Nature': 'Opening Nature'}) 
                fig8 = px.bar(entries_per_Closing_nature, x='Close Category', y='count',
                            title='Number of Entries per Close Category',labels={'count': 'Number of Entries', 'Close Category': 'Close Category'}) 
                fig9 = px.bar(entries_per_client_category, x='Client Category', y='count',
                            title='Number of Entries per Client Category',labels={'count': 'Number of Entries', 'Client Category': 'Client Category'})                                     
                                        
                create_visualizations(fig1, fig2, fig3, fig4, fig5, fig6,fig7, fig8, fig9)    

def rsm_dashboard_content(main_data_frame: None):
        filtered_df = create_sidebar_filters('RSM')
        summary_container = st.container()
        data_container = st.container()
        viz_container = st.container()
            
        with summary_container:
            if st.session_state.df_rsm is not None and filtered_df is not None:
                create_summary_section_RSM(filtered_df)
            else :    
                create_summary_section_RSM(st.session_state.df_rsm)
        
        with data_container:
            st.markdown("### data")
            if st.session_state.df_rsm is not None:
                if 'filtered_data_rsm' in st.session_state and st.session_state.filtered_data_rsm is not None:
                    # filtered_df['wait_time'] = filtered_df['wait_time'].astype(int)
                    st.session_state.filtered_data_rsm = filtered_df
                    st.dataframe(st.session_state.filtered_data_rsm, use_container_width=True, hide_index=True)
                else:
                    for col in st.session_state.df_rsm.columns:
                            # Convert numpy integers to Python integers
                            if st.session_state.df_rsm[col].dtype in [np.int64, np.int32]:
                                st.session_state.df_rsm[col] = st.session_state.df_rsm[col].astype(int)
                            # Convert numpy floats to Python floats
                            elif st.session_state.df_rsm[col].dtype in [np.float64, np.float32]:
                                st.session_state.df_rsm[col] = st.session_state.df_rsm[col].astype(float)
                            # Convert any object types that might cause issues
                            elif st.session_state.df_rsm[col].dtype == 'object':
                                st.session_state.df_rsm[col] = st.session_state.df_rsm[col].astype(str)
                    # main_data_frame['wait_time'] = main_data_frame['wait_time'].astype(int)
                    st.dataframe(st.session_state.df_rsm, use_container_width=True, hide_index=True)
            else:                
                st.info("Waiting for data to be loaded...")

        with viz_container:
            if 'df_rsm' in st.session_state and st.session_state.df_rsm is not None:
                # Create visualizations based on filtered data
                if 'filtered_data_rsm' in st.session_state and st.session_state.filtered_data_rsm is not None:
                    data = st.session_state.filtered_data_rsm
                else :
                    data = st.session_state.df_rsm                   
                entries_per_BTS = data['BTS Name'].unique()
                entries_per_BTS = data['BTS Name'].value_counts().reset_index()
                entries_per_BTS.columns = ['BTS Name', 'count']
                entries_per_status = data['Status'].unique()
                entries_per_status = data.groupby('Status')['Ticket ID'].count().reset_index()
                entries_per_status.columns = ['Status', 'count']
                entries_per_OLT = data['OLT Name'].unique()
                entries_per_OLT = data['OLT Name'].value_counts().reset_index()
                entries_per_OLT.columns = ['OLT Name', 'count']
                entries_per_BRAS = data['BRAS'].unique()
                entries_per_BRAS = data['BRAS'].value_counts().reset_index()
                entries_per_BRAS.columns = ['BRAS', 'count']

                entries_per_opening_nature = data['Opening Nature'].unique()
                entries_per_opening_nature = data['Opening Nature'].value_counts().reset_index()
                entries_per_opening_nature.columns = ['Opening Nature', 'count']

                entries_per_Closing_nature = data['Close Category'].unique()
                entries_per_Closing_nature = data['Close Category'].value_counts().reset_index()
                entries_per_Closing_nature.columns = ['Close Category', 'count']               
                
                fig1 = px.bar(entries_per_OLT, x='OLT Name',y='count', color='OLT Name', title='Total Ticket Count Per OLT')
                fig2 = px.bar(entries_per_BRAS, x='BRAS', y='count', color='BRAS',title='Total Ticket Count Per BRAS')
                fig3 = px.bar(entries_per_BTS, x='BTS Name', y='count',
                            title='Number of Entries per BTS',labels={'count': 'Number of Entries', 'BTS Name': 'BTS'})
                fig4 = px.pie(entries_per_status, names='Status', values='count',
                            title='Total Tickets Per Status',labels={'count': 'Number of Tickets', 'Status': 'Ticket Status'})  
                fig5 = px.bar(entries_per_opening_nature, x='Opening Nature', y='count',
                            title='Number of Entries per Opening Nature',labels={'count': 'Number of Entries', 'Opening Nature': 'Opening Nature'}) 
                fig6 = px.bar(entries_per_Closing_nature, x='Close Category', y='count',
                            title='Number of Entries per Close Category',labels={'count': 'Number of Entries', 'Close Category': 'Close Category'})  
                fig7 = px.bar(data, x='Source Of Info',y='Ticket ID',title='Number of Entries per Complain source', color='Status', 
                color_discrete_map={
                        'some_group': 'red',
                        'some_other_group': 'green'
                    }) 
                fig8 = px.bar(data, x='Team Name',y='Ticket ID',title='Number of Entries per Team', color='Status',barmode='group', 
                color_discrete_map={
                        'some_group': 'red',
                        'some_other_group': 'green'
                    })                                                        
                create_visualizations_RSM(fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8)  

def dashboard_config(main_data_frame=None,rsm_data_frame=None):
   
    header()
    mis, rsm = st.tabs(['MIS', 'RSM'])
    with mis :
        if 'df_mis' in st.session_state and st.session_state.df_mis is not None:
           mis_dashboard_content(st.session_state.df_mis)
        else :
           st.info('please upload MIS data file first')           
    with rsm :
        if 'df_rsm' in st.session_state and st.session_state.df_rsm is not None:
           rsm_dashboard_content(st.session_state.df_rsm)
        else :
           st.info('please upload RSM data file first') 
    # with both :
    #     st.write("Both - Coming Soon")    

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
        <h1 class="compact-title">Complaint Ticket Analytics</h1>
    </div>
    """, unsafe_allow_html=True)


def main():
    # projection = ['full_name', 'age', 'gender', 'item_name', 'category', 'item_tags', 'season', 'printing', 'price', 'amount', 'order_date']
    init_dashboard()


if __name__ == '__main__':
    main()

