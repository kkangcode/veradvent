import re
import math
import random
import datetime

class ProgressBar:
    def __init__(self, finishPoint, noOverfill):
        self.currentPosition = 0
        self.finishPoint = finishPoint
        self.noOverfill = noOverfill

    def updatePosition(self, addPosition):
        self.currentPosition = self.currentPosition + addPosition
        #With noOverfill flag set to true, if the amount is over the progress bar, set to finish point instead
        if ((self.currentPosition > self.finishPoint) & (self.noOverfill == True)):
            self.currentPosition = self.finishPoint
        elif(self.currentPosition < 0):
            #For now, do not allow negative values for the progress bar
            self.currentPosition = 0

    def showProgressBar(self, showPercent):
        #Example of Progress Bar: [************--------] 60% (20 characters long)
        #For the bar, round down to the nearest 5%
        #For the percentage, round down to the nearest 1%
        progressPercent = math.floor(self.currentPosition/ self.finishPoint * 100)
        progressCount = math.floor(self.currentPosition / self.finishPoint * 20)

        #Generate the progress bar as a string to return
        progressBar = "["
        for x in range(1, 21):
            if (x <= progressCount):
                progressBar = progressBar + "#"
            else:
                progressBar = progressBar + "-"
        progressBar = progressBar + "]"

        #If set to true, show the percentage, if not show a fraction instead
        if (showPercent == True):
            progressBar = progressBar + " " + str(progressPercent) + "%"
        else:
            progressBar = progressBar + " " + str(self.currentPosition) + " / " + str(self.finishPoint)

        return progressBar

class MultipleChoice:
    def __init__(self, title, choices, randomOn):
        self.title = title
        self.choices = ["Empty"]
        #Adding choices is done through the append (since it is a list), there is no dedicated procedure for it
        if (randomOn == True):
            self.choices[0] = "Random"
            self.choices = self.choices + choices
        else:
            self.choices = choices

    def displayChoices(self):
        #The choices will start from 1 rather than 0 (make it easier on a regular keyboard)
        #The indices of the choices will still start at 0, the offset will be taken care of
        x = 1
        print("\n" + self.title)
        for currentOption in self.choices:
            print(str(x) + " ) " + currentOption)
            x = x + 1

    def selectChoice(self, returnIndex):
        validChoice = False
        selectedChoice = ""
        while (validChoice == False):
            self.displayChoices()
            selectNum = input("Choose: ")
            if (selectNum.isnumeric() == False):
                print("Invalid Choice, Select Again")
            else:
                selectInt = int(selectNum)
                #Check to see if the number is within range
                #The +1 is to help include the upper bound of the selection
                if ((selectInt > 0) & (selectInt < len(self.choices) + 1)):
                    validChoice = True
                    if (self.choices[selectInt - 1] == "Random"):
                        #Starting at 2 because 1 is the random option
                        selectInt = random.randint(2, len(self.choices))
                    #The -1 is to offset (since the choices begin at 1 rather than 0)
                    selectedChoice = self.choices[selectInt - 1]
                    print("\nSelected: " + self.choices[selectInt - 1])
                else:
                    print("Invalid Choice, Select Again")

        #Return the selected index if needed, otherwise return the string of the object
        if (returnIndex == True):
            selectedChoice = selectInt - 1
        return selectedChoice

#There can be multiples of an item
#Note: "∞" can be used for infinite uses
class Item:    
    def __init__(self, name, effect, count, value, description, price):
        self.name = name
        self.effect = effect
        self.count = count
        self.value = value
        self.description = description
        self.price = price

    def checkItem(self):
        print("\n" + self.name + " (" + str(self.count) + ")")
        print("Effect: " + self.effect)
        print(self.description + "\n")

#This is for both weapons and spells
class Attack:
    def __init__(self, name, type, attackPower, manaCost):
        self.name = name
        self.type = type
        self.attackPower = attackPower
        self.manaCost = manaCost

class Arsenal:
    def __init__(self, title):
        self.title = title
        self.case = []
        self.list = MultipleChoice(title, [], False)
        self.case.append(Attack("BackMainMenu", "None", 0, 0))
        self.list.choices.append("Back to Main Menu")

    def addAttack(self, name, type, attackPower, manaCost):
        self.case.append(Attack(name, type, attackPower, manaCost))
        self.list.choices.append(name + " (Atk: " + str(attackPower) + " / Mana: " + str(manaCost) + ")")

    def chooseAttack(self, chooseDefault):
        if (chooseDefault == True):
            #Return the first attack listed, which will be index 1 since the 'back to main menu' takes slot 0
            return self.case[1]
        #Get the index of the attack
        pickAttack = self.list.selectChoice(True)
        return self.case[pickAttack]

