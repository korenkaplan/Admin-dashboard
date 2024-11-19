import streamlit as st
import pandas as pd



def sidebar_config(dataFrame,column):
       
    st.sidebar.header("Filters")
    selected_values, filtered_df = create_filter_widgets(dataFrame, column)
    return selected_values, filtered_df


def create_filter_widgets(df: pd.DataFrame, column: str) -> tuple:
    """
    Create filter widgets for DataFrame
    
    Parameters:
    df (pd.DataFrame): DataFrame to filter
    column (str): Column name to filter on
    
    Returns:
    tuple: Selected filter values and filtered DataFrame
    """
    # Get unique values from the column
    if df is not None:
      unique_values = sorted(df[column].unique())
    
    # Create filter container
    with st.container():
        st.write(f"Filter by {column}")
        
        # Create filter type selector
        filter_type = st.radio(
            "Filter type",
            ["Single Select", "Multi Select"],
            horizontal=True,
            key=f"filter_type_{column}"
        )
        
        if filter_type == "Single Select":
            # Add "All" option for single select
            options = ["All"] + list(unique_values)
            selected = st.selectbox(
                f"Select {column}",
                options,
                key=f"select_{column}"
            )
            
            # Filter DataFrame
            if selected == "All":
                filtered_df = df
            else:
                filtered_df = df[df[column] == selected]
                
        else:  # Multi Select
            selected = st.multiselect(
                f"Select {column}(s)",
                unique_values,
                default=unique_values,
                key=f"multiselect_{column}"
            )
            
            # Filter DataFrame
            if df is not None:
              filtered_df = df[df[column].isin(selected)] if selected else df






