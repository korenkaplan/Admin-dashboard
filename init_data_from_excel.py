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

    # Read all sheets from Excel file
    all_sheets = pd.read_excel(excel_file_path, sheet_name=None)

    # Create a dictionary to store the sheets
    sheet_dict = {sheet_name: data_frame for sheet_name, data_frame in all_sheets.items()}


    return sheet_dict