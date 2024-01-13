# veradvent: Versatile Adventure
Customizable, Turn-Based, Text-Based Adventure

Goal: To create a customizable, interactive story by only needing to modify a user input file.

*Note: This repository is for my learning purposes. I am just trying to learn Python. Use with caution.

## Basic Features
Create a Customizable Adventure with CSV Story Files

A Core File to Store Shared Assets Between Story Files

Turn Count and Progress Bar

List Objectives and Last Turn Summary

Simple Combat

Travel Between Towns

Visit Shops and Inns in Towns

## Important Files
tutorialstory.csv: This is the user input file where the user can add or modify scenarios and objectives.

veradvent.py: This is the "engine" to read the user's CSV Story File. 

storylibrary.py: This is the library containing the objects to make the adventure possible.

corefile.csv: This file contains a set of assets that can be reused for different CSV Story Files.

## How to Use

### Script Use

*Note: Place all of the files into one single directory.

#### Command: python3 veradvent.py

### Story File (Example: tutorialstory.csv)

This file is to store a set of scenarios and objectives in a given order. It follows a top-down order so the topmost line will be the first to be executed.

### Core File (Example: corefile.csv)

This file is to store common assets that can be shared between different story files (i.e. locations, items, venues, etc.).

## Input Line Formats

### Story File

#### Scenario Format: \<Scenario>,scenarioType,scenarioName,destination,objectiveStr,progressPoints

Scenario Types: Start, Travel, Battle

##### Note: 'Start' Scenario determines the starting location of the adventure.

Start Example: \<Scenario>,Start,Beginning,Stillings,Your adventure begins in Stillings.,0

Travel Example: \<Scenario>,Travel,On the Way to Philbrook,Stillings-Philbrook Route,Make your way to Philbrook.,500

Battle Example: \<Scenario>,Battle,Crossing the Troll Bridge,Stillings-Philbrook Route,You need to defeat the troll to continue on.,500

#### Objective Format: \<Objective>,objectiveTask,objectiveType,objectiveReqStr

Objective Type: ItemCheck, Arrival

Objective Requirement String Format: [Item or Location]=[Quantity]

ItemCheck Example: \<Objective>,Obtain 3 Red Potions,ItemCheck,Red Potion=3

Arrival Example: \<Objective>,Go to Holloway,Arrival,Holloway=0

#### Enemy Format: \<Enemy>,enemyName,health,mana,enemyType,elementalType,attack,armor

\<Enemy>,Troll,50,100,Minion,None,5,0

### Core File

#### Location Format: \<Location>,locationname,description,Travel:travelLocation=travelTurn;travelLocation=travelTurn (multiples)

Location Example: \<Location>,Philbrook,"Village at the crossroads",Travel:Stillings-Philbrook Route=4;Philbrook-Holloway Route=5

#### Venue Format: \<Venue>,venuename,location,venuetype,otherDetails (multiples)

Venue Example: \<Venue>,Tabard Inn,Philbrook,Inn,Inn Room;Sauna

#### Items Format: \<Item>,itemname,description,Attribute:Value,moneyCost

Item Example: \<Item>,Red Potion,Heals for 50HP,Heal:50,75