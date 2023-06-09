""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _DB.py                                                                                                     """
""" Contains the definition of the DBWrapper class                                                                   """
""" Well-written code is immortal                                                                                    """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import pyodbc
import sys

from pyodbc import Cursor, Connection

from DB._DBNucleus import DBTable, DBColumn, DBPrimaryKey
from GenUtility import isNoneOrEmpty


class DBWrapper:
    """
    Represents DBWrapper class
    Supports SQL Query execution
    """

    def __init__(self, inConnectionString: str):
        if isNoneOrEmpty(inConnectionString):
            print(f'Error: Empty Connection String provided to {self.__class__}')
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
            print(f'Error: {error}')
            sys.exit(1)

    def disconnect(self):
        """Disconnects from DB"""
        if self.__mConnection is not None:
            self.__mConnection.close()

    def init(self, inTables: list[str] = None, inCachedRows: int = None) -> dict:
        """
        Initializes all the tables with Column, Primary and Foreign keys data
        :param inTables: List of tables to initialize (Default=None, to cache all the Tables)
        :param inCachedRows: No of rows' data to cache in a column (Default=None, to cache all)
        """
        if isNoneOrEmpty(inTables):
            inTables = list()

        allTables = dict()
        for tableMeta in self.getTablesNames():
            table = DBTable(tableMeta[0], tableMeta[1], tableMeta[2])
            if table.FullName in inTables:
                allTables[table.FullName] = table
        for table in allTables.values():
            # Populates Primary Keys
            for pKey in self.getPrimaryKeyNames(table.mName, table.mCatalog, table.mSchema):
                primaryKey = DBPrimaryKey(pKey[3], pKey[4], pKey[5])
                table.mPrimaryKeys[primaryKey.mName] = primaryKey
            # Populates Column Meta Data
            tableData = self.getTableData(table.FullName, inCachedRows)
            tableColumns = self.getColumns(table.mName, table.mCatalog, table.mSchema)
            for colIdx, colData in enumerate(tableColumns):
                column = DBColumn(colData[3], colData[5])
                for rowData in tableData:
                    assert len(rowData) == len(tableColumns)
                    column.addToResultSet(rowData[colIdx])
                table.mColumns[column.mName] = column
        return allTables

    def getTablesNames(self) -> list:
        """
        Returns all the table data
        :return: list of tuple(Catalog, Schema, Table, Type, dict(privileges))
        """
        allTables = list()
        tablesInfo = self.Cursor.tables().fetchall()
        for tableData in tablesInfo:
            if tableData[3] == 'TABLE':
                allTables.append(tableData)
        return allTables

    def getColumns(self, inTable: str, inCatalog: str, inSchema: str) -> list:
        """
        Retrieves the columns of a given table
        :return: List of tuple(Catalog,
                               Schema,
                               Table,
                               Column,
                               Data type,
                               Type name,
                               Column Size,
                               Buffer length,
                               Decimal digits,
                               Num Prec Radix,
                               Nullable,
                               Remarks,
                               Column definition,
                               SQL Data type,
                               SQL Date time sub,
                               Character Octet length,
                               Ordinal position,
                               Is Nullable,
                               User data type)
        """
        if isNoneOrEmpty(inTable) or isNoneOrEmpty(inCatalog) or isNoneOrEmpty(inSchema):
            print(f'Error: Empty Table data provided to {self.__class__}')
            sys.exit(1)
        return self.Cursor.columns(inTable, inCatalog, inSchema).fetchall()

    def getTableData(self, inTable: str, inLimitRows: int = None) -> list:
        """
        Selects all the data of the given table
        Equivalent to SELECT * FROM TABLE
        :param inLimitRows: No. of rows to fetch from given table (Default=None, to select all)
        :param inTable: Full qualified table name (Catalog.Schema.Table)
        :return: Table's data -> list(values)
        """
        if isNoneOrEmpty(inTable):
            print(f'Error: Empty Table data provided to {self.__class__}')
            sys.exit(1)
        print(f'Info: Fetching data of {inTable}')
        resultSet = self.Cursor.execute(f'SELECT * FROM {inTable}')
        filteredSet = resultSet.fetchmany(inLimitRows) if inLimitRows is not None else resultSet.fetchall()
        return filteredSet

    def getPrimaryKeyNames(self, inTableName: str, inCatalogName: str, inSchemaName: str) -> list:
        """
        Returns all the Primary Keys of a table
        :return: list of tuple(Catalog, Schema, Table, Column, Sequence, PK Name)
        """
        if isNoneOrEmpty(inTableName) or isNoneOrEmpty(inCatalogName) or isNoneOrEmpty(inSchemaName):
            print(f'Error: Empty Table data provided to {self.__class__}')
            sys.exit(1)
        return self.Cursor.primaryKeys(inTableName, inCatalogName, inSchemaName).fetchall()

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
