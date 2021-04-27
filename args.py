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


def isOnline():
    if "--online" in sys.argv[1:]:
        return True
    return False


def isContainingGameId():
    if "--server" in sys.argv[1:] and "--name" in sys.argv[1:]:
        if "--game" in sys.argv[1:]:
            return True
        else:
            return False


def areParametersValid():
    if isContainingGameId():
        if len(sys.argv) >= 8:
            return True
        else:
            return False
    else:
        if len(sys.argv) >= 6:
            return True
        else:
            return False

def getParams():
    params = {
        "server": None,
        "name": None,
        "gameId": None
    }
    i = 0
    while i < len(sys.argv):
        if(sys.argv[i] == "--server"):
            params["server"] = sys.argv[i + 1]
        elif sys.argv[i] == "--name":
            params["name"] = sys.argv[i + 1]
        elif sys.argv[i] == "--game":
            params["gameId"] = sys.argv[i + 1]
        i += 1
    return params