#This will keep track of the current state of the hero's party, enemy's party, turn count, and other things
class StagingArea:
    def __init__(self, maxTurnCount, debugLogName):
        self.turnCount = ProgressBar(maxTurnCount, True)
        self.heroParty = Roster("Hero's Party")
        self.enemyParty = Roster("Enemy's Party")
        self.debugLog = DebugLog(debugLogName)

class Inventory:
    def __init__(self, title):
        self.title = title
        self.storage = []
        self.list = MultipleChoice(title, [], False)
        self.storage.append(Item("BackMainMenu", "None", "∞", 0, "Back to Main Menu", 0))
        self.list.choices.append("Back to Main Menu")

    def addItem(self, newItem, quantity, showPrice):
        #Need to check if the thing is an actual item
        if (isinstance(newItem, Item)):
            #First check to see if the item already exists in the inventory, if so then stack it
            checkIndex = 0
            for checkItem in self.storage:
                if (checkItem.name == newItem.name):
                    self.storage[checkIndex].count = self.storage[checkIndex].count + quantity
                    if (showPrice == True):
                        #Show the price if it is a venue
                        self.list.choices[checkIndex] = checkItem.name + " (Cost: " + str(self.storage[checkIndex].price) + ")"
                    else:
                        #Update the string in the list to reflect the updated quantity
                        self.list.choices[checkIndex] = checkItem.name + " (" + str(self.storage[checkIndex].count) + ")"
                    return None
                else:
                    checkIndex = checkIndex + 1

            #If it doesn't exist, then add item to the storage
            #Adjust the quantity based on the function input (since an item can have an infinite count when buying)
            newItem.count = quantity
            self.storage.append(newItem)
            #Add item to the list
            if (showPrice == True):
                #Show the price if it is a venue
                self.list.choices.append(newItem.name + " (Cost: " + str(newItem.price) + ")")
            else:
                self.list.choices.append(newItem.name + " (" + str(newItem.count) + ")")
        else:
            print("This is not a valid Item object")

    def listInventory(self):
        self.list.displayChoices()

    def selectItem(self, stagingArea):
        pickItem = self.list.selectChoice(True)

        #Need to decrease the count in the inventory (if it has finite uses)
        if (self.storage[pickItem].count != "∞"):
            self.storage[pickItem].count = self.storage[pickItem].count - 1

        #Store the item details later (since it might be removed if it is the last instance of the item)
        pickedItem = self.storage[pickItem]

        if (pickedItem.name == "BackMainMenu"):
            #User wants to go back to the main menu, no need to go through the rest of the procedure
            return pickedItem.name

        #Use the item
        if (self.storage[pickItem].effect == "Heal"):
            #For now, use the item only on the user
            stagingArea.heroParty.healChar(self.storage[pickItem].value)
        
        #If the count goes to 0, then remove it from the inventory
        if (self.storage[pickItem].count == 0):
            self.removeItem(pickItem)
        else:
            #Update the string with the updated count
            self.list.choices[pickItem] = self.storage[pickItem].name + " (" + str(self.storage[pickItem].count) + ")"
        
        return pickedItem
        
    def removeItem(self, removeIndex):
        #Item needs to be removed from the storage and list
        self.storage.pop(removeIndex)
        self.list.choices.pop(removeIndex)

class Character:
    def __init__(self, name, startHealth, startMana, classType, elementalType, baseAttack, baseDefense):
        self.name = name
        self.health = ProgressBar(startHealth, True)
        self.health.updatePosition(startHealth)
        self.mana = ProgressBar(startMana, True)
        self.mana.updatePosition(startMana)
        self.status = "OKAY"
        self.backpack = Inventory(self.name + "'s Backpack")
        self.arsenalCase = Arsenal("Attacks")
        #Every character will have an infinite 'normal attack'
        self.arsenalCase.addAttack("Normal Attack", "None", baseAttack, 0)
        self.classType = classType
        self.elementalType = elementalType
        self.baseDefense = baseDefense
        self.wallet = 0

    def showStatus(self):
        print("\n" + self.name + " [" + self.status + "]")
        print("Class: " + self.classType)
        print("Element Type: " + self.elementalType)
        print("Wallet: " + str(self.wallet))
        print("HP: " + self.health.showProgressBar(False))
        print("MP: " + self.mana.showProgressBar(False))

