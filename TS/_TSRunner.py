""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _TSRunner.py                                                                                               """
""" Contains the definition of TSRunner class                                                                        """
""" Code is a piece of `art`                                                                                         """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import json
import os
from enum import Enum

from DB import DBWrapper
from P4Utils import Perforce
from TS._TSException import TSException
from TS.TestSets import TSTestSetWriter
from TS._TSInputReader import TSInput, Constants
from TS._TSTouchStoneUtils import TSTouchStoneUtils

from MDEF import MDEF
from GenUtility import readFile


class TSExecutionMode(Enum):
    """
    Enum class represent Execution modes
    Mapped values represent mode shorthands
    """
    TestSet = '-ts'
    ResultSet = '-rs'


class TSRunner:
    """
    Represents Main application runner class
    """

    def __init__(self, inFilePath: str):
        if not os.path.exists(inFilePath):
            raise TSException(f'Error: {inFilePath} not found')
        self.__mFilePath = inFilePath
        self.__mInput = TSInput(inFilePath)
        self.__mP4Inst = Perforce()

    def run(self, inMode: TSExecutionMode):
        print('=======================================================================================================')
        print(f'                     TestCasesGenerator started running with {inMode.name} mode')
        print('=======================================================================================================')
        touchStoneRoot = os.path.join(os.path.abspath(os.curdir), 'Output')
        mdefDiff = self.__findSchemaDifferences()
        db = DBWrapper(self.__mInput.ConnectionString)
        dbTables = db.init(mdefDiff.AllTableNames)
        print('=======================================================================================================')
        print('                                        Database initialized')
        print('=======================================================================================================')
        TSTouchStoneUtils.setup(
            touchStoneRoot, list(self.__mInput.TestDefinitions.keys()), self.__mInput.ConnectionString
        )
        writer = TSTestSetWriter(self.__mInput.TestDefinitions, touchStoneRoot, mdefDiff, dbTables)
        writer.write()
        print('=======================================================================================================')
        print('                                    Testcases generation completed')
        print('=======================================================================================================')

        if inMode.value == TSExecutionMode.ResultSet.value:
            TSTouchStoneUtils.run(touchStoneRoot, list(self.__mInput.TestDefinitions.keys()))
        db.disconnect()

    def __findSchemaDifferences(self) -> MDEF:
        mdefPath = self.__mP4Inst.transformPath(self.__mInput.MDEFP4Location)
        if self.__mInput.DifferenceFindMode == Constants.ModifiedMDEFLocation.value:
            modifiedMDEF = MDEF()
            modifiedMDEF.parse(readFile(self.__mInput.ModifiedMDEFLocation))
            if self.__mInput.IsFirstRevision:
                return modifiedMDEF
            latestMDEF = MDEF()
            latestMDEF.parse(readFile(mdefPath))

            return modifiedMDEF - latestMDEF
        elif self.__mInput.DifferenceFindMode == Constants.CompareTwoRevisions.value:
            olderMDEF = MDEF()
            # Since 0th index will have lower revision representing older mdef
            # while 1st represents the latest one
            olderMDEF.parse(json.loads(self.__mP4Inst.readRevision(mdefPath, self.__mInput.CompareRevisions[0])))
            newerMDEF = MDEF()
            newerMDEF.parse(json.loads(self.__mP4Inst.readRevision(mdefPath, self.__mInput.CompareRevisions[1])))

            return newerMDEF - olderMDEF
