from dashboard import dashboard_config
from excel_data_frames import get_main_data_frame


def main():
    excel_file_path = "C:\\Users\\Koren Kaplan\\Desktop\\Projects\\Python Final Project\\Python Scan and Go Database.xlsx"
    projection = ['full_name', 'age', 'gender', 'item_name', 'category', 'item_tags', 'season', 'printing', 'price', 'amount', 'order_date']
    combined_df = get_main_data_frame(excel_file_path)
    dashboard_config(combined_df, projection)


if __name__ == '__main__':
    main()
