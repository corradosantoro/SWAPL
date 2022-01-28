from termcolor import colored
from datetime import datetime
from os import system, name
import sys

LOG_COLORS = {
    "LOG": "blue",
    "INFO" : "cyan",
    "ERROR" :"red",
    "WARNING":"yellow",
    "SUCCESS" : "green"
}

class Console:

    @staticmethod
    def generateTimeString():
        now = datetime.now()
        return "["+now.strftime("%d/%m/%Y %H:%M:%S")+"]"

    @staticmethod
    def generateListStrings(type, time=False, what=None):
        listString = []
        if time:
            listString.append(Console.generateTimeString())

        strHead = colored('['+type+']', LOG_COLORS.get(type), attrs=['bold'])
        listString.append(strHead)

        if what is not None:
            listString.append(colored('['+what+']', LOG_COLORS.get(type)))

        return listString

    @staticmethod
    def log(*args, time=True, what=None):
        print(*(Console.generateListStrings("LOG", time, what) + list(args)), sep=" ")

    @staticmethod
    def info(*args, time=True, what=None):
        print(*(Console.generateListStrings("INFO", time, what) + list(args)), sep=" ")

    @staticmethod
    def warning(*args, time=True, what=None):
        print(*(Console.generateListStrings("WARNING", time, what) + list(args)), sep=" ")

    @staticmethod
    def error(*args, time=True, what=None):
        print(*(Console.generateListStrings("ERROR", time, what) + list(args)), sep=" ", file=sys.stderr)

    @staticmethod
    def success(*args, time=True, what=None):
        print(*(Console.generateListStrings("SUCCESS", time, what) + list(args)), sep=" ")

    @staticmethod
    def print(*args, color=None, attrs=[]):
        print(colored(str(*list(args)), color, attrs=attrs), sep=" ")

    @staticmethod
    def clear():

        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')
