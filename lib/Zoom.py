import requests
from AWS import AWS
#!/usr/bin/env python3
import csv
import os
import jwt
import time
import json
import string
import random
import base64
import time
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
from AWS import AWS

class Zoom:
    '''
    A class for performing tasks within a Zoom account. 
    '''

    def __init__(self, domain):
        # Save keys in file keys object
        #For every user, format data and add to user list
        self.domain = domain
        self.log = open(os.path.dirname(__file__) + '/../log/zoom.log', 'w+')
        self.API_TOKEN = AWS().getEnvVariable('/'+ domain +'/zoom/apiToken')
        self.API_SECRET = AWS().getEnvVariable('/'+ domain +'/zoom/apiSecret')
        self.PAYLOAD = {"iss": self.API_TOKEN, "exp": int(time.time() + 60)}
        self.JWT_TOKEN = jwt.encode(self.PAYLOAD, self.API_SECRET, algorithm="HS256")
        self.HEADERS = {
            'Authorization': 'Bearer ' + self.JWT_TOKEN,
            'Content-type': 'application/json',
        }


    def getAllUsers(self, PARAMS={ "page_size": 300 }):
        allUsers = []
        response = requests.get('https://api.zoom.us/v2/users', params=PARAMS, headers=self.HEADERS).json()
        allUsers.extend(response['users'])
        while response['next_page_token']: 
            PARAMS['next_page_token'] = response['next_page_token']
            response = requests.get('https://api.zoom.us/v2/users', params=PARAMS, headers=self.HEADERS)
            allUsers.extend(response['users'])
        return allUsers
    

    def updateUserEmail(self, oldEmail, newEmail):
        response = requests.put(
            f'https://api.zoom.us/v2/users/{oldEmail}/email', 
            json={"email": newEmail}, 
            headers=self.HEADERS
        )
        if response.status_code == 204: print(f'Successfully updated {oldEmail} to {newEmail}')
        elif response.status_code == 404: print(response.json()['message'])
        else: print(f"Received {response.status_code} for {oldEmail}. Go to https://marketplace.zoom.us/docs/api-reference/error-definitions for more information")
        return response


    def createZoomAccount(self, user): 
        '''
        Creates an account in Zoom for user
            https://marketplace.zoom.us/docs/api-reference/zoom-api/users/usercreate

        Arguments
            user: User of the new Zoom account
        Returns
            Response from Zoom as json object, if account created successfully
            False if error occurs
        '''

         # Define variables
        URL = 'https://api.zoom.us/v2/users'
        DATA = {    
            'action': 'create',
            'user_info': {
                'email': user['workEmail'],
                'type': '2',
                'first_name': user['firstName'],
                'last_name': user['lastName']
            } 
        }
        HEADERS = {
            'Authorization': 'Bearer ' + self.auth.keys['zoom']['ACCESS_TOKEN'],
            'Content-type': 'application/json',
        }

        # Make POST request
        addedUser = requests.post(url = URL, json = DATA, headers = HEADERS)
        
        # Print result
        if addedUser.status_code == 201:
            self.log.write(f"createZoomAccount ==> Pro Zoom account successfully created for {user['firstName']} {user['lastName']}\n{addedUser.json()}\n")
            return addedUser.json()
   
        elif addedUser.status_code == 200:
            DATA['user_info']['type'] = '1'
            addedUser = requests.post(url = URL, json = DATA, headers = HEADERS)
            if addedUser.status_code == 201:
                self.log.write(f"createZoomAccount ==> Basic Zoom account successfully created for {user['firstName']} {user['lastName']}\n{addedUser.json()}\n")
                return addedUser.json()
            else: 
                self.log.write(f"createZoomAccount ==> ERROR {user['firstName']} {user['lastName']} {addedUser.json()}\n")
                return False
        else: 
            self.log.write(f"createZoomAccount ==> ERROR {user['firstName']} {user['lastName']} {addedUser.json()}\n")
            return False

if __name__ == '__main__':
    ZOOM = Zoom('4catalyzer')
    print(f'Testing connection to {ZOOM.domain}.zoom.us')
    print(ZOOM.getAllUsers())