#This allows multiple enemies to be added and defeated during the game without creating individual variables for each enemy
class Roster:
    def __init__(self, title):
        self.title = title
        self.rosterList = []
        self.rosterTotal = 0

    def addRoster(self, name, startHealth, startMana, classType, elementalType, baseAttack, baseDefense):
        newChar = Character(name, startHealth, startMana, classType, elementalType, baseAttack, baseDefense)
        self.rosterList.append(newChar)
        self.rosterTotal = self.rosterTotal + 1

    def removeRoster(self, rosterIndex): 
        self.rosterList.pop(rosterIndex)
        self.rosterTotal = self.rosterTotal - 1

    def showRoster(self):
        print("\n" + self.title + " (" + str(self.rosterTotal) + ")")
        for currentChar in self.rosterList:
            currentChar.showStatus()

    def targetRoster(self):
        #Because the roster can change very quickly, it is better to generate the list on demand so it is up to date
        rosterNames = []
        for currentChar in self.rosterList:
            rosterNames.append(currentChar.name)
        currentRoster = MultipleChoice(self.title, rosterNames, False)
        #selectChoice will already remove the -1 for the index
        rosterIndex = currentRoster.selectChoice(True)
        return rosterIndex
    
    def attackChar(self, attackPower):
        #This is to attack someone on the given party
        #If there is only one target, then default to that target
        if (self.rosterTotal == 1): 
            rosterIndex = 0
        else:
            print("Choose Target to Attack:")
            rosterIndex = self.targetRoster()
        #Decrease the HP (after taking armor into consideration)
        damageDone = attackPower - self.rosterList[rosterIndex].baseDefense
        self.rosterList[rosterIndex].health.updatePosition(-damageDone)
        enemyStatus = self.rosterList[rosterIndex].name + " (Armor Reduced: " + str(self.rosterList[rosterIndex].baseDefense) + ")"
        enemyStatus = enemyStatus + "\nTotal Damage Done: " + str(damageDone) + "HP"
        #Show the new HP amount
        self.rosterList[rosterIndex].showStatus()
        if (self.rosterList[rosterIndex].health.currentPosition < 1):
            enemyStatus = enemyStatus + "\nTarget Eliminated"
            self.removeRoster(rosterIndex)

        return enemyStatus

    def healChar(self, healPower):
        #If there is only one target, then default to that target
        if (self.rosterTotal == 1): 
            rosterIndex = 0
        else:
            print("Choose Target to Heal:")
            rosterIndex = self.targetRoster()
        #Increase the HP
        self.rosterList[rosterIndex].health.updatePosition(healPower)
        #Show the new HP amount
        self.rosterList[rosterIndex].showStatus()

    # ! Currently this is not in use
    def changeStatusChar(self, newStatus):
        print("Choose Target to " + newStatus + ":")
        rosterIndex = self.targetRoster()
        #Change to the new status
        self.rosterList[rosterIndex].status = newStatus
        #Show the new status
        self.rosterList[rosterIndex].showStatus()

#A scenario is a segment of a story
class Scenario:
    def __init__(self, type, name, location, objective, progressPoints):
        self.type = type
        self.name = name
        self.location = location
        self.objective = objective
        self.progressPoints = progressPoints
        self.completeFlag = False

    def readScenario(self):
        scenarioStr = "Scenario: " + self.name + " [" + self.type + "]"
        scenarioStr = scenarioStr + "\nDestination: " + self.location
        scenarioStr = scenarioStr + "\nMain Objective: " + self.objective
        scenarioStr = scenarioStr + "\nPoints:" + str(self.progressPoints)
        return scenarioStr

class Objective:
    def __init__(self, task, type, criteria, value):
        self.task = task
        self.type = type
        self.criteria = criteria
        self.value = value
        self.completeFlag = False

    def objItemCheck(self, stagingArea):
        #For now, item check is only for the hero
        for checkItem in stagingArea.heroParty.rosterList[0].backpack.storage:
            #Ignore the first option since it is just a back menu option
            if (checkItem.name != "BackMainMenu"):
                if ((checkItem.name == self.criteria) & (int(checkItem.count) >= int(self.value))):
                    self.completeFlag = True

    def objArrivalCheck(self, checkLocation):
        #Check the location of the hero character
        if (self.criteria == checkLocation):
            self.completeFlag = True

