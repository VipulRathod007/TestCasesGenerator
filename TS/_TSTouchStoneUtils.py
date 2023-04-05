""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _TSTouchStoneUtils.py                                                                                      """
""" Contains the definition of TSTouchStoneUtils class                                                               """
""" Write Codes, not Einstein's theory of relativity                                                                 """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import sys
import subprocess
from shutil import copy

from GenUtility import createDir, isNoneOrEmpty, getEnvVariableValue, writeFile
from TS._TSException import TSException


class TSTouchStoneUtils:

    @classmethod
    def setup(cls, inRoot: str, inTestDefinitions: list, inConnectionString: str):
        """
        Sets up the Touchstone directory with given test definitions and
        copies Touchstone artifacts from `TOUCHSTONE_DIR`
        :param inRoot: Root directory to set up Touchstone at
        :param inTestDefinitions: List of Test Definitions
        :param inConnectionString: Connection string to be added in the file
        """
        if isNoneOrEmpty(inRoot) or isNoneOrEmpty(inTestDefinitions):
            raise TSException(f'Error: Empty/Invalid input provided to {cls.__class__.__name__}')

        outputDir = os.path.abspath(inRoot)
        touchstoneDir = getEnvVariableValue('TOUCHSTONE_DIR')

        createDir(outputDir)
        copy(os.path.join(touchstoneDir, 'Touchstone.exe'), outputDir)
        copy(os.path.join(touchstoneDir, 'sbicudt58_64.dll'), outputDir)
        copy(os.path.join(touchstoneDir, 'sbicuuc58d_64.dll'), outputDir)

        createDir(os.path.join(outputDir, 'Envs'))
        TSTouchStoneUtils.createTestEnv(inRoot, inConnectionString)
        for testDef in inTestDefinitions:
            createDir(os.path.join(outputDir, testDef))
            createDir(os.path.join(outputDir, testDef, 'TestSets'))
            createDir(os.path.join(outputDir, testDef, 'ResultSets'))

    @classmethod
    def createTestEnv(cls, inRoot: str, inConnectionString: str):
        """
        Creates TestEnv.xml at <Root>/Envs/TestEnv.xml location
        :param inRoot: Root directory to set up Touchstone at
        :param inConnectionString: Connection string to be added in the file
        """
        if isNoneOrEmpty(inRoot) or isNoneOrEmpty(inConnectionString):
            raise TSException(f'Error: Empty/Invalid input provided to {cls.__class__.__name__}')

        testEnvDir = os.path.join(inRoot, 'Envs')
        createDir(testEnvDir)

        content = ''
        content += '<?xml version="1.0" encoding="utf-8"?>\n'
        content += '<TestEnvironment>\n'
        content += f'\t<ConnectionString>{inConnectionString}</ConnectionString>\n'
        content += '\t<SqlWCharEncoding>UTF-32</SqlWCharEncoding>\n'
        content += '\t<GenerateResults>true</GenerateResults>\n'
        content += '</TestEnvironment>'

        writeFile(content, os.path.join(testEnvDir, 'TestEnv.xml'))

    @classmethod
    def run(cls, inRoot: str, inTestSuites: list):
        """Runs TouchStone for given test-suites"""
        if isNoneOrEmpty(inRoot) or isNoneOrEmpty(inTestSuites):
            raise TSException(f'Error: Empty/Invalid input provided to {cls.__class__.__name__}')

        for testSuite in inTestSuites:
            cmd = f'Touchstone.exe -te Envs\TestEnv.xml -ts {testSuite}\TestSuite.xml -o {testSuite}'
            try:
                print(cmd)
                print('Info: Touchstone started')
                subprocess.run(cmd, cwd=inRoot, shell=True)
                print()
            except Exception as error:
                raise TSException(str(error))
