import re
from tinydb import TinyDB, Query
from tinydb.operations import *
from time import time

# Queue Database wrapper
class Queue():
    __DB = None
    __QUERY = None

    def __init__(self, path):
        self.__DB = TinyDB(path)
        self.__QUERY = Query()

    # Adds the info to the database
    def add(self, info):
        idx = self.__DB.insert(info)
        self.__DB.update(set("printHistory", []), doc_ids=[idx])
        self.__DB.update(set("id", idx - 1), doc_ids=[idx])
        self.__log(idx, "add", "") 

    # Remove the specified print
    def remove(self, idx):
        self.__DB.remove(idx)

    # Gets the specified print by id
    def get(self, idx):
        return self.__DB.all()[idx]

    # Gets the first n prints given a query
    def get_n(self, n, query=None):
        prints = self.__DB.all()

        if query:
            prints = self.__DB.search(query)

        return self.__DB.all()[:n]

    # Queries the list
    def search(self, query):
        pass

    # Updates the specified print
    def edit(self, idx, printInfo):
        self.get(idx).update(printInfo, doc_id=idx)

    # Logs information, should only be used internally
    # Useful for making log messages consistent
    def __log(self, idx, action, note):
        self.__DB.update(add('printHistory', "{\"action\": \"test\", \"note\": \"\", \"unixTime\": 000000\}"), 
            doc_ids = [idx]
        )
