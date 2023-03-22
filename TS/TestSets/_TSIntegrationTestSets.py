""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _TSIntegrationTestSets.py                                                                                  """
""" Contains the definition of TSIntegrationTestSets class                                                           """
""" Integration of qualities is always a good idea                                                                   """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


from MDEF import MDEF
from P4Utils import Perforce
from GenUtility import isNoneOrEmpty
from TS.TSException import TSException

from ._TSAbstractTestSet import TSAbstractTestSet


class TSIntegrationTestSets(TSAbstractTestSet):
    """
    Represents TSIntegrationTestSet class
    Prepares all Integration TestSets
    """

    def __init__(self, inTestSuite: str, inTestSets: dict, inTouchstoneRoot: str, inMDEF: MDEF, inResultSet: dict):
        super().__init__(inTestSuite, inTestSets, inTouchstoneRoot, inMDEF, inResultSet)

    def create(self):
        """Creates all the test-sets for given test-suite"""
        self.createTestSuite()
        for testSet, startID in self.mTestSets.items():
            queries = None
            if testSet.upper() == 'SQL_SELECT_ALL':
                queries = self.createSelectAll()
            elif testSet.upper() == 'SQL_PASSDOWN':
                queries = self.createSQLPassdown()
            self.createTestSet(testSet, queries, startID)

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
        # TODO: Fix me to use Resultsets

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
