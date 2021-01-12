import json
import time
import hashlib


class DataProvider:
    def __init__(self):
        self.printDB = "prints.json"

    # This function tests whether the database exists or not.
    # If it does, it loads and sends it to the function caller.
    # If not, it makes a empty one via makePrintDB().
    def dbExists(self, debug=False):
        try:
            printJSON = json.loads(open(self.printDB).read())
            if debug:
                print("DB exists!")
            return True, printJSON
        except:
            if debug:
                print("Doesn't exist, making now.")
            makePrintDB()
            if debug:
                print("DB made.")
            printJSON = json.loads(open(self.printDB).read())
            return False, printJSON

    # Simple helper function.
    def makePrintDB(self):
        with open(self.printDB, "w") as prints:
            prints.write(json.dumps([]))

    # This is a wrapper for a lambda we expect to use for multiple renderers.
    def sortDB(self, inputData, reverse=False):
        inputData = sorted(
            inputData, key=lambda x: (x["unixTime"], x["hash"]), reverse=reverse
        )
        return inputData

    # Helper function for main page.
    def getPrints(self, howMany=20):
        dbE = self.dbExists()
        if dbE[0]:
            printsJSON = self.sortDB(dbE[1])

            if howMany == -1:
                return printsJSON
            else:
                return printsJSON[:howMany]

    def addPrint(self, printData):
        dbE = self.dbExists(True)
        if dbE[0]:
            printJSON = self.sortDB(dbE[1])
            
        printData["unixTime"] = time.time()
        if "printHistory" not in printData:
            printData["printHistory"] = []

        printData["hash"] = str(
            hashlib.md5(str.encode(str(printData))).hexdigest()
        )  # This allows us to uniquely address each item, and the time difference ensures different times of the same contents get different prints.

        printJSON.append(printData)

        with open(self.printDB, "w") as x:
            x.write(json.dumps(printJSON))

    # Returns the contents of a print info dump
    # only by the hash.
    
    def editPrint(self, hash, item):
        dbItems = self.getPrints(-1)
        
        for k,v in enumerate(dbItems):
            if v['hash'] == hash:
                dbItems[k] = item
                
        with open(self.printDB, "w") as x:
            x.write(json.dumps(dbItems))

    def getPrintByHash(self, hash):
        printJSON = self.getPrints(-1)
        printJSON = list(filter(lambda x: x["hash"] == hash, printJSON))
        if len(printJSON) != 0:
            return printJSON[0]
        else:
            return None

    # This function finds a print in-line
    # the JSON store by hash, if there is
    # no history, adds one.  In doing so,
    # We have a timestamped and ordered log
    # to keep track of what happened to a print.
    def addPrintLog(self, hash, action, note):
        printToModify = self.getPrintByHash(hash)
        if "printHistory" not in printToModify:
            printToModify["printHistory"] = []

        history = {}
        history["action"] = action
        history["note"] = note
        history["unixTime"] = time.time()

        printToModify["printHistory"].append(history)

        printJSON = json.loads(open(self.printDB).read())

        for key, item in enumerate(printJSON):
            if item["hash"] == printToModify["hash"]:
                printJSON[key] = printToModify

        with open(self.printDB, "w") as x:
            x.write(json.dumps(printJSON))
