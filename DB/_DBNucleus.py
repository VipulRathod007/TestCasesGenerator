""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _DBNucleus.py                                                                                              """
""" Contains the definition of the various Database classes & containers                                             """
""" Re-use, It's good for Code and environment too :)                                                                """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from GenUtility import isNoneOrEmpty


class DBPrimaryKey:
    def __init__(self, inName: str, inSeq: int, inPK: str):
        if isNoneOrEmpty(inName) or isNoneOrEmpty(inPK):
            print(f'Error: Empty input to {self.__class__}')
        self.mName = inName
        self.mSequence = inSeq
        self.mPKName = inPK


class DBColumn:
    def __init__(self, inName: str, inType: str):
        if isNoneOrEmpty(inName) or isNoneOrEmpty(inType):
            print(f'Error: Empty input to {self.__class__}')
        self.mName = inName
        self.mType = inType
        self.mValues = list()

    def setResultSet(self, inValues: list[str]):
        pass

    def getResultSet(self):
        return self.mValues


class DBTable:
    def __init__(self, inCatalog: str, inSchema: str, inName: str):
        if isNoneOrEmpty(inCatalog) or isNoneOrEmpty(inSchema) or isNoneOrEmpty(inName):
            print(f'Error: Empty input to {self.__class__}')
        self.mCatalog = inCatalog
        self.mSchema = inSchema
        self.mName = inName
        self.mPrimaryKeys = list()
        self.mColumns = list()

    @property
    def FullName(self):
        return f'{self.mCatalog}.{self.mSchema}.{self.mName}'
