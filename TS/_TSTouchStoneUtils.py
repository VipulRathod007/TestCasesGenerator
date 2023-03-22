""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _TSTouchStoneUtils.py                                                                                      """
""" Contains the definition of TSTouchStoneUtils class                                                               """
""" Write Codes, not Einstein's theory of relativity                                                                 """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import sys
from shutil import copy

from GenUtility import createDir, isNoneOrEmpty, getEnvVariableValue


class TSTouchStoneUtils:

    @classmethod
    def setup(cls, inRoot: str, inTestDefinitions: list):
        """
        Sets up the Touchstone directory with given test definitions and
        copies Touchstone artifacts from `TOUCHSTONE_DIR`
        :param inRoot: Root directory to set up Touchstone at.
        :param inTestDefinitions: List of Test Definitions
        """
        if isNoneOrEmpty(inRoot) or isNoneOrEmpty(inTestDefinitions):
            print(f'Error: Empty/Invalid input provided to {cls.__class__.__name__}')
            sys.exit(1)
        outputDir = os.path.join(os.path.abspath(inRoot), 'Output')
        touchstoneDir = getEnvVariableValue('TOUCHSTONE_DIR')

        createDir(outputDir)
        copy(os.path.join(touchstoneDir, 'Touchstone.exe'), outputDir)
        copy(os.path.join(touchstoneDir, 'sbicudt58_64.dll'), outputDir)
        copy(os.path.join(touchstoneDir, 'sbicuuc58d_64.dll'), outputDir)

        createDir(os.path.join(outputDir, 'Envs'))
        for testDef in inTestDefinitions:
            createDir(os.path.join(outputDir, testDef))
            createDir(os.path.join(outputDir, testDef, 'TestSets'))
            createDir(os.path.join(outputDir, testDef, 'ResultSets'))
