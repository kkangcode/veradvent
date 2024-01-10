from storylibrary import *
import os

#Start up the story
maxTurnCount = 50
storyFile = "tutorialstory.csv"
coreFile = "corefile.csv"
mainStory = Story(storyFile, coreFile, maxTurnCount, "debug.log")

heroClasses = ["Rook", "Knight", "Bishop"]
elementalType = ["Wind", "Earth", "Shadow", "Water", "Fire", "Holy"]

#Have the player choose their class and elemental type
# ! These don't have any impact in combat yet
classSelect = MultipleChoice("Classes", heroClasses, True)
playerClass = classSelect.selectChoice(False)
mainStory.stagingArea.debugLog.writeLine("Value", "Player Class: " + playerClass)
elementSelect = MultipleChoice("Elemental Type", elementalType, True)
playerElement = elementSelect.selectChoice(False)
mainStory.stagingArea.debugLog.writeLine("Value", "Player Elemental Type: " + playerElement)

#Add a player character to the party
mainStory.stagingArea.heroParty.addRoster("Oliver", 100, 100, playerClass, playerElement, 50, 5)
#Give the player character some starting money
mainStory.stagingArea.heroParty.rosterList[0].wallet = 1000

#DEBUG: Check to see if all of the scenarios were loaded and the progress bar is working
#Show the beginning scenario
#mainStory.showStoryProgress()
#Go through each of the scenarios and build up the progress bar
# for currentScenario in mainStory.scenarioSet:
#     mainStory.scenarioComplete()
#     mainStory.showStoryProgress()

