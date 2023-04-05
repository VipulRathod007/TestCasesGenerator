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
        self.__mValues = list()

    def addToResultSet(self, inValue):
        """Saves the result-set value after converting based on the data type"""
        if 'char' in self.mType.lower():
            self.__mValues.append(f"'{str(inValue)}'")
        elif 'time' in self.mType.lower() or 'date' in self.mType.lower():
            # TODO: Fix me
            pass
        else:
            self.__mValues.append(inValue)

    def getResultSet(self):
        return self.__mValues

    def setResultSet(self, inValues: list[str]):
        for val in inValues:
            self.addToResultSet(val)


class DBTable:
    def __init__(self, inCatalog: str, inSchema: str, inName: str):
        if isNoneOrEmpty(inCatalog) or isNoneOrEmpty(inSchema) or isNoneOrEmpty(inName):
            print(f'Error: Empty input to {self.__class__}')
        self.mCatalog = inCatalog
        self.mSchema = inSchema
        self.mName = inName
        self.mPrimaryKeys = dict()
        self.mColumns = dict()

    @property
    def FullName(self):
        return f'{self.mCatalog}.{self.mSchema}.{self.mName}'
