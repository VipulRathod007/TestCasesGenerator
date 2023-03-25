""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _TSInputReader.py                                                                                          """
""" Contains the definition of TSInputReader class                                                                   """
""" Coding makes you input efforts and outputs extraordinary results                                                 """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import json

from enum import Enum

from TS import TSException
from TS.TestSets._TSTestSet import TSTestSet

from P4Utils import Perforce
from GenUtility import assure, isNoneOrEmpty


class Constants(Enum):
    ConnectionString = 'ConnectionString'
    DifferenceFindMode = 'DifferenceFindMode'
    CompareTwoRevisions = 'CompareTwoRevisions'
    ExternalArguments = 'ExternalArguments'
    ModifiedMDEFLocation = 'ModifiedMDEFLocation'
    IsFirstRevision = 'IsFirstRevision'
    PerforceLocation = 'PerforceLocation'
    MDEFLocation = 'MDEFLocation'
    TestDefinitionsLocation = 'TestDefinitionsLocation'
    TestSuite = 'TestSuite'


class TSInput:
    """Represents TSInput class"""
    def __init__(self, inFilePath: str):
        if not os.path.exists(inFilePath):
            raise TSException(f'{inFilePath} not found')

        self.__mContent = None
        with open(inFilePath, 'r') as file:
            self.__mContent = json.load(file)

        self.__parse()

    def __parse(self):
        assert isinstance(self.__mContent, dict)

        for key, val in self.__mContent.items():
            if Constants.ConnectionString.value == key:
                if isNoneOrEmpty(val):
                    raise TSException(f'Empty input for {key}')
                self.__mConnectionString = val

            elif Constants.DifferenceFindMode.value == key:
                if isNoneOrEmpty(val):
                    raise TSException(f'Empty input for {key}')
                for subKey, subVal in val.items():
                    if Constants.CompareTwoRevisions.value == subKey:
                        if isNoneOrEmpty(subVal):
                            self.__mCompareTwoRevisions = None
                            self.__mDifferenceFindMode = Constants.ModifiedMDEFLocation.value
                        else:
                            self.__mCompareTwoRevisions = sorted(map(lambda x: int(x), subVal))
                            self.__mIsFirstRevision = False
                            self.__mDifferenceFindMode = Constants.CompareTwoRevisions.value
                    elif Constants.ModifiedMDEFLocation.value == subKey:
                        self.__mModifiedMDEFLocation = None
                        if self.__mDifferenceFindMode == Constants.ModifiedMDEFLocation.value:
                            if isNoneOrEmpty(subVal) or not os.path.exists(subVal):
                                raise TSException(f'Invalid {subKey}')
                            self.__mModifiedMDEFLocation = subVal
                    elif Constants.IsFirstRevision.value == subKey:
                        self.__mIsFirstRevision = bool(subVal == 'true')
                        # Use `ModifiedMDEFLocation` mode with First revision
                        self.__mDifferenceFindMode = Constants.ModifiedMDEFLocation.value

            elif Constants.PerforceLocation.value == key:
                self.__mMDEFLocation = assure(val, Constants.MDEFLocation.value)
                self.__mTestDefinitionsLocation = assure(val, Constants.TestDefinitionsLocation.value)

            elif Constants.TestSuite.value == key:
                assert isinstance(val, dict)
                self.__mTestDefinitions = dict()
                # TODO: Using P4 here is an overkill.
                #       This must be responsible for reading values and perform basic validations only
                p4Inst = Perforce()
                testDefinitionPath = p4Inst.transformPath(self.__mTestDefinitionsLocation)
                for name, testDefs in val.items():
                    assert isinstance(testDefs, dict)
                    self.__mTestDefinitions[name] = list()
                    for stdTestName, actTestName in testDefs.items():
                        testSet = TSTestSet(name, stdTestName, actTestName)
                        testSet.init(testDefinitionPath)
                        self.__mTestDefinitions[name].append(testSet)

    @property
    def ConnectionString(self) -> str:
        return self.__mConnectionString

    @property
    def DifferenceFindMode(self) -> str:
        return self.__mDifferenceFindMode

    @property
    def CompareRevisions(self) -> list:
        return self.__mCompareTwoRevisions

    @property
    def ModifiedMDEFLocation(self) -> str:
        return self.__mModifiedMDEFLocation

    @property
    def IsFirstRevision(self) -> bool:
        return self.__mIsFirstRevision

    @property
    def MDEFP4Location(self) -> str:
        return self.__mMDEFLocation

    @property
    def TestDefinitionsP4Location(self) -> str:
        return self.__mTestDefinitionsLocation

    @property
    def TestDefinitions(self) -> dict:
        return self.__mTestDefinitions
