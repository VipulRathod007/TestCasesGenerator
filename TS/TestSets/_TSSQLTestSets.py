""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _TSSQLTestSets.py                                                                                          """
""" Contains the definition of TSSQLTestSets class                                                                   """
""" Be so good to be chosen again and again                                                                          """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import random

from MDEF import MDEF
from P4Utils import Perforce
from GenUtility import isNoneOrEmpty
from TS.TestSets._TSTestSet import TSTestSet
from TS.TestSets._TSAbstractTestSets import TSAbstractTestSets


class TSSQLTestSets(TSAbstractTestSets):
    """
    Represents TSSQLTestSets class
    Prepares all the SQL TestSets
    """

    def __init__(self, inTestSuite: str, inTestSets: list[TSTestSet], inTouchstoneRoot: str, inMDEF: MDEF, inResultSet: dict):
        super().__init__(inTestSuite, inTestSets, inTouchstoneRoot, inMDEF, inResultSet)

    def create(self):
        """Creates all the test-sets for given test-suite"""
        self.createTestSuite()
        for testSet in self.mTestSets:
            queries = None
            if testSet.StandardName.upper() == 'SQL_ORDER_BY':
                queries = self.createOrderBy(testSet)
            elif testSet.StandardName.upper() == 'SQL_SELECT_TOP':
                queries = self.createSelectTop(testSet)
            elif testSet.StandardName.upper() == 'SQL_COLUMNS_1TABLE':
                queries = self.createFirstColumns(testSet)
            elif testSet.StandardName.upper() == 'SQL_GROUP_BY':
                queries = self.createGroupBy(testSet)
            elif testSet.StandardName.upper() == 'SQL_IN_BETWEEN':
                queries = self.createInBetween(testSet)
            elif testSet.StandardName.upper() == 'SQL_AND_OR':
                queries = self.createAndOr(testSet)
            elif testSet.StandardName.upper() == 'SQL_LIKE':
                queries = self.createLike(testSet)
            elif testSet.StandardName.upper() == 'SQL_FUNCTION_1TABLE':
                queries = self.createFunction(testSet)
            if not isNoneOrEmpty(queries):
                self.createTestSet(testSet, queries)

    def createOrderBy(self, inTestSet: TSTestSet) -> list[str]:
        """Creates the SQL_ORDER_BY test-set"""

        def prepare(inResultSet) -> list:
            queries = list()
            for colName in set(random.choices(list(inResultSet.mColumns), k=inTestSet.MaxQueriesPerTable)):
                queries.append(f'SELECT * FROM {inResultSet.FullName} ORDER BY {colName}')
            return queries

        queries = list()
        for table in self.mMDEF.AllTables:
            queries.extend(prepare(self.mResultSet[table.FullName]))

        return queries

    def createSelectTop(self, inTestSet: TSTestSet) -> list[str]:
        """Creates the SQL_SELECT_TOP test-set"""

        def prepare(inResultSet) -> list:
            queries = list()
            for colName in set(random.choices(list(inResultSet.mColumns), k=inTestSet.MaxQueriesPerTable)):
                count = len(inResultSet.mColumns[colName].getResultSet()) % 25
                if count > 0:
                    queries.append(f'SELECT TOP {count} {colName} FROM {inResultSet.FullName} ORDER BY {colName}')
            return queries

        queries = list()
        for table in self.mMDEF.AllTables:
            queries.extend(prepare(self.mResultSet[table.FullName]))

        return queries

    def createGroupBy(self, inTestSet: TSTestSet) -> list[str]:
        """Creates the SQL_SELECT_TOP test-set"""

        def prepare(inResultSet) -> list:
            queries = list()
            for colName in set(random.choices(list(inResultSet.mColumns), k=inTestSet.MaxQueriesPerTable)):
                colValues = list(set(inResultSet.mColumns[colName].getResultSet()))
                if len(colValues) > 0:
                    queries.append(f'SELECT {colName} FROM {inResultSet.FullName} GROUP BY {colName} '
                                   f'HAVING {colName} = {colValues[0]}')
                else:
                    queries.append(f'SELECT {colName} FROM {inResultSet.FullName} GROUP BY {colName} ORDER BY {colName}')
            return queries

        queries = list()
        for table in self.mMDEF.AllTables:
            queries.extend(prepare(self.mResultSet[table.FullName]))

        return queries

    def createInBetween(self, inTestSet: TSTestSet) -> list[str]:
        """Creates the SQL_IN_BETWEEN test-set"""

        def prepare(inResultSet) -> list:
            queries = list()
            for colName in set(random.choices(list(inResultSet.mColumns), k=inTestSet.MaxQueriesPerTable)):
                colValues = list(set(inResultSet.mColumns[colName].getResultSet()))
                if len(colValues) >= 2:
                    queries.append(f'SELECT {colName} FROM {inResultSet.FullName} '
                                   f'WHERE {colName} IN ({",".join(map(str, set(random.choices(colValues, k=5))))})')
            return queries

        queries = list()
        for table in self.mMDEF.AllTables:
            queries.extend(prepare(self.mResultSet[table.FullName]))

        return queries

    def createLike(self, inTestSet: TSTestSet) -> list[str]:
        """Creates the SQL_LIKE test-set"""

        def prepare(inResultSet) -> list:
            queries = list()
            for colName in set(random.choices(list(inResultSet.mColumns), k=inTestSet.MaxQueriesPerTable)):
                colValues = list(set(inResultSet.mColumns[colName].getResultSet()))
                if isNoneOrEmpty(colValues):
                    continue
                colValue = str(random.choice(colValues))
                pattern = f'%{random.choice(list(colValue))}{random.choice(["_", "%", ""])}'
                queries.append(f'SELECT {colName} FROM {inResultSet.FullName} WHERE {colName} LIKE \'{pattern}\'')
            return queries

        queries = list()
        for table in self.mMDEF.AllTables:
            queries.extend(prepare(self.mResultSet[table.FullName]))

        return queries

    def createFunction(self, inTestSet: TSTestSet) -> list[str]:
        """Creates the SQL_FUNCTION_1TABLE test-set"""

        def prepare(inResultSet) -> list:
            queries = list()
            for colName in set(random.choices(list(inResultSet.mColumns), k=inTestSet.MaxQueriesPerTable)):
                colType = inResultSet.mColumns[colName].mType
                if 'INT' in colType.upper():
                    currFunc = random.choice(['MAX', 'MIN', 'COUNT', 'SUM', 'AVG'])
                    queries.append(f'SELECT {currFunc}({colName}) AS {currFunc}_{colName.upper()} '
                                   f'FROM {inResultSet.FullName}')
                elif 'CHAR' in colType.upper():
                    currFunc = random.choice(['UCASE', 'LCASE', 'COUNT'])
                    queries.append(f'SELECT {currFunc}({colName}) FROM {inResultSet.FullName}')
                else:
                    continue
            return queries

        queries = list()
        for table in self.mMDEF.AllTables:
            queries.extend(prepare(self.mResultSet[table.FullName]))

        return queries

    def createAndOr(self, inTestSet: TSTestSet) -> list[str]:
        """Creates the SQL_AND_OR test-set"""

        def prepare(inResultSet) -> list:
            queries = list()
            for _ in range(inTestSet.MaxQueriesPerTable):
                colMap = list()
                for colName in set(random.choices(list(inResultSet.mColumns), k=5)):
                    colValues = list(set(inResultSet.mColumns[colName].getResultSet()))
                    if not isNoneOrEmpty(colValues):
                        colMap.append(f'{colName} = {colValues[0]}')
                if len(colMap) < 2:
                    continue
                joint = random.choice([' AND ', ' OR '])
                queries.append(f'SELECT * FROM {inResultSet.FullName} WHERE {joint.join(colMap)}')
            return queries

        queries = list()
        for table in self.mMDEF.AllTables:
            queries.extend(prepare(self.mResultSet[table.FullName]))

        return queries

    def createFirstColumns(self, inTestSet: TSTestSet) -> list[str]:
        """Creates the SQL_COLUMNS_1TABLE test-set"""

        def prepare(inResultSet) -> list:
            queries = list()
            for colName in set(random.choices(list(inResultSet.mColumns), k=inTestSet.MaxQueriesPerTable)):
                queries.append(f'SELECT {colName} FROM {inResultSet.FullName} ORDER BY {colName}')
            return queries

        queries = list()
        for table in self.mMDEF.AllTables:
            queries.extend(prepare(self.mResultSet[table.FullName]))

        return queries
