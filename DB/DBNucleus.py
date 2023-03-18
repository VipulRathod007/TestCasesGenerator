""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file DBNucleus.py                                                                                               """
""" Contains the definition of the various Database classes & containers                                             """
""" Re-use, It's good for Code and environment too :)                                                                """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from GenUtility import isNoneOrEmpty


# TODO: Add more containers as per need

class DBTable:
    def __init__(self, inCatalog: str, inSchema: str, inName: str):
        # TODO: Add validations if needed
        self.mCatalog = inCatalog
        self.mSchema = inSchema
        self.mName = inName

    @property
    def FullName(self):
        return f'{self.mCatalog}.{self.mSchema}.{self.mName}'
