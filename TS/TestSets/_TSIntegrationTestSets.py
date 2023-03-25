""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _TSIntegrationTestSets.py                                                                                  """
""" Contains the definition of TSIntegrationTestSets class                                                           """
""" Integration of qualities is always a good idea                                                                   """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


from MDEF import MDEF
from P4Utils import Perforce
from GenUtility import isNoneOrEmpty
from TS import TSException
from TS.TestSets._TSTestSet import TSTestSet
from TS.TestSets._TSAbstractTestSets import TSAbstractTestSets


class TSIntegrationTestSets(TSAbstractTestSets):
    """
    Represents TSIntegrationTestSet class
    Prepares all Integration TestSets
    """

    def __init__(self, inTestSuite: str, inTestSets: list[TSTestSet], inTouchstoneRoot: str, inMDEF: MDEF, inResultSet: dict):
        super().__init__(inTestSuite, inTestSets, inTouchstoneRoot, inMDEF, inResultSet)

    def create(self):
        """Creates all the test-sets for given test-suite"""
        self.createTestSuite()
        for testSet in self.mTestSets:
            queries = None
            if testSet.StandardName.upper() == 'SQL_SELECT_ALL':
                queries = self.createSelectAll()
            elif testSet.StandardName.upper() == 'SQL_PASSDOWN':
                queries = self.createSQLPassdown()
            self.createTestSet(testSet, queries)

    def createSelectAll(self) -> list[str]:
        """Creates the SQL_SELECT_ALL test-set"""

        def prepare(inTable):
            query = f'SELECT * FROM {inTable.FullName} ORDER BY ' \
                    f'{" AND ".join(map(lambda x: x.Name, inTable.PrimaryKeys))}'
            return query

        queries = list()
        for table in self.mMDEF.Tables:
            queries.append(prepare(table))
            for vTable in table.VirtualTables:
                queries.append(prepare(vTable.FullName))

        return queries

    def createSQLPassdown(self) -> list[str]:
        """Creates the SQL_PASSDOWN test-sets"""

        def prepare(inTable):
            colValueMap = list()
            for colName in inTable.ItemEndpointColumnNames:
                colValues = self.mResultSet[inTable.FullName][colName].getResultSet()
                colValueMap.append(f'{colName}={colValues[0]}')
            query = f'SELECT * FROM {inTable.FullName} WHERE {" AND ".join(colValueMap)}'
            return query

        queries = list()
        for table in self.mMDEF.Tables:
            queries.append(prepare(table))
            for vTable in table.VirtualTables:
                queries.append(prepare(vTable.FullName))

        return queries
