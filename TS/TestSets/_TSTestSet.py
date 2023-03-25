""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _TSTestSet.py                                                                                              """
""" Contains the definition of TSTestSet class                                                                       """
""" It's okay to have stack underflow of thoughts sometimes                                                          """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import xml.etree.ElementTree as Etree

from GenUtility import isNoneOrEmpty, readFile
from P4Utils import Perforce
from TS import TSException


class TSTestSet:
    """Represents data class for TestSet"""

    def __init__(self, inTestSuiteName: str, inStandardName: str, inActualName: str):
        if isNoneOrEmpty(inStandardName) or isNoneOrEmpty(inActualName):
            raise TSException(f'Empty/Invalid input provided at {self.__class__.__name__}')
        self.__mTestSuiteName = inTestSuiteName
        self.__mStdName = inStandardName
        self.__mActName = inActualName
        self.__mStartID = None

    def init(self, inTestDefinitionLoc: str):
        """
        Initializes the TestSet metadata
        :param inTestDefinitionLoc: Absolute path to the test-definition directory
        """
        if not os.path.exists(inTestDefinitionLoc):
            raise TSException(f'Invalid Path provided at {self.__class__.__name__}\n'
                              f'{inTestDefinitionLoc}')
        testSetPath = os.path.join(inTestDefinitionLoc, self.__mTestSuiteName, 'TestSets', self.__mActName)
        if not os.path.exists(testSetPath):
            raise TSException(f'Invalid Path provided at {self.__class__.__name__}\n'
                              f'{testSetPath}')
        content = readFile(testSetPath)
        etree = Etree.fromstring(content.strip())
        lastTestSetID = None
        for child in etree.iter('Test'):
            lastTestSetID = child.attrib.get('ID')
        self.__mStartID = int(lastTestSetID) + 1

    @property
    def ActualName(self):
        return self.__mActName

    @property
    def StandardName(self):
        return self.__mStdName

    @property
    def StartID(self):
        if self.__mStartID is None:
            raise TSException(f'Un-initialized TestSet. Call {self.__class__}.init() beforehand')
        return self.__mStartID

    @property
    def TestSuiteName(self):
        return self.__mTestSuiteName
