import streamlit as st
import pandas as pd



def sidebar_config(data_frame):
    """
       Configure the sidebar for filtering options and generate a filtered DataFrame.

       Args:
           data_frame (pd.DataFrame): The original DataFrame containing the data.

       Returns:
           pd.DataFrame: The filtered DataFrame based on the sidebar selections.
       """
    # Set the sidebar's header
    st.sidebar.header('Please Filter Here:')

    # Get the inputs from the selects and checkboxes
    full_name, item_name, category, printing = init_sidebar_selects(data_frame)

    male_check, female_check, winter_check, summer_check = init_sidebar_checkboxes()
    # A divider
    st.sidebar.markdown('---')

    # Get the input from the date inputs
    start_date, end_date = init_sidebar_dates_pickers(data_frame)

    # Get the values from the checkboxes item tags and season
    item_tags, season = get_value_from_checkbox_sidebar(male_check, female_check, winter_check, summer_check)

    # Initiate the queries for the filtering
    queries_dict = init_selects_queries_dict()

    # The prefix of the query made of the inputs that can't be null
    prefix_query = f'item_tags.isin(@item_tags) and @start_date <= order_date <= @end_date and season.isin(@season)'

    # Build the query from the selected values
    select_query: str = build_final_query_string(full_name, item_name, category, printing, queries_dict)

    # Check if select_query is null means no values were selected in the selects box the filter by the basic filters
    # else select_query is not null then add the selected query to the prefix one
    df_selections = data_frame.query(f'{select_query} and {prefix_query}') if select_query else data_frame.query(f'{prefix_query}')
    return df_selections


def init_selects_queries_dict():
    """
        Initialize a dictionary of queries for select options.

        Returns:
            dict: A dictionary containing the queries for select options.
        """
    queries = {}
    queries['item_name_query'] = ' item_name == @item_name '
    queries['client_name_query'] = ' full_name == @full_name '
    queries['printing_query'] = ' printing == @printing '
    queries['category_query'] = ' category == @category '
    return queries


def build_final_query_string(full_name, item_name, category, printing, queries_dict):
    """
    Build the final query string based on the selected values.

    Args:
        full_name (list): The selected client names.
        item_name (list): The selected item names.
        category (list): The selected categories.
        printing (list): The selected printing options.
        queries_dict (dict): The dictionary of queries for select options.

    Returns:
        str: The final query string.
    """
    conditions = []
    if full_name:
        conditions.append(queries_dict['client_name_query'])
    if item_name:
        conditions.append(queries_dict['item_name_query'])
    if category:
        conditions.append(queries_dict['category_query'])
    if printing:
        conditions.append(queries_dict['printing_query'])
    conditions_query = ' and '.join(conditions)
    return conditions_query


def init_sidebar_selects(data_frame):
    """
        Initialize the sidebar select options.

        Args:
            data_frame (pd.DataFrame): The original DataFrame containing the data.

        Returns:
            tuple: The selected client names, item names, categories, and printing options.
        """
    full_name = st.sidebar.multiselect(
        'Select the client name:',
        options=data_frame['full_name'].unique(),
    )

    item_name = st.sidebar.multiselect(
        'Select a specific item:',
        options=data_frame['item_name'].unique()
    )
    printing = st.sidebar.multiselect(
        'Select the Texture:',
        options=data_frame['printing'].unique(),
    )
    category = st.sidebar.multiselect(
        'Select the category:',
        options=data_frame['category'].unique(),
    )
    return full_name, item_name, category, printing


def init_sidebar_checkboxes():
    """
        Initialize the sidebar checkboxes.

        Returns:
            tuple: The selected checkbox values.
        """
    st.sidebar.header('Item Tag:')
    male_check = st.sidebar.checkbox('Male', value=True)
    female_check = st.sidebar.checkbox('Female', value=True)

    st.sidebar.header('Select a Season:')
    winter_check = st.sidebar.checkbox('fall/winter', value=True)
    summer_check = st.sidebar.checkbox('spring/summer', value=True)
    return male_check, female_check, winter_check, summer_check


def init_sidebar_dates_pickers(data_frame):
    """
        Initialize the sidebar date pickers.

        Args:
            data_frame (pd.DataFrame): The original DataFrame containing the data.

        Returns:
            tuple: The selected start and end dates.
        """
    data_frame['order_date'] = pd.to_datetime(data_frame['order_date'])
    min_date = pd.to_datetime(data_frame['order_date']).min()
    max_date = pd.to_datetime(data_frame['order_date']).max()

    start_date = st.sidebar.date_input('Start date', value=min_date)
    end_date = st.sidebar.date_input('End date', value=max_date)
    return start_date, end_date


def get_value_from_checkbox_sidebar(male_check, female_check, winter_check, summer_check):
    """
       Get the values from the checkbox sidebar.

       Args:
           male_check (bool): The value of the Male checkbox.
           female_check (bool): The value of the Female checkbox.
           winter_check (bool): The value of the winter checkbox.
           summer_check (bool): The value of the summer checkbox.

       Returns:
           tuple: The selected item tags and season values.
       """
    item_tags = []
    season = []

    if male_check:
        item_tags.append('male')
    if female_check:
        item_tags.append('female')
    if winter_check:
        season.append('fall/winter')
    if summer_check:
        season.append('spring/summer')
    return item_tags, season
