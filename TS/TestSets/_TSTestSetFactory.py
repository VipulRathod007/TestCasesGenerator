""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _TSTestSetFactory.py                                                                                       """
""" Contains the definition of TSTestSetFactory class                                                                """
""" Design patterns are elite irrespective of the language                                                           """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from TS._TSException import TSException
from TS.TestSets._TSIntegrationTestSets import TSIntegrationTestSets
from TS.TestSets._TSTestSet import TSTestSet

from GenUtility import isNoneOrEmpty
from MDEF import MDEF


class TSTestSetFactory:

    TestDefinitions = [
        'INTEGRATION',
        'SQL',
        'SP'
    ]
    TestSets = [
        'SQL_SELECT_ALL',
        'SQL_PASSDOWN',
        'SQL_SP',
        'SQL_AND_OR',
        'SQL_FUNCTION_1TABLE',
        'SQL_GROUP_BY',
        'SQL_IN_BETWEEN',
        'SQL_LIKE',
        'SQL_ORDER_BY',
        'SQL_SELECT_TOP',
        'SQL_COLUMNS_1TABLE'
    ]

    @classmethod
    def create(cls, inTestSuite: str, inTestSets: list[TSTestSet], inTouchstoneRoot: str, inMDEF: MDEF, inResultSet: dict):
        if isNoneOrEmpty(inTestSuite):
            raise TSException('Empty Test Definition name provided')
        if inTestSuite.upper() == 'INTEGRATION':
            return TSIntegrationTestSets(inTestSuite, inTestSets, inTouchstoneRoot, inMDEF, inResultSet)
        elif inTestSuite.upper() == 'SQL':
            # TODO: Fix me
            pass
        elif inTestSuite.upper() == 'SP':
            # TODO: Fix me
            pass
