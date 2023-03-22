""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _TSTestSetWriter.py                                                                                        """
""" Contains the definition of TSTestSetWriter class                                                                 """
""" It's not a codebase if doesn't seem complex at first                                                             """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import sys

from TS.TSException import TSException
from TS.TestSets import TSTestSetFactory

from GenUtility import isNoneOrEmpty
from MDEF import MDEF


class TSTestSetWriter:
    def __init__(self, inTestDefinitions: dict, inTouchstoneRoot: str, inMDEF: MDEF, inResultSets: dict):
        if isNoneOrEmpty(inTestDefinitions) or isNoneOrEmpty(inTouchstoneRoot) or \
                isNoneOrEmpty(inMDEF) or isNoneOrEmpty(inResultSets):
            raise TSException('Empty/Invalid input provided')
        self.mTestDefinitions = inTestDefinitions
        self.mTouchstoneRoot = inTouchstoneRoot
        self.mMDEF = inMDEF
        self.mResultSets = inResultSets

    def write(self):
        factory = TSTestSetFactory()
        for testDef, testSets in self.mTestDefinitions.items():
            defInst = factory.create(testDef, testSets, self.mTouchstoneRoot, self.mMDEF, self.mResultSets)
            defInst.create()