class Location:
    def __init__(self, name, description, destinationStr):
        self.name = name
        self.description = description
        self.destinationStr = destinationStr
        self.destinations = MultipleChoice("Destinations (Travel Turn Time)", [], False)
        self.destinations.choices.append("Back to Main Menu")
        self.venues = []
        self.venuesList = MultipleChoice("Venues", [], False)
        self.venuesList.choices.append("Back to Main Menu")

    def parseDestinations(self):
        #First remove the \n
        destinationSplit = self.destinationStr.rstrip()
        destList = destinationSplit.split(";")
        #For each destination, place it in the MultipleChoice object
        for currentDest in destList:
            #Do another split for the turn count
            splitDetails = currentDest.split("=")
            #Truncate the first part (Travel:) from the string
            splitDetails[0] = splitDetails[0].lstrip("Travel:")
            self.destinations.choices.append(splitDetails[0] + " (" + splitDetails[1] + ")")

    def chooseDestination(self):
        selectDest = self.destinations.selectChoice(False)
        return selectDest
    
    def chooseVenue(self):
        #Need to -1 to line up the indices properly (the list starts at 1)
        selectVenue = self.venuesList.selectChoice(True)
        return selectVenue
    
    def enterVenue(self, selectVenue, stagingArea):
        turnSummary = "None"
        #Show the current wallet amount of the character
        print("\nWallet: " + str(stagingArea.heroParty.rosterList[0].wallet))
        #Need to offset the selectVenue by -1 to line up the indices
        selectVenue = selectVenue - 1
        #This is either buying an object or selecting a rest option
        selectService = self.venues[selectVenue].services.list.selectChoice(True)
        #If it is not "Rest", then it will be an item
        selectedItem = self.venues[selectVenue].services.storage[selectService]
        if (self.venues[selectVenue].type == "Shop"):
            #Place the item in character's inventory
            #Prompt the user how many the character wants to buy
            numberGiven = False
            while (numberGiven == False):
                quantity = input("How Many? ")
                if (quantity.isnumeric()):
                    #Need to create a special option 0 to avoid soft-locking the character if they don't have enough money
                    if (int(quantity) == 0):
                        return None
                    #Check if the character has enough money to buy the items
                    if (stagingArea.heroParty.rosterList[0].wallet >= (int(quantity) * selectedItem.price)):
                        numberGiven = True
                        stagingArea.heroParty.rosterList[0].wallet = stagingArea.heroParty.rosterList[0].wallet - (int(quantity) * selectedItem.price)
                        stagingArea.heroParty.rosterList[0].backpack.addItem(selectedItem, int(quantity), False)
                        if (int(quantity) == 1):
                            turnSummary = "Purchased " + quantity + " " + selectedItem.name + " for " + str(int(quantity) * selectedItem.price)
                        else:
                            turnSummary = "Purchased " + quantity + " " + selectedItem.name + "s for " + str(int(quantity) * selectedItem.price)
                        turnSummary = turnSummary + "\nNew Wallet Amount: " + str(stagingArea.heroParty.rosterList[0].wallet)
                    else:
                        print("Invalid Funds, Choose a Lesser Quantity")
                else:
                    print("Invalid Entry, Give An Integer Value")
        elif (self.venues[selectVenue].type == "Inn"):
            #Check if the character has enough money to stay at the inn
            if (stagingArea.heroParty.rosterList[0].wallet >= selectedItem.price):
                stagingArea.heroParty.rosterList[0].wallet = stagingArea.heroParty.rosterList[0].wallet - selectedItem.price
                #Heal the character by percentage
                innHeal = math.floor(stagingArea.heroParty.rosterList[0].health.finishPoint * selectedItem.value / 100)
                stagingArea.heroParty.rosterList[0].health.updatePosition(innHeal)
                turnSummary = "Selected " + selectedItem.name + " To Heal " + str(innHeal) + " HP for " + str(selectedItem.price)
                turnSummary = turnSummary + "\nNew Wallet Amount: " + str(stagingArea.heroParty.rosterList[0].wallet)
            else:
                print("Invalid Funds, Choose a Different Service")

        return turnSummary

    #This is for both shop and inn
    def addVenue(self, venueName, venueType, shopInventory, coreFile):
        newVenue = Venue(venueName, venueType)
        #Add items to the shop
        #Split up the shopInventory string by ";"
        inventoryStock = shopInventory.split(";")
        for stockItem in inventoryStock:
            #Go through the coreFile and find the respective item
            with open(coreFile) as readFile:
                for readLine in readFile:
                    itemLine = re.search("<Item>,(.+),(.+),(.+),(.+)", readLine)
                    if itemLine:
                        #If the item is listed, then add it to the inventory
                        if (itemLine.group(1) == stockItem):
                            splitDetails = itemLine.group(3).split(":")
                            #For now, the shop inventory is infinite
                            newVenue.services.addItem(Item(itemLine.group(1), splitDetails[0], "∞",
                                                          int(splitDetails[1]), itemLine.group(2), 
                                                          int(itemLine.group(4))), "∞", True)
        self.venues.append(newVenue)
        self.venuesList.choices.append(venueName)

