from typing import Any 
import requests


# Ping a financial API to get the latest stock information

def handle_response(response: requests.Response) -> tuple[dict[str, Any], int]:
    """
    :param response: the response object from the api
    :return: a tuple of the json result and the total number of pages
    """
    if response.status_code == 200:
        json_result = response.json()
        total_page = json_result.get('data', {'data': []}).get('total_page', 1)
        return json_result, total_page
    else:
        print(f'Error: {response.status_code}. {response.json()}')
        return {}, 0


def ping_api(result: list[dict[str, Any]], url: str, params: dict[str, Any], **kwargs) -> tuple[
    list[dict[str, Any]], int]:
    """
    :param url: The name of the api url
    :param result: a list of json objects to be inserted or updated in the database.
    :param params: a dictionary of parameters to be passed to the api
    :param kwargs: any additional parameters to be passed to the api
    :return: a tuple of the json result and the total number of pages
    """
    total_page = kwargs.get('total_page', 1)
    if total_page == 1:
        page_range = range(1, total_page + 1)
    else:
        # If the total number of pages is greater than 1, we need to ping the api from page 2 to the last page
        page_range = range(2, total_page + 1)
    for page in page_range:
        params['page'] = page
        print(f'Pinging page {page} of {total_page}')
        response = requests.get(url=url, params=params)
        json_result, new_total_page = handle_response(response)
        if len(json_result) == 0:
            break
        result.extend(json_result.get('data', {'data': []}).get('data', []))
        total_page = new_total_page
    return result, total_page
