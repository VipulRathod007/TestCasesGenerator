""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _TSAbstractTestSet.py                                                                                      """
""" Contains the definition of TSAbstractTestSet class                                                               """
""" Life is meant to be anything other than an empty function                                                        """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import sys

from abc import ABC, abstractmethod

from TS.TSException import TSException
from P4Utils import Perforce, PerforceException
from MDEF import MDEF
from GenUtility import isNoneOrEmpty, writeFile


class TSAbstractTestSet(ABC):
    """Represents TSAbstractTestSet class that deals with all the common functionality its child classes will provide"""

    @abstractmethod
    def __init__(self, inTestSuite: str, inTestSets: dict, inTouchstoneRoot: str, inMDEF: MDEF, inResultSet: dict):
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

    @abstractmethod
    def create(self):
        pass

    def createTestSuite(self):
        """Creates TestSuite.xml for given test-suite"""
        content = f'<TestSuite Name="{self.mTestSuite}">\n'
        for testSet in self.mTestSets:
            content += f'<TestSet Name="{testSet}" SetFile="{self.mTestSuite}/TestSets/{testSet}.xml" />\n'
        content += '<GenerateResults>true</GenerateResults>\n'
        content += f'<BaselineDirectory>{self.mTestSuite}\ResultSets</BaselineDirectory>\n'
        content += '</TestSuite>'

        writeFile(content, os.path.join(self.mTouchstoneRoot, self.mTestSuite, 'TestSuite.xml'))

    def createTestSet(self, inTestSet: str, inQueries: list[str], inStartID: int = 1):
        """
        Creates Test set file for given test-set name
        :param inTestSet: Name of the test-set
        :param inQueries: List of queries for given test-set
        :param inStartID: Start ID for new queries
        """
        if isNoneOrEmpty(inQueries) or isNoneOrEmpty(inTestSet):
            raise TSException('Empty inputs are not considered')
        if inTestSet not in self.mTestSets:
            raise TSException(f'{inTestSet} can not be created for {self.mTestSuite}')

        content = f'<TestSet Name="{inTestSet}" ' \
                  f'JavaClass="com.simba.testframework.testcases.jdbc.resultvalidation.SqlTester" ' \
                  f'dotNetClass="SqlTester">\n'
        for idx, query in enumerate(inQueries):
            content += f'\t<Test Name="SQL_QUERY" JavaMethod="testSqlQuery" dotNetMethod="TestSqlQuery" ' \
                       f'ID="{inStartID + idx}">\n'
            content += f'\t\t<SQL><![CDATA[ {query} ]]></SQL>\n'
            # TODO: Fix hardcoded values and add more parameters
            content += f'\t\t<ValidateColumns>True</ValidateColumns>\n'
            content += f'\t\t<ValidateNumericExactly>True</ValidateNumericExactly>\n'
            content += f'\t</Test>\n'
        content += '</TestSet>'

        writeFile(content, os.path.join(self.mTouchstoneRoot, self.mTestSuite, 'TestSets', f'{inTestSet}.xml'))
