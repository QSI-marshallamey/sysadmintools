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
from AWS import AWS

class Slack:
    '''
    A class for performing tasks within a Slack account. 
    '''

    def __init__(self, company):
        # Save keys in file keys object
        #For every user, format data and add to user list
        self.company = company
        self.log = open(os.path.dirname(__file__) + '/../log/slack.log', 'w+')
        self.API_TOKEN = AWS().getEnvVariable('/'+ company +'/slack/apiToken')
        self.HEADERS = {
            'Authorization': 'Bearer ' + self.API_TOKEN,
            'Content-type': 'application/x-www-form-urlencoded',
        }

    def createSlackAccount(self, user):
        '''
        Generates an email address in gSuite for new hire

        Arguments
            user: User to send Slack invitation
        Returns
            True if invitation sent successfully
            False if error occured
        '''

        # Define variables
        URL = 'https://slack.com/api/users.admin.invite'
        DATA = {    
            'email': user['workEmail'],
            'channels':'C9FUXFA3A',
            'real_name': f"{user['firstName']} {user['lastName']}",  
        }

        # Make POST request
        response = requests.post(url = URL, data = DATA, headers = self.HEADERS)
        res = response.json()
        
        # Print result
        if res['ok'] == True:
            self.log.write('createSlackAccount ==> Slack invitation successful for ' + DATA['real_name'] + '\n')
            return True
        else: 
            self.log.write(f"createSlackAccount ==> Something went wrong. Slack invite not sent to {user['firstName']} {user['lastName']}.\n{res['error']}\n")
            return False

    def getAllUsers(self):
        '''
        Returns a list of all Slack users
        '''

        # Define variables
        URL = 'https://slack.com/api/users.list'

        # Make GET request
        response = requests.get(url = URL, headers = self.HEADERS)
        res = response.json()
        # Print result
        if res['ok'] == True:
            for user in res['members']:
                if user['deleted'] == True or user['is_bot'] == True or user['name'] == 'slackbot':
                    res['members'].remove(user)
            print(f'There are {len(res["members"])} active users')
            self.log.write(f'getAllUsers ==> {res}\n')
            return res['members']
        else: 
            self.log.write(f"getAllUsers ==> {res}\n")
            return False


    def updateUserEmail(self, oldEmail, newEmail, userID):
        '''
        Updates email address of Slack user
        '''
        
        # Define variables
        URL = 'https://slack.com/api/users.profile.set'
        HEADERS = {
            'Authorization': 'Bearer ' + self.API_TOKEN,
            'Content-type': 'application/json; charset=utf-8',
        }
        DATA = {
            "user": userID,
            "profile": { "email": newEmail }
        }
        
        # Make POST request
        response = requests.post(url=URL, headers=HEADERS, json=DATA)
        res = response.json()
        # Print result
        if res['ok'] == True:
            print(f"Successfully updated {oldEmail} to {newEmail}")
            self.log.write(f'updateSlackEmail ==> {res}\n')
            return res
        else: 
            print(f"{oldEmail} not updated. {res}")
            self.log.write(f"updateSlackEmail ==> {res}\n")
            return res