""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file TSException.py                                                                                             """
""" Contains the definition of TSException class                                                                     """
""" Every Code does the wonder or make you wonder ;)                                                                 """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import random
import sys


class TSException(Exception):
    """
    Represents TSException class
    """

    def __init__(self, inErrorMessage: str):
        try:
            if len(inErrorMessage) == 0:
                raise TSException('Inception of Exception. Empty Error message')
            self.__mErrorMessage = inErrorMessage
        except TSException as e:
            print(e)
            sys.exit(1)

    def __str__(self):
        return f'[TSException] - {self.__mErrorMessage}\n' \
               f'{self.getFluffyMessage()}'

    @staticmethod
    def getFluffyMessage():

        s_FluffySays = [
            "Buddy, It's high time you've a coffee break",
            "Do what you love, love what you do!",
            "Ahhh, Humans after all...!",
            "Sometimes you play with code and sometimes code... ;)"
        ]

        return random.choice(s_FluffySays)
