import pandas as pd


def init_data(excel_file_path):
    """
    Initialize data from an Excel file.

    Args:
        excel_file_path (str): Path to the Excel file.

    Returns:
        dict: Dictionary containing all sheets from the Excel file, where
              the keys are the sheet names and the values are the corresponding
              data frames.
    """
    excel_file_path: str = excel_file_path

    # Read all sheets from Excel file, **sheet_name=None -> to read all sheets from the file
    all_sheets = pd.read_excel(excel_file_path, sheet_name=None)

    # Create a dictionary to store the sheets , dictionary comprehension
    sheet_dict = {sheet_name: data_frame for sheet_name, data_frame in all_sheets.items()}
    return sheet_dict


def get_main_data_frame(excel_file_path):
    """
    Initialize data from an Excel file.

    Args:
        excel_file_path (str): Path to the Excel file.
    Returns:
      data_frame:  a data frame composed of the transactions with the user information and the items
    """
    sheet_dict = init_data(excel_file_path)
    merged_df = pd.merge(sheet_dict['users'], sheet_dict['transactions'],  on='user_id')
    merged_df = pd.merge(merged_df, sheet_dict['items'], on='item_id')
    return merged_df
