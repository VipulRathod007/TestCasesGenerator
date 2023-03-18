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

    def __init__(self, inTestSuite: str, inTestSets: list[str], inTouchstoneRoot: str, inMDEF: MDEF):
        super().__init__(inTestSuite, inTestSets, inTouchstoneRoot, inMDEF)

    def createSelectAll(self, inTestSet: str, inStartID: int = 1):
        """
        Creates the SQL_SELECT_ALL test-set with customized name and starting testcase Id
        :param inTestSet: Actual Name of the SQL_SELECT_ALL test-set
        :param inStartID: Start ID for new queries
        :return:
        """

        def prepare(inTable):
            query = f'SELECT * FROM {inTable.FullName} ORDER BY ' \
                    f'{" AND ".join(map(lambda x: x.Name, inTable.PrimaryKeys))}'
            return query

        if isNoneOrEmpty(inTestSet):
            raise TSException('Empty inputs are not considered')

        queries = list()
        for table in self.mMDEF.Tables:
            queries.append(prepare(table))
            for vTable in table.VirtualTables:
                queries.append(prepare(vTable.FullName))

        self.createTestSet(inTestSet, queries, inStartID)

    def createSQLPassdown(self, inTestSet: str, inStartID: int = 1):
        """
        Creates the SQL_PASSDOWN test-set with customized name and starting testcase Id
        :param inTestSet: Actual Name of the SQL_PASSDOWN test-set
        :param inStartID: Start ID for new queries
        """

        def prepare(inTable):
            query = f'SELECT * FROM {inTable.FullName} ORDER BY ' \
                    f'{" AND ".join(map(lambda x: x.Name, inTable.PrimaryKeys))}'
            return query

        if isNoneOrEmpty(inTestSet):
            raise TSException('Empty inputs are not considered')

        queries = list()
        for table in self.mMDEF.Tables:
            queries.append(prepare(table))
            for vTable in table.VirtualTables:
                queries.append(prepare(vTable.FullName))

        self.createTestSet(inTestSet, queries, inStartID)
