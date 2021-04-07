#!/usr/bin/env python3
import csv
import os
import time
import json
import string
import random
import base64
from datetime import date
from email.mime.text import MIMEText
import hashlib

import openpyxl
import requests
import urllib.request
import urllib.parse as urlparse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from datetime import datetime
from Authentication import Authentication
class Harvest:
     def createHarvestAccount(self, user): 
        '''
        Creates an account in Harvest for user

        Arguments
            user: User of the new Harvest account
        Returns
            Harvest response as json object if created successfully
            False if error occurred
        '''

        # Define variables
        URL = 'https://api.harvestapp.com/v2/users'
        DATA = {    
            'first_name': user['firstName'],
            'last_name': user['lastName'],
            'email': user['workEmail'],
            'roles': [user['title']],
        }
        HEADERS = {
            'Authorization': 'Bearer ' + self.auth.keys['harvest']['ACCESS_TOKEN'],
            'Harvest-Account-Id': self.auth.keys['harvest']['ACCOUNT_ID'],
            'User-Agent': f"MyApp ({self.auth.keys['admin_email']})",
            'Content-type': 'application/json',
        }

        # Make POST request
        addedUser = requests.post(url = URL, json = DATA, headers = HEADERS)
        
        # Print result
        if addedUser.status_code == 201:
            self.log.write(f"createHarvestAccount ==> Harvest account successfully created for {user['firstName']} {user['lastName']}\n{addedUser.json()}\n")
            return addedUser.json()
        else:
            self.log.write(f"createHarvestAccount ==> Something went wrong with the request. Harvest user {user['firstName']} {user['lastName']} not created\n{addedUser.json()}\n")
            return False