import sys
def isDebug():
    if "--debug" in sys.argv[1:]:
        return True