from dashboard import init_dashboard


def main():
    projection = ['full_name', 'age', 'gender', 'item_name', 'category', 'item_tags', 'season', 'printing', 'price', 'amount', 'order_date']
    init_dashboard(projection)


if __name__ == '__main__':
    main()