class Venue:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        #This could either be items or inn services
        self.services = Inventory(name)

#Story is an array of scenarios
#This is where the scenarios get loaded
#NOTE: Using debug log is mandatory when making a story, the user needs to provide a log name
class Story:
    def __init__(self, scenarioFile, coreFile, maxTurnCount, debugLogFile):
        self.scenarioFile = scenarioFile
        self.coreFile = coreFile
        self.scenarioSet = []
        self.scenarioTotal = 0
        self.stagingArea = StagingArea(maxTurnCount, debugLogFile)
        self.currentLocation = Location("", "", "")
        self.objectiveSet = []
        progressTotal = 0
        #Read the scenario file and load each scenario into the story
        with open(self.scenarioFile) as readFile:
            for readLine in readFile:
                #Ignore '#' since it is a comment line
                if (re.search("#", readLine)):
                    #Remove the \n at the end
                    readLine = readLine.rstrip()
                    self.stagingArea.debugLog.writeLine("Value", "Comment Line: " + readLine)
                    continue

                #Note: <Scenario> is the identifier for the line, not a parameter to be filled in
                scenarioLine = re.search("<Scenario>,(.+),(.+),(.+),(.+),(\d+)", readLine)
                if scenarioLine:
                    newScenario = Scenario(scenarioLine.group(1), scenarioLine.group(2), scenarioLine.group(3),
                                           scenarioLine.group(4), int(scenarioLine.group(5)))
                    #With the scenario details uploaded, add it to the story array
                    self.scenarioSet.append(newScenario)
                    self.stagingArea.debugLog.writeLine("Value", "Scenario Added: (Index: " + str(self.scenarioTotal) + ") "
                                                        + scenarioLine.group(2))
                    # self.stagingArea.debugLog.writeLine("Value", "Type: " + scenarioLine.group(1) +
                    #                                     "Location: " + scenarioLine.group(3) + 
                    #                                     "Objective: " + scenarioLine.group(4))
                    previousTotal = progressTotal
                    progressTotal = progressTotal + int(scenarioLine.group(5))
                    self.stagingArea.debugLog.writeLine("Math", "Progress Increased: " + str(previousTotal) +
                                                         " (PREVIOUS) + " + str(scenarioLine.group(5)) +
                                                         " (ADDED) = " + str(progressTotal) + " (TOTAL)")
                    #Increment the number of scenarios by 1
                    self.scenarioTotal = self.scenarioTotal + 1

        #Once the progress total has been calculated, then create a progress bar based on that
        self.progressBar = ProgressBar(progressTotal, False)
        #This will be updated via procedure
        self.currentScenarioIndex = 0
        #Load the first scenario information
        self.currentScenarioName = self.scenarioSet[self.currentScenarioIndex].name
        self.currentScenarioType = self.scenarioSet[self.currentScenarioIndex].type

        #Set up the battle and travel menus
        self.battleMenu = MultipleChoice("Battle Menu", [], False)
        self.battleMenu.choices.append("Attacks and Spells")
        self.battleMenu.choices.append("Items")
        self.travelMenu = MultipleChoice("Travel Menu", [], False)
        self.travelMenu.choices.append("Travel Locations")
        self.travelMenu.choices.append("Venues")
        self.travelMenu.choices.append("Items")
        self.travelMenu.choices.append("Character Status")

    #For now, presume continual forward progress (there are no branching paths right now)
    def scenarioComplete(self):
        turnSummary = "None"
        self.scenarioSet[self.currentScenarioIndex].completeFlag = True
        #Add to the current progress
        self.progressBar.updatePosition(self.scenarioSet[self.currentScenarioIndex].progressPoints)
        turnSummary = "Completed Scenario: " + self.currentScenarioName
        self.stagingArea.debugLog.writeLine("Value", "Completed Scenario: " + self.currentScenarioName)
        #Since the scenario has been completed, empty out the objectiveSet
        self.objectiveSet = []
        # ! This will need to be adjusted later for branching paths
        #If at the end (and there are no remaining scenarios), remain on the last scenario
        if (self.currentScenarioIndex != (self.scenarioTotal - 1)):
            self.currentScenarioIndex = self.currentScenarioIndex + 1
            #Load the next scenario information
            self.currentScenarioName = self.scenarioSet[self.currentScenarioIndex].name
            self.currentScenarioType = self.scenarioSet[self.currentScenarioIndex].type
            turnSummary = turnSummary + "\nNew Scenario: " + self.currentScenarioName
            if (self.currentScenarioType == "Battle"):
                turnSummary = turnSummary + "\nEntered Into A Battle"

        return turnSummary

    def loadScenario(self, firstScenario):
        #Read the scenario file and find the given scenario
        with open(self.scenarioFile) as readFile:
            #This flag will be active when underneath the particular scenario
            inScenario = False
            battleMode = False
            for readLine in readFile:
                scenarioLine = re.search("<Scenario>,(.+),(.+),(.+),(.+),(\d+)", readLine)
                if scenarioLine:
                    if ((scenarioLine.group(1) == "Start") & (firstScenario == True)):
                        self.currentLocation.name = scenarioLine.group(3)
                        self.loadLocation()
                    elif (scenarioLine.group(2) == self.currentScenarioName):
                        inScenario = True
                        #Check to see what type it is
                        if (scenarioLine.group(1) == "Battle"):
                            battleMode = True
                            #Add the battle objective
                            self.loadBattleObjective()
                            self.stagingArea.debugLog.writeLine("Load", "Loading Battle Scenario: " + self.currentScenarioName)
                        elif (scenarioLine.group(1) == "Travel"):
                            self.stagingArea.debugLog.writeLine("Load", "Loading Travel Scenario: " + self.currentScenarioName)
                        elif (scenarioLine.group(1) == "Start"):
                            self.stagingArea.debugLog.writeLine("Load", "Loading Starting Position: " + self.currentScenarioName)
                    else:
                        if (inScenario == True):
                            #This means this line is for the next scenario, end the procedure
                            self.stagingArea.debugLog.writeLine("Load", "Completed Loading Scenario: " + self.currentScenarioName)
                            break
                        #This is not the correct scenario, continue on
                        continue

                #If the regex does not match, then check to see if inScenario
                if (inScenario == True):
                    #If there is a pound, it is a comment, skip to the next line
                    if (re.search("#", readLine)):
                        continue
                    #Check to see if there is an objective
                    if (re.search("<Objective>", readLine)):
                        self.loadObjective(readLine)
                    #If in a battle, then load the enemies in
                    if (battleMode == True):
                        enemyLine = re.search("<Enemy>,(.+),(\d+),(\d+),(.+),(.+),(\d+),(\d+)", readLine)
                        if enemyLine:
                            #Load in the enemy roster
                            self.stagingArea.enemyParty.addRoster(enemyLine.group(1), int(enemyLine.group(2)), int(enemyLine.group(3)),
                                                             enemyLine.group(4), enemyLine.group(5), int(enemyLine.group(6)),
                                                             int(enemyLine.group(7)))
                            self.stagingArea.debugLog.writeLine("Load", "Successfully Loaded Enemy: " + enemyLine.group(1))
                else:
                    continue

    def loadLocation(self):
        #Read the core file and find the given location
        with open(self.coreFile) as readFile:
            locationFound = False
            for readLine in readFile:
                locationLine = re.search("<Location>,(.+),(.+),(.+)", readLine)
                if locationLine:
                    if (locationFound == True):
                        #This means this line is a new location, break out of the loop
                        break
                    elif (locationLine.group(1) == self.currentLocation.name):
                        locationFound = True
                        #Overwrite the previous location information with the new location information
                        self.currentLocation = Location(locationLine.group(1), locationLine.group(2), locationLine.group(3))
                        self.currentLocation.parseDestinations()
                
                if (locationFound == True):
                    venueLine = re.search("<Venue>,(.+),(.+),(.+),(.+)", readLine)
                    if venueLine:
                        #Make sure that the venue does exist at this location
                        if (venueLine.group(2) == self.currentLocation.name):
                            if (venueLine.group(3) == "Shop"):
                                # ! For now, the shop is not going to buy anything from the player
                                self.currentLocation.addVenue(venueLine.group(1), "Shop", venueLine.group(4), self.coreFile)
                            elif (venueLine.group(3) == "Inn"):
                                self.currentLocation.addVenue(venueLine.group(1), "Inn", venueLine.group(4), self.coreFile)

    #Note: Battle objective will always be "Defeat the Opposing Force"
    def loadBattleObjective(self):
        self.objectiveSet.append(Objective("Defeat the Opposing Force", "Battle", "Battle", 0))

    def loadObjective(self, readObjective):
        #Load the objectives in travel mode
        objectiveStr = re.search("<Objective>,(.+),(.+),(.+)", readObjective)
        if objectiveStr:
            objectiveTask = objectiveStr.group(1)
            objectiveType = objectiveStr.group(2)
            #Need to break down the objective requirement string
            breakdownReq = objectiveStr.group(3).split("=")
            self.objectiveSet.append(Objective(objectiveTask, objectiveType, breakdownReq[0], breakdownReq[1]))

    def listObjectives(self):
        objectiveList = "\nCurrent Objectives\n"
        for readObjective in self.objectiveSet:
            objectiveList = objectiveList + "\nTask: " + readObjective.task + " [" + str(readObjective.completeFlag) + "]"
        return objectiveList

    def checkObjectives(self):
        #Note: This does not apply to battle objectives since there is only one: defeat all enemies
        #This will by default be set to true, anything that is not completed will be false
        allDone = True
        #Check each objective to see if they have met the criteria to complete it
        for readObjective in self.objectiveSet:
            #Check depending on the different type
            if (readObjective.type == "ItemCheck"):
                readObjective.objItemCheck(self.stagingArea)
            elif (readObjective.type == "Arrival"):
                readObjective.objArrivalCheck(self.currentLocation.name)
            #Anything that is not completed will make allDone flag false
            if (readObjective.completeFlag == False):
                allDone = False

        return allDone

    def showStoryProgress(self):
        storyProgress = "\n-------------------------------------------------------------------------\n"
        storyProgress = storyProgress +  "\nCurrent Scenario\n"
        scenarioDetail = self.scenarioSet[self.currentScenarioIndex].readScenario()
        storyProgress = storyProgress + "\n" + scenarioDetail
        return storyProgress

    def checkStoryFinish(self):
        #Checks the scenarios to see if their completeFlags are all true
        #It only takes one incomplete scenario to say it is false
        allComplete = True
        for checkScenario in self.scenarioSet:
            if (checkScenario.completeFlag == False):
                allComplete = False

        if (allComplete == True):
            return True
        else:
            return False

