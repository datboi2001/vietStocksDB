# This is a sample Python script.

# Press Alt+Shift+X to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
from src.api import ping_api
import os
from datetime import datetime
from src.DBInterface import DBInterface


def main():
    """
    Driver code to ping api then save the result to a database
    :return:
    """
    params = {'platform': 'web', 'param': 'match_price:500:1000000', 'floor': 'all', 'group_id': 'all',
              'key': 'match_price', 'sort': 'asc', 'page': 1, 'per_page': 500}
    url = os.getenv('API_URL')
    result = []
    result, total_page = ping_api(result, url + '/v1/web/company/technical-filter', params)
    result, total_page = ping_api(result, url + '/v1/web/company/technical-filter', params, total_page=total_page)
    # Add a date
    for i, doc in enumerate(result):
        doc['date'] = datetime.today().strftime('%Y-%m-%d')
        result[i] = doc
    # Save the result to the database
    db_interface = DBInterface(os.getenv('MONGO_URL'), 'stocksDB', 'vietStocks')
    result, exception = db_interface.start_db_operations(result)

    if exception != '':
        print(f'Error: {exception}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
