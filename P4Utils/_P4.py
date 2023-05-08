""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _P4.py                                                                                                     """
""" Contains the definition of Perforce class                                                                        """
""" Never let Wrappers around wrappers wrap(hides) the originality                                                   """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import subprocess

from P4 import P4, P4Exception

from GenUtility import assure


class Perforce:
    """
    Initializes an instance of P4 and saves all P4 related info for later use in methods.
    Throws P4Exception if fails to connect.
    """

    def __init__(self):
        p4v = P4()
        try:
            with p4v.connect():
                info = p4v.run('info')
                self.__mP4Root = info[0]['serverRoot']
                self.__mP4Host = info[0]['clientHost']
                self.__mP4User = info[0]['userName']
                self.__mP4Client = info[0]['clientName']
                self.__mP4ClientRoot = info[0]['clientRoot']
                p4v.exception_level = 1
                self.__mP4Instance = p4v
        except P4Exception as p4e:
            raise PerforceException("Perforce connection error " + str(p4e))

    def transformPath(self, inPath: str):
        """
        Transforms and returns the given path to Perforce path if workspace path is given and vice versa
        """
        if inPath.startswith(self.__mP4ClientRoot):
            return '/' + inPath.replace(self.__mP4ClientRoot, '').replace('\\', '/')
        else:
            return os.path.abspath(self.__mP4ClientRoot + inPath)

    def markDirForAdd(self, inDirPath: str, inCLNum: int) -> int:
        """
        Marks each of the files under local directory path to add
        :param inCLNum: CL to add local files
        :param inDirPath: Local directory path
        :return: Total files added
        """

        def iterFiles(inPath: str) -> int:
            """
            Iterates through all the files and subdirectories recursively to add those to the CL
            :param inPath: Directory path to iterate
            :return: Total files count
            """
            count = 0
            for item in os.listdir(inPath):
                itemPath = os.path.abspath(os.path.join(inPath, item))
                if os.path.isdir(itemPath):
                    count += iterFiles(itemPath)
                elif os.path.isfile(itemPath):
                    self.markForAdd(str(inCLNum), itemPath)
                    count += 1
            return count

        return iterFiles(inDirPath)

    def createNewCL(self, inCLDescription: str):
        """Creates a new empty changelist and returns the changelist number."""
        try:
            with self.__mP4Instance.connect():
                newCL = self.__mP4Instance.save_change({
                    'Change': 'new',
                    'Description': inCLDescription
                })[0]
                return int(newCL.split()[1])  # returns the changelist number.
        except P4Exception as p4e:
            raise PerforceException("Perforce connection error " + str(p4e))

    def markForAdd(self, inCLNumber: str, *inFiles: str):
        """
        Opens file(s) for add within the cl_number specified.
        Equivalent of `p4 add -c cl_number file`.
        """
        try:
            with self.__mP4Instance.connect():
                for f in inFiles:
                    self.__mP4Instance.run_add('-c', inCLNumber, f)
        except P4Exception as p4e:
            raise PerforceException("Perforce connection error " + str(p4e))

    def markForDelete(self, inCLNumber: str, *inFiles: str):
        """
        Mark file(s) for delete within the cl_number specified.
        Equivalent of `p4 delete -c cl_number file`.
        """
        try:
            with self.__mP4Instance.connect():
                for f in inFiles:
                    self.__mP4Instance.run_delete('-c', inCLNumber, f)
        except P4Exception as p4e:
            raise PerforceException("Perforce connection error " + str(p4e))

    def checkout(self, inCLNumber: str, *inFiles: str):
        """
        Opens file(s) for edit within the cl_number specified.
        Equivalent of `p4 edit -c cl_number file`.
        """
        try:
            with self.__mP4Instance.connect():
                for f in inFiles:
                    self.__mP4Instance.run_edit('-c', inCLNumber, f)
        except P4Exception as p4e:
            raise PerforceException("Perforce connection error " + str(p4e))

    def createLabel(self, inLabelName: str, inLabelDescription: str, inViews: list, inOptions='unlocked'):
        """
        Creates a new label.
        """
        try:
            with self.__mP4Instance.connect():
                newLabel = self.__mP4Instance.run_label('-o', inLabelName)[0]
                newLabel['Description'] = inLabelDescription
                newLabel['Options'] = inOptions
                newLabel['Owner'] = self.__mP4User
                newLabel['View'] = inViews.copy()
                self.__mP4Instance.input = newLabel
                self.__mP4Instance.run_label('-i')
        except P4Exception as p4e:
            raise PerforceException("Perforce connection error " + str(p4e))

    def tagToLabel(self, inLabelName: str, inView: str, inRevision: str = 'head'):
        revision = f'#{inRevision}' if inRevision == 'head' else f'@{inRevision}'
        try:
            with self.__mP4Instance.connect():
                # Built-in tag function fails to tag correctly when used with specific revision
                subprocess.run(f'p4 tag -l {inLabelName} {inView}{revision}')
        except P4Exception as p4e:
            raise PerforceException("Perforce connection error " + str(p4e))

    def submit(self, inCLNumber: int):
        """Submit a changelist given it's number."""
        try:
            with self.__mP4Instance.connect():
                self.__mP4Instance.run_submit('-c', str(inCLNumber))
        except P4Exception as p4e:
            raise PerforceException("Perforce connection error " + str(p4e))

    def fetchLabel(self, inLabelName):
        try:
            with self.__mP4Instance.connect():
                return self.__mP4Instance.fetch_label(inLabelName)
        except P4Exception as p4e:
            raise PerforceException("Perforce connection error " + str(p4e))

    def lockLabel(self, inLabelName: str):
        """Creates a new label."""
        try:
            with self.__mP4Instance.connect():
                newLabel = self.__mP4Instance.run_label('-o', inLabelName)[0]
                newLabel['Options'] = 'locked'
                self.__mP4Instance.input = newLabel
                self.__mP4Instance.run_label('-i')
        except P4Exception as p4e:
            raise PerforceException("Perforce connection error " + str(p4e))

    def getRevision(self, inPath: str, inRevision: str = 'head', inForceRev: bool = False):
        """
        To get particular revision of file from P4V
        :param inForceRev: Flag to force revision
        :param inPath: Path of file or directory to get
        :param inRevision: Revision of file.
        """
        try:
            with self.__mP4Instance.connect():
                if inForceRev:
                    self.__mP4Instance.run(
                        'sync', '-f', f'{inPath}...' if inRevision == 'head' else f'{inPath}...@{inRevision}'
                    )
                else:
                    self.__mP4Instance.run(
                        'sync', f'{inPath}...' if inRevision == 'head' else f'{inPath}...@{inRevision}'
                    )
        except P4Exception as p4e:
            raise PerforceException("Perforce connection error " + str(p4e))

    def integrate(self, inSource: str, inTarget: str, inCLNum: int):
        """Equivalent to Merge/Integrate files"""
        try:
            with self.__mP4Instance.connect():
                self.__mP4Instance.run('integrate', '-c', str(inCLNum), inSource, inTarget)
        except P4Exception as p4e:
            raise PerforceException(f'Perforce Exception: {p4e}')

    def shelve(self, inCLNum: int):
        """Equivalent to shelve"""
        try:
            with self.__mP4Instance.connect():
                self.__mP4Instance.run('shelve', '--parallel=0', '-f', '-Af', '-c', str(inCLNum))
        except P4Exception as p4e:
            raise PerforceException(f'Perforce Exception: {p4e}')

    def getLatestRevisionNumber(self, inFilePath: str):
        """
        Finds the latest revision number of the file \n
        :param inFilePath: Path of the file to get latest revision number
        :return: Returns the latest revision number of the specified file
        """
        if os.path.exists(inFilePath):
            try:
                with self.__mP4Instance.connect():
                    result = self.__mP4Instance.run('fstat', os.path.abspath(inFilePath))[0]
                    return int(assure(result, 'headRev'))
            except P4Exception as p4e:
                raise PerforceException(f'Perforce Exception: {p4e}')
        else:
            raise FileNotFoundError(f"{inFilePath} is an invalid location")

    def readRevision(self, inFilePath: str, inFileRevision: int = None):
        """
        Reads a file from Perforce with the latest revision if revision not specified \n
        :param inFilePath: Perforce Path of the file to get revision
        :param inFileRevision: Revision Number of a file to get
        :return: Returns the File content
        """
        try:
            with self.__mP4Instance.connect():
                if inFileRevision is not None:
                    fileContent = subprocess.check_output(
                        ['p4.exe', 'print', '-q', f"{os.path.abspath(inFilePath)}#{inFileRevision}"]
                    ).decode()
                else:
                    fileContent = subprocess.run(['print', '-q', os.path.abspath(inFilePath)]).stdout.decode()
            return fileContent
        except P4Exception as p4e:
            raise PerforceException("Perforce connection error " + str(p4e))


class PerforceException(Exception):
    pass