# ! NOTE: NOT FULLY IMPLEMENTED
# ! The only way the DebugLog will be easily accessible is through the StagingArea object (which will be created in the Story object)
# ! If the specific method does not use the StagingArea object, then it will not have access to the DebugLog class
class DebugLog:
    def __init__(self, fileName):
        #Start up the debug log
        self.printLog = open(fileName, "w")

        #Get the current time and print it into the log
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Start of Script Execution: " + str(currentTime), file=self.printLog)
        print("-------------------------------------------------------------------------", file=self.printLog)
    
    def writeLine(self, type, content):
        #Get the current line
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #Start the line variable
        lineHolder = "[" + str(currentTime) + "] "
        #Type: Output, Load, Math, Value, Error
        if (type == "Output"):
            lineHolder = lineHolder + "[OUTPUT] " + content
        elif (type == "Value"):
            lineHolder = lineHolder + "[VALUE] " + content
        elif (type == "Math"):
            lineHolder = lineHolder + "[MATH] " + content
        elif (type == "Load"):
            lineHolder = lineHolder + "[LOAD] " + content
        elif (type == "Error"):
            lineHolder = lineHolder + "[ERROR] " + content
        else:
            lineHolder = lineHolder + "[NONE] " + content

        print(lineHolder, file=self.printLog)