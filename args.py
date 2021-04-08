import sys
def isDebug():
    if "--debug" in sys.argv[1:]:
        return True
    return False

def isHelpWanted():
    if "--help" in sys.argv[1:]:
        return True
    return False

def isMultiplayer():
    if "--multiplayer" in sys.argv[1:]:
        return True
    return False
