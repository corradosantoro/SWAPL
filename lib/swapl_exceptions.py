# -----------------------------------------------------------------
# swapl_exceptions.py
# -----------------------------------------------------------------

class InvalidTypeException(Exception):
    def __init__(self, uMessage):
        super().__init__(uMessage)
# -----------------------------------------------------------------
class UndefinedVarException(Exception):
    def __init__(self, uMessage):
        super().__init__(uMessage)
# -----------------------------------------------------------------
class UndefinedAttributeException(Exception):
    def __init__(self, uMessage):
        super().__init__(uMessage)
# -----------------------------------------------------------------
class UndefinedMethodException(Exception):
    def __init__(self, uMessage):
        super().__init__(uMessage)
# -----------------------------------------------------------------
class UndefinedFunctionException(Exception):
    def __init__(self, uMessage):
        super().__init__(uMessage)
# -----------------------------------------------------------------
class InvalidOpeningInstructionException(Exception):
    def __init__(self):
        super().__init__('A with block must begin with ParExecBegin instruction')
# -----------------------------------------------------------------
class InvalidClosingInstructionException(Exception):
    def __init__(self):
        super().__init__('A with block must end with ParExecEnd instruction')


