""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file GenUtility.py                                                                                              """
""" Contains the definition of the general utility methods                                                           """
""" Code re-use is a thing                                                                                           """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import errno
import os
import sys
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


def createDir(inDirPath: str, inMode: int = 0o777):
    """Creates the absent directories from the given path."""
    try:
        os.makedirs(inDirPath, inMode)
    except OSError as err:
        # Re-raise the error unless it's for already existing directory
        if err.errno != errno.EEXIST or not os.path.isdir(inDirPath):
            raise


def getEnvVariableValue(inVarName: str):
    """Returns Environment Variable's Value from the given key"""
    return assure(dict(os.environ), inVarName)


def isNoneOrEmpty(inVal) -> bool:
    """Checks if the given value is None or Empty"""
    if inVal is None:
        return True
    elif isinstance(inVal, str):
        return inVal is None or len(inVal) == 0
    elif isinstance(inVal, dict):
        return inVal is None or \
               len(inVal) == 0 or \
               all(map(lambda x: isNoneOrEmpty(x) and isNoneOrEmpty(inVal[x]), inVal))
    elif isinstance(inVal, list):
        return inVal is None or \
               len(inVal) == 0 or \
               all(map(lambda x: isNoneOrEmpty(x), inVal))
    else:
        return isNoneOrEmpty(str(inVal))


def writeFile(inContent: str, inPath: str, inMode: str = 'w'):
    """
    Writes to the file
    :param inContent: Content to write
    :param inPath: Path of the file
    :param inMode: Mode to write to the file. Default 'w'
    """
    try:
        with open(inPath, inMode) as file:
            file.write(inContent.replace('\t', '    '))
    except Exception as error:
        print(f'Error at {__name__}: {error}')
        sys.exit(1)


def readFile(inPath: str, inMode: str = 'r'):
    """
    Reads from the file
    :param inPath: Path of the file
    :param inMode: Mode to write to the file. Default 'r'
    """
    content = None
    try:
        with open(inPath, inMode) as file:
            content = file.read()
    except Exception as error:
        print(f'Error at {__name__}: {error}')
        sys.exit(1)
    return content
