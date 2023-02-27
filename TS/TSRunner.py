""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file TSRunner.py                                                                                                """
""" Contains the definition of TSRunner class                                                                        """
""" Code is a piece of `art`                                                                                         """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
from enum import Enum

from .TSException import TSException


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

    def run(self, inMode: TSExecutionMode):
        print(inMode)
