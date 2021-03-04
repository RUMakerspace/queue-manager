import re
from tinydb import TinyDB, Query
from tinydb.operations import *
from time import time

# Queue Database wrapper
class Queue:
    __DB = None
    __QUERY = None
    __PRINTS = None
    __LOG = None

    def __init__(self, path):
        self.__DB = TinyDB(path)
        self.__QUERY = Query()
        self.__PRINTS = self.__DB.table("queue")
        self.__LOG = self.__DB.table("log")

    # Adds the info to the database
    def add_print(self, info):
        idx = self.__PRINTS.insert(info)
        self.__PRINTS.update(set("id", idx), doc_ids=[idx])
        self.__PRINTS.update(set("status", "new"), doc_ids=[idx])
        self.log(idx, "add", "")

    # Remove the specified print
    def remove_print(self, idx):
        self.__PRINTS.remove(self.__QUERY["id"] == idx)

    # Gets the specified print by id
    def get_print(self, idx):
        return self.__PRINTS.search(self.__QUERY["id"] == idx)[0]

    # Gets the first n prints given a query
    def get_prints(self, n=0, query=None):
        prints = self.__PRINTS.all()

        if query:
            prints = self.__PRINTS.search(query)

        if n > 0:
            prints = prints[:n]

        return prints

    # Get the log for a specific print
    def get_log(self, idx):
        return self.__LOG.search(self.__QUERY["id"] == idx)

    # Updates the specified print status
    def set_status(self, idx, status):
        self.get_print(idx).update(set("status", status), doc_ids=[idx])
        self.log(idx, "edit", "")

    # Updates the specified print
    def edit_print(self, idx, printInfo):
        self.get_print(idx).update(printInfo, doc_ids=[idx])
        self.log(idx, "edit", "")

    # Logs information, should only be used internally
    # Useful for making log messages consistent
    def log(self, idx, action, note):
        self.__LOG.insert({"id": idx, "time": time(), "action": action, "note": note})
