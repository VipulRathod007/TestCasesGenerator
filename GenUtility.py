""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file GenUtility.py                                                                                              """
""" Contains the definition of the general utility methods                                                           """
""" Code re-use is a thing                                                                                           """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
from shutil import copy


def assure(inParam: dict, inArg: str, ignoreError: bool = False):
    """Assure if the given `inArg` is a key of `inParam`"""
    if inParam is not None and inArg in inParam and inParam[inArg] is not None:
        return inParam[inArg]
    else:
        # If set to True, No Exception would be thrown but would return False
        # in case given inArg is not a key of inParam
        if ignoreError:
            return False
        else:
            raise KeyError(f"Invalid Expression: {inParam}[{inArg}]")


def getEnvVariableValue(inVarName: str):
    """Returns Environment Variable's Value from the given key"""
    return assure(dict(os.environ), inVarName)


def checkFilesInDir(inDirPath: str, inFiles: list):
    """
    Checks whether given files are present or not in the specified Directory \n
    :param inDirPath: The specified Directory path
    :param inFiles: List of files to check
    :return: Returns True if all the given files are present in the specified directory else False
    """
    if os.path.exists(inDirPath) and os.path.isdir(inDirPath):
        if inFiles is not None and len(inFiles) > 0 and all(map(lambda x: x in os.listdir(inDirPath), inFiles)):
            return True
    return False


def copyFilesInDir(inSrcDirPath: str, inDestDirPath: str, inFiles: list):
    """
    Copies given files in the specified Directory \n
    :param inSrcDirPath: The specified Source Directory path
    :param inDestDirPath: The specified Destination Directory path
    :param inFiles: List of files to copy
    :return: Return True if succeeded else False
    """
    if os.path.exists(inSrcDirPath) and os.path.isdir(inSrcDirPath) and \
            os.path.exists(inDestDirPath) and os.path.isdir(inDestDirPath):
        try:
            [copy(os.path.join(inSrcDirPath, fileName), inDestDirPath) for fileName in inFiles]
            return True
        except FileNotFoundError as e:
            print('Error:', e)
            return False
    else:
        print(f'Invalid arguments: {inSrcDirPath} or {inDestDirPath}')
        return False

