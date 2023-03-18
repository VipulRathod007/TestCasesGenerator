""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _DB.py                                                                                                     """
""" Contains the definition of the DBWrapper class                                                                   """
""" Well-written code is immortal                                                                                    """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import pyodbc
import sys

from pyodbc import Cursor, Connection

from DBNucleus import DBTable
from GenUtility import isNoneOrEmpty


class DBWrapper:
    """
    Represents DBWrapper class
    Supports SQL Query execution
    """

    def __init__(self, inConnectionString: str):
        if isNoneOrEmpty(inConnectionString):
            print('Error: Empty Connection String provided')
            sys.exit(1)

        self.__mCursor = None
        self.__mConnection = None
        self.__mConnectionString = inConnectionString

    def connect(self):
        """
        Connects to the ODBC Driver
        Currently works with a single connection
        """
        try:
            if self.__mConnection is None:
                self.__mConnection = pyodbc.connect(self.__mConnectionString, encoding='utf-8', autocommit=True)
                self.__mCursor = self.__mConnection.cursor()
        except Exception as error:
            self.__mConnection = None
            self.__mCursor = None
            print(error)
            sys.exit(1)

    def getTables(self):
        allTables = list()
        tablesInfo = self.Cursor.tables().fetchall()
        for tableData in tablesInfo:
            if tableData[3] == 'TABLE':
                allTables.append(DBTable(tableData[0], tableData[1], tableData[2]))
        return allTables

    @property
    def Connection(self) -> Connection:
        if self.__mConnection is None:
            self.connect()
        return self.__mConnection

    @property
    def Cursor(self) -> Cursor:
        if self.__mConnection is None:
            self.connect()
        return self.__mCursor
