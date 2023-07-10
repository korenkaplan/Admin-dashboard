from dashboard import dashboard_config
from excel_data_frames import get_transactions_users__items_data_frame,init_data


def main():
    combined_df = get_transactions_users__items_data_frame("C:\\Users\\Koren Kaplan\\Desktop\\Projects\\Python Final Project\\Python Scan and Go Database.xlsx")
    projection = ['order_date', 'full_name', 'category', 'item_name', 'item_tags', 'season', 'printing', 'price', 'amount']
    shheet= init_data("C:\\Users\\Koren Kaplan\\Desktop\\Projects\\Python Final Project\\Python Scan and Go Database.xlsx")
    print(shheet['transactions'])
    dashboard_config(combined_df, projection)


if __name__ == '__main__':
    main()
