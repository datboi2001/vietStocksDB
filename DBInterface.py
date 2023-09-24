import pymongo
from pymongo.client_session import ClientSession
import logging


# Create a class to handle all database interactions


def _find_redundant_symbols(collection_symbols: set[str], api_symbols: set[str]):
    """
    :param collection_symbols: a set of symbols from the database
    :param api_symbols: a set of symbols from the api
    :return: set difference between the two sets
    """
    return collection_symbols - api_symbols


def get_symbols_from_api(data: list[dict[str, int | str]]) -> set[str]:
    """
    :param data: a list of json objects to be inserted or updated in the database. The json objects must have a
    'symbol' key.
    :return: a set of symbols from the api
    """
    return set(doc['symbol'] for doc in data)


def _callback(session: ClientSession, stock: pymongo.collection.Collection, data: list[dict[str, any]]):
    # Loop through the data and update the database
    for doc in data:
        stock.find_one_and_replace({'symbol': doc['symbol']}, doc, upsert=True, session=session)


class DBInterface:

    def __init__(self, url: str, db_name: str, collection_name: str):
        self.client = pymongo.MongoClient(url)
        # If the database does not exist, it will be created.
        self.db = self.client.get_database(db_name)
        # If the collection does not exist, it will be created.
        self.collection = self.db.get_collection(collection_name)

        self.collection_symbols = self.get_symbols()

    def get_symbols(self) -> set[str]:
        """
        :return: a set of symbols from the database
        """
        return set(doc['symbol'] for doc in self.collection.find({}, {'_id': 0, 'symbol': 1}))

    def start_db_operations(self, data: list[dict[str, int | str]]) -> tuple[bool, str]:
        """
        :param data: a list of json objects to be inserted or updated in the database. The json objects must have a
        'symbol' key. The collection will search for the symbol and update the document if it exists, otherwise it will
        insert a new document.
        :return: boolean indicating success or failure and a message in case of failure
        """
        # Main idea: get all symbols from the database, get all symbols from the api
        # and find the difference between the two sets. The difference is the set of symbols to be deleted.
        # This is to ensure that the database is always up to date with the api.

        try:
            symbols_for_delete = _find_redundant_symbols(self.collection_symbols, get_symbols_from_api(data))
            if len(symbols_for_delete) > 0:
                self.delete(list(symbols_for_delete))
            with self.client.start_session() as session:
                session.with_transaction(lambda s: _callback(s, self.collection, data))
            return True, ''
        except Exception as e:
            return False, str(e)

    def delete(self, symbol: list[str]):
        """
        :param symbol: the symbol to be deleted
        :return: boolean indicating success or failure and a message in case of failure
        """
        self.collection.delete_many({'symbol': {'$in': symbol}})

# Path: main.py
