#!/usr/bin/env python3
import argparse
from datetime import datetime

from classes.Authentication import Authentication
from classes.Staff import Staff 


## Parse command arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', 
    help='provide path to staff excel file', 
    default='./Onboarding Tracker.xlsx', 
    metavar=''
)
parser.add_argument('-k', '--keys', 
    help='provide path to admin keys', 
    default='', 
    metavar=''
)
args = parser.parse_args()

# Create necessary variables
if args.keys: auth = Authentication(args.keys) 
else: auth = Authentication()
staff = Staff(args.file, auth)

# Get list of current staff
masterList = open("employee-list.txt", "r+")
list = masterList.readlines()
masterList.close()
currentStaff = []
for employee in list: 
    currentStaff.append(employee.rstrip())

# Onboard employees in list
masterList = open("employee-list.txt", "a+")
confirmationMsg = ''
for newHire in staff.users:
    if newHire['workEmail'] not in currentStaff:
        confirm = input(f"Would you like to onboard {newHire['firstName']} {newHire['lastName']}? (y or n) ")
        if confirm.lower() == 'y':
            staff.log.write(f"Onboarding {newHire['firstName']} {newHire['lastName']}...\n\n")
            staff.addGSuiteUser(newHire)
            if newHire['status'] != 'temp': 
                staff.addToGSuiteGroups(newHire, ['obscura'])
                #staff.createHarvestAccount(newHire)
            else: staff.addToGSuiteGroups(newHire, ['obscura', 'od-temps'])
            staff.createSlackAccount(newHire)
            staff.createZoomAccount(newHire)
            staff.sendEmail(newHire['personalEmail'], f"Welcome to Obscura Digital, {newHire['firstName']}", '', 'html', newHire)
            masterList.write(str(newHire['workEmail']) + '\n')
            confirmationMsg += newHire['workEmail'] + '\n'
        else: staff.log.write(f"{newHire['firstName']} {newHire['lastName']} not onboarded\n\n")
masterList.close()
staff.log.close()  

# Send confirmation email to administrator 
staff.sendEmail(auth.keys['admin_email'], 'New hire(s) onboarded', confirmationMsg)

# COMMENT OUT TO STOP REMOVAL OF ADMIN KEYS AFTER SCRIPT EXIT (not recommended)
if staff.auth.removeKeys():
    print('Keys safely removed from working directory')
else: print('Keys not removed from working directory.')
