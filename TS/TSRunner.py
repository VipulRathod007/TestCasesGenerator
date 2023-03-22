""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file TSRunner.py                                                                                                """
""" Contains the definition of TSRunner class                                                                        """
""" Code is a piece of `art`                                                                                         """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
from enum import Enum

from DB import DBWrapper
from P4Utils import Perforce
from .TSException import TSException
from ._TSInputReader import TSInput, Constants
from ._TSTouchStoneUtils import TSTouchStoneUtils

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
        mdefDiff = self.__findSchemaDifferences()
        dbTables = DBWrapper(self.__mInput.ConnectionString).init()
        TSTouchStoneUtils.setup(os.curdir, list(self.__mInput.TestDefinitions.keys()))

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
            olderMDEF.parse(self.__mP4Inst.readRevision(mdefPath, self.__mInput.CompareRevisions[0]))
            newerMDEF = MDEF()
            newerMDEF.parse(self.__mP4Inst.readRevision(mdefPath, self.__mInput.CompareRevisions[1]))

            return newerMDEF - olderMDEF
