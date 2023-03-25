""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file _TSException.py                                                                                            """
""" Contains the definition of TSException class                                                                     """
""" Every Code does the wonder or makes you wonder ;)                                                                """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import random
import sys


class TSException(Exception):
    """
    Represents TSException class
    """

    def __init__(self, inErrorMessage: str):
        try:
            self.__mErrorPrefix = 'TSException'
            if len(inErrorMessage) == 0:
                raise TSException('Inception of Exception. Empty Error message')
            super(TSException, self).__init__(
                f'{self.__mErrorPrefix} - {inErrorMessage}\n'
                f'{self.getFluffyMessage()}'
            )
        except TSException as e:
            print(e)
            sys.exit(1)

    @staticmethod
    def getFluffyMessage():

        fluffySays = [
            "Buddy, It's high time you've a coffee break",
            "Do what you love, love what you do!",
            "Ahhh, Humans after all...!",
            "Sometimes you play with code and sometimes code... ;)"
        ]

        return random.choice(fluffySays)