#Load the first scenario
addTurnCount = 0
mainStory.loadScenario(True)
mainStory.showStoryProgress()
showCharacterStatus = False
lastTurnSummary = "None"
innRest = False
while (mainStory.checkStoryFinish() == False):
    #This will clear the terminal
    os.system('clear')
    #Increment the turn count now
    #If traveling between a town, it will cost additional turns to mimic the distance travelled
    #If the user wants to see the character status (when not using an inn), then do not increment the turn counter
    if ((showCharacterStatus == False)):
        if (addTurnCount != 0):
            mainStory.stagingArea.turnCount.currentPosition = mainStory.stagingArea.turnCount.currentPosition + int(addTurnCount)
            addTurnCount = 0
        else:
            mainStory.stagingArea.turnCount.currentPosition = mainStory.stagingArea.turnCount.currentPosition + 1
    elif (innRest == True):
        #Staying at an inn will cost a turn
        innRest = False
        mainStory.stagingArea.turnCount.currentPosition = mainStory.stagingArea.turnCount.currentPosition + 1

    #Check to see if the turn limit has been reached
    if (mainStory.stagingArea.turnCount.currentPosition > mainStory.stagingArea.turnCount.finishPoint):
        print("You have exceeded the maximum number of turns")
        break

    print("\nTurn Count " + str(mainStory.stagingArea.turnCount.currentPosition))
    print("Turn Limit: " + mainStory.stagingArea.turnCount.showProgressBar(False))
    mainStory.stagingArea.debugLog.writeLine("Value", "Turn: " + str(mainStory.stagingArea.turnCount.currentPosition))
    mainStory.showStoryProgress()
    #If the user requested to see the character status in the previous turn, then display now
    if (showCharacterStatus == True):
        showCharacterStatus = False
        print("\n-------------------------------------------------------------------------")
        print("\nCharacter Status")
        mainStory.stagingArea.heroParty.rosterList[0].showStatus()

    #Show the current objectives remaining
    print("\n-------------------------------------------------------------------------")
    objectiveList = mainStory.listObjectives()
    print(objectiveList)

    #Since the console clears away the previous things, report what happened last turn
    print("\n-------------------------------------------------------------------------")
    print("\nLast Turn Summary\n")
    print(lastTurnSummary)
    print("\n-------------------------------------------------------------------------")
    #Reset the lastTurnSummary string
    lastTurnSummary = "None"
    actionSelected = False

    if (mainStory.currentScenarioType == "Start"):
        #Load the starting location listed in the start scenario
        mainStory.loadLocation()
        #Load the next scenario
        mainStory.scenarioComplete()
        mainStory.loadScenario(False)
        mainStory.showStoryProgress()
        #On first turn, show the character status (in case the player randomized their class and type)
        showCharacterStatus = True
    elif (mainStory.currentScenarioType == "Battle"):
        #Show current status of the hero and the enemies
        mainStory.stagingArea.heroParty.rosterList[0].showStatus()
        mainStory.stagingArea.enemyParty.showRoster()
        #Have the character attack first for now (this will also have the option to select items)
        while (actionSelected == False):
            #Option 0 - Attacks and Spells, Option 1 - Items
            playerSelect = mainStory.battleMenu.selectChoice(True)
            if (playerSelect == 0):
                heroAttack = mainStory.stagingArea.heroParty.rosterList[0].arsenalCase.chooseAttack(False)
                #If the player selected to go back, then go back to the main menu
                if (heroAttack.name != "BackMainMenu"):
                    actionSelected = True
                    # ! Need debugLog output
                    enemyStatus = mainStory.stagingArea.enemyParty.attackChar(heroAttack.attackPower)
                    heroName = mainStory.stagingArea.heroParty.rosterList[0].name
                    lastTurnSummary = heroName + " Attacked With " + heroAttack.name + " For " + str(heroAttack.attackPower) + "HP on " + enemyStatus
            elif (playerSelect == 1):
                # ! Need debugLog output
                heroItem = mainStory.stagingArea.heroParty.rosterList[0].backpack.selectItem(mainStory.stagingArea)
                if (heroItem != "BackMainMenu"):
                    #If the user used an item, then skip the attack phase
                    actionSelected = True
                    if (heroItem.effect == "Heal"):
                        heroName = mainStory.stagingArea.heroParty.rosterList[0].name
                        lastTurnSummary = heroName + " Used " + heroItem.name + " To " + heroItem.effect + " " + str(heroItem.value) + "HP"
        #For now, limit the enemies to one attack and only one target (the hero)
        #If the hero defeats the last enemy in the party, then this part gets skipped over
        for enemyChar in mainStory.stagingArea.enemyParty.rosterList:
            # ! Need debugLog output
            enemyAttack = enemyChar.arsenalCase.chooseAttack(True)
            heroStatus = mainStory.stagingArea.heroParty.attackChar(enemyAttack.attackPower)
            enemyName = enemyChar.name
            lastTurnSummary = lastTurnSummary + "\n" + enemyName + " Attacked With " + enemyAttack.name + " For " + str(enemyAttack.attackPower) + "HP on " + heroStatus
    elif (mainStory.currentScenarioType == "Travel"):
        while (actionSelected == False):
            #Option 0 - Travel Locations, Option 1 - Venues, Option 2 - Items, Option 3 - Show Character Status
            playerSelect = mainStory.travelMenu.selectChoice(True)
            if (playerSelect == 0):
                heroTravel = True
                print("\nCurrent Location: " + mainStory.currentLocation.name)
                selectDestination = mainStory.currentLocation.chooseDestination()
                if (selectDestination != "Back to Main Menu"):
                    actionSelected = True
                    #Load the next location (Break the string and process the turn count separately)
                    splitDestination = re.search("(.+) \((\d+)\)", selectDestination)
                    if splitDestination:
                        mainStory.currentLocation.name = splitDestination.group(1)
                        addTurnCount = splitDestination.group(2)
                        mainStory.loadLocation()
                        lastTurnSummary = "Travelled to New Location: " + mainStory.currentLocation.name + " (Turns Passed: " + addTurnCount + ")"
            elif (playerSelect == 1):
                print("\nPick a Venue")
                venueIndex = mainStory.currentLocation.chooseVenue()
                if (venueIndex != 0):
                    actionSelected = True
                    #Note: if the user goes into a store and does not buy anything, then that still costs a turn (cause the user travelled to that venue)
                    # ! Need debugLog output
                    lastTurnSummary = mainStory.currentLocation.enterVenue(venueIndex, mainStory.stagingArea)
                    #If the player went into an inn to heal, then show the character status next turn
                    if (mainStory.currentLocation.venues[venueIndex - 1].type == "Inn"):
                        showCharacterStatus = True
                        innRest = True
            elif (playerSelect == 2):
                # ! Need debugLog output
                heroItem = mainStory.stagingArea.heroParty.rosterList[0].backpack.selectItem(mainStory.stagingArea)
                if (heroItem != "BackMainMenu"):
                    actionSelected = True
                    print("Hero Item: " + heroItem.name)
                    if (heroItem.effect == "Heal"):
                        heroName = mainStory.stagingArea.heroParty.rosterList[0].name
                        lastTurnSummary = heroName + " Used " + heroItem.name + " To " + heroItem.effect + " " + str(heroItem.value) + "HP"
                        #Show the character status next turn
                        showCharacterStatus = True
                        #Using an item to heal is the same effect as going to the inn, need to increment the turn count
                        innRest = True
            elif (playerSelect == 3):
                #This will not cost the user a turn
                showCharacterStatus = True
                actionSelected = True

    #Check the objectives to see if the scenario has been completed
    #Battles don't need objectives, simply eliminate all of the enemies
    # ! Need debugLog output
    objectiveDone = mainStory.checkObjectives()
    
    #If the player dies, then the game is over
    if ((mainStory.stagingArea.heroParty.rosterTotal == 0)):
        print("You have died!")
        break
    elif ((objectiveDone == True) & (mainStory.currentScenarioType == "Travel")):
        # ! Need debugLog output
        scenarioStr = mainStory.scenarioComplete()
        lastTurnSummary = lastTurnSummary + "\n" + scenarioStr
        mainStory.loadScenario(False)
        storyProgress = mainStory.showStoryProgress()
        lastTurnSummary = lastTurnSummary + "\n" + storyProgress
    elif ((mainStory.stagingArea.enemyParty.rosterTotal == 0) & (mainStory.currentScenarioType == "Battle")):
        #Note: The battle objective is completed when there are no more enemies on the opposing force
        #There is no need to set the completeFlag to true
        # ! Need debugLog output
        scenarioStr = mainStory.scenarioComplete()
        lastTurnSummary = lastTurnSummary + "\n" + scenarioStr
        mainStory.loadScenario(False)
        storyProgress = mainStory.showStoryProgress()
        lastTurnSummary = lastTurnSummary + "\n" + storyProgress
        #Show the character status after the battle to alert the player if healing is needed
        showCharacterStatus = True
        #This is to make sure that a turn still passes after the character defeats the last enemy
        innRest = True

if (mainStory.checkStoryFinish() == True):
    print("You win!")
else:
    print("You lose!")