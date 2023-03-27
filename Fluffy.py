import sys

from TS import TSRunner
from TS import TSExecutionMode as TSMode


def help():
    print('To use TestCasesGenerator,\n'
          'run "python Fluffy.py <input-json file path> <execution mode>"\n'
          'Refer readme.md to get mode info on input-json file\n'
          'Execution modes:\n'
          ' 1. -ts: Generates test cases only\n'
          ' 2. -rs: Generates test cases & result-sets both\n'
          '\n'
          'Use -h/-help to get help')


def main(inFilePath: str, inMode: str):
    try:
        if inMode.lower() == TSMode.TestSet.value:
            TSRunner(inFilePath).run(TSMode.TestSet)
        elif inMode.lower() == TSMode.ResultSet.value:
            TSRunner(inFilePath).run(TSMode.ResultSet)
        else:
            print("Error: Invalid Mode provided")
            help()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # if len(sys.argv) < 3:
    #     if len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '-help'):
    #         help()
    #     else:
    #         print("Error: Invalid Input provided\n"
    #               f"Use python Fluffy.py -h/-help to get help")
    #     sys.exit(1)
    # inputFile = sys.argv[1]
    # mode = sys.argv[2]

    main('input.json', '-ts')
    # main(inputFile, mode)
