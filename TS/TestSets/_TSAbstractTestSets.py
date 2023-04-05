""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _TSAbstractTestSets.py                                                                                     """
""" Contains the definition of TSAbstractTestSets class                                                              """
""" Life is meant to be anything other than an empty function                                                        """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import sys

from abc import ABC, abstractmethod

from TS._TSException import TSException
from TS.TestSets._TSTestSet import TSTestSet
from P4Utils import Perforce, PerforceException
from MDEF import MDEF
from GenUtility import isNoneOrEmpty, writeFile


class TSAbstractTestSets(ABC):
    """Represents abstract TSAbstractTestSets class"""

    @abstractmethod
    def __init__(self, inTestSuite: str, inTestSets: list[TSTestSet], inTouchstoneRoot: str, inMDEF: MDEF, inResultSet: dict):
        # TODO: Create class for TestSuite/TestSet provide more input i.e SetFile or ID as part of instance
        if isNoneOrEmpty(inTestSuite) or isNoneOrEmpty(inTestSets) or \
                isNoneOrEmpty(inTouchstoneRoot) or isNoneOrEmpty(inMDEF):
            raise TSException('Empty inputs are not considered')
        if not os.path.exists(inTouchstoneRoot):
            raise TSException('Invalid Location')
        self.mMDEF = inMDEF
        self.mTestSuite = inTestSuite
        self.mTestSets = inTestSets
        self.mTouchstoneRoot = inTouchstoneRoot
        self.mResultSet = inResultSet

    @abstractmethod
    def create(self):
        pass

    def createTestSuite(self):
        """Creates TestSuite.xml for given test-suite"""
        content = f'<TestSuite Name="{self.mTestSuite}">\n'
        for testSet in self.mTestSets:
            content += f'\t<TestSet Name="{testSet.StandardName}" ' \
                       f'SetFile="{self.mTestSuite}/TestSets/{testSet.ActualName}.xml" />\n'
        content += '\t<GenerateResults>true</GenerateResults>\n'
        content += f'\t<BaselineDirectory>{self.mTestSuite}\ResultSets</BaselineDirectory>\n'
        content += '</TestSuite>'

        writeFile(content, os.path.join(self.mTouchstoneRoot, self.mTestSuite, 'TestSuite.xml'))

    def createTestSet(self, inTestSet: TSTestSet, inQueries: list[str]):
        """
        Creates Test set file for given test-set name
        :param inTestSet: Instance of the test-set
        :param inQueries: List of queries for given test-set
        """
        if isNoneOrEmpty(inQueries):
            raise TSException(f'Empty list of Queries are not considered at {self.__class__.__name__}')
        if all(map(lambda x: x.ActualName != inTestSet.ActualName, self.mTestSets)):
            raise TSException(f'{inTestSet.ActualName} can not be created for {self.mTestSuite}')

        content = f'<TestSet Name="{inTestSet.StandardName}" ' \
                  f'JavaClass="com.simba.testframework.testcases.jdbc.resultvalidation.SqlTester" ' \
                  f'dotNetClass="SqlTester">\n'
        for idx, query in enumerate(inQueries):
            content += f'\t<Test Name="SQL_QUERY" JavaMethod="testSqlQuery" dotNetMethod="TestSqlQuery" ' \
                       f'ID="{inTestSet.StartID + idx}">\n'
            content += f'\t\t<SQL><![CDATA[ {query} ]]></SQL>\n'
            # TODO: Fix hardcoded values and add more parameters
            content += f'\t\t<ValidateColumns>True</ValidateColumns>\n'
            content += f'\t\t<ValidateNumericExactly>True</ValidateNumericExactly>\n'
            content += f'\t</Test>\n'
        content += '</TestSet>'

        writeFile(
            content, os.path.join(self.mTouchstoneRoot, self.mTestSuite, 'TestSets', f'{inTestSet.ActualName}.xml')
        )
