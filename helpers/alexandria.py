from os import listdir, mkdir
from os.path import isfile, join, isdir
from pprint import pprint
import json

# basePath = """//alexandria.rutgers.edu/makerspace-shared/!3D Prints/"""
basePath = """./Prints/"""

# This is intended to run on a windows
# computer with access to the drive
# already mapped.  This means my laptop
# or the desktop in 3D Printing.  This
# could potentially change but it'd be annoying.
def produceUsers() -> list:
    return [x for x in listdir(basePath) if isdir(join(basePath, x))]


def produceUserSubmissions(userString: str) -> list:
    # print(join(basePath, userString))
    q = [x for x in listdir(join(basePath, userString))]

    output = []

    for d in q:
        temp = join(join(basePath, userString), d)
        if isdir(temp):
            output.append(d)
    return output


def readDataFromFile():
    return json.loads(open("./db/alexandria.json", "r").read())


def produceToFileParentInfo():
    userFolders = produceUsers()

    # print(userFolders)

    output = []
    for u in userFolders:
        g = []
        if g := produceUserSubmissions(u):
            output.append({"user": u, "dates": g})

    with open("./db/alexandria.json", "w") as alex:
        alex.write(json.dumps(output, indent=4))

    print("[debug] Produced list of users and projects from alexandria.")


def produceJobsMetadata():
    usersDirectories = readDataFromFile()

    usersFlat = []

    for u in [q["user"] for q in usersDirectories]:
        tempPath = join(basePath, u)
        if not isfile(join(tempPath, "userinfo.json")):
            with open(join(tempPath, "userinfo.json"), "w") as userdata:
                userdata.write(
                    json.dumps(
                        {"name": None, "email": None, "netid": None, "shadow": True}
                    )
                )
            print("[debug] Wrote user profile empty of {}".format(u))

    for u in usersDirectories:
        user = u["user"]
        for d in u["dates"]:
            folder = d

            fullPath = join(join(basePath, user), folder)

            usersFlat.append(fullPath)

    for u in usersFlat:
        if not isfile(join(u, "jobdata.json")):
            with open(join(u, "jobdata.json"), "w") as jobdata:
                jobdata.write(json.dumps({}))
                print("Wrote {}".format(u))


def userExists(userString: str) -> bool:
    return isdir(join(basePath, userString))


def userFolderExists(userString: str, userFolderString: str) -> bool:
    return isdir(join(join(basePath, userString), userFolderString))


def makeUserFolder(userString: str) -> None:
    mkdir(join(basePath, userString))


def makeUserProjectFolder(userString: str, userFolderString: str) -> None:
    mkdir(join(join(basePath, userString), userFolderString))


def getValidPrintUsers(onlyValid: bool = True) -> list:
    with open(join(basePath, "makerspaceStaff.json"), "r") as staff:
        return json.loads(staff.read())


def addValidPrintUsers(newUser: dict) -> None:
    # newUser must contain stringName: str, isActive: bool
    if not isfile(join(basePath, "makerspaceStaff.json")):
        users = [newUser]
        with open(join(basePath, "makerspaceStaff.json"), "w") as qg:
            qg.write(json.dumps(users))
    else:
        currentUsers = json.loads(
            open(join(basePath, "makerspaceStaff.json"), "r").read()
        )
        currentUsers.append(newUser)

        with open(join(basePath, "makerspaceStaff.json"), "w") as qg:
            qg.write(json.dumps(currentUsers))
