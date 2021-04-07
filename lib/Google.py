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
from google.auth import crypt
from google.auth import jwt

from datetime import datetime
from AWS import AWS

##### VARIABLES #####
users = []
auth = {}
log = open('../log/staff.log', 'w+')

class Google:
    '''
    A library for performing tasks within a GSuite account. 
    '''

    def __init__(self, domain):        
        '''
        Instantiate object
        '''      
        SERVICE_ACCOUNT = AWS().getEnvVariable('/'+ domain +'/google/serviceAccount')
        SIGNER = crypt.RSASigner.from_service_account_info(
            json.loads(SERVICE_ACCOUNT)
        )
        PAYLOAD = {
            "iss": "gyb-project-m6m-rtj-us9@gyb-project-m6m-rtj-us9.iam.gserviceaccount.com", 
            "scope": "https://www.googleapis.com/auth/admin.directory.user",
            "aud": "https://oauth2.googleapis.com/token",
            "exp": int(time.time() + 3600),
            "iat": int(time.time()),
            "sub": "mamey@detect.com"
        }
        JWT_TOKEN = jwt.encode(SIGNER, PAYLOAD)
        DATA = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": JWT_TOKEN
        }
        response = requests.post("https://oauth2.googleapis.com/token", data=DATA).json()

        self.log = open('../log/google.log', 'w+')
        self.ACCESS_TOKEN = response['access_token']
        self.HEADERS = {
            'Authorization': 'Bearer ' + self.ACCESS_TOKEN,
            'Content-type': 'application/json',
        }
        

    def getAllUsers(self, nextPageToken=0): 
        ''' 
        Retrieves all users from the domain

        Returns
            Object containing all users
            False if error during operation
        '''
        # Make API request to add new user

        allUsers = []
        response = requests.get('https://www.googleapis.com/admin/directory/v1/users?domain=detect.com', headers=self.HEADERS).json()
        allUsers.extend(response['users'])
        while 'nextPageToken' in response: 
            response = requests.get('https://www.googleapis.com/admin/directory/v1/users?domain=detect.com', headers=self.HEADERS, params={ 'pageToken': response['nextPageToken'] }).json()
            allUsers.extend(response['users'])
        return allUsers

    def updateUserEmail(self, oldEmail, newEmail):
        ''' Updates user email in GSuite. Old email is automatically added as an alias '''  

        # Make API request to change primary email
        response = requests.put(
            f'https://www.googleapis.com/admin/directory/v1/users/{oldEmail}', 
            headers=HEADERS, 
            json={ "primaryEmail": newEmail }
        ).json()
        return response


    def addGSuiteUser(self, user): 
        ''' 
        Generates an email address in gSuite for new hire
        
        Arguments
            user: Dictionary of user data to be added

        Returns
            Object containing created user from Google
            False if error during operation
        '''
        if not self.auth.keys['google']['ACCESS_TOKEN']: self.auth.getGoogleAccessToken()
        # Make API request to add new user
        USER_DATA = {
            "name": {
                "familyName": user['lastName'],
                "givenName": user['firstName']
            },
            "password": self.auth.keys['default_password'],
            "primaryEmail": user['workEmail'],
        }

        HEADERS = {
            'Authorization': 'Bearer ' + self.auth.keys['google']['ACCESS_TOKEN'],
            'Content-type': 'application/json',
        }
        addedUser = requests.post('https://www.googleapis.com/admin/directory/v1/users', headers=HEADERS, json=USER_DATA)
        if addedUser.status_code == 200:
            self.log.write(f"addGSuiteUser ==> Email creation successful for {user['firstName']} {user['lastName']}\n{addedUser.json()}\n")
            return addedUser.json()
        else:
            self.log.write(f"addGSuiteUser ==>  Something went wrong with the request. {user['firstName']} {user['lastName']} not added\n{addedUser.json()}\n")
            return False


    def removeGSuiteUser(self, userEmail):
        ''' 
        Removes a user from gSuite
        
        Arguments
            userEmail: Email address of the user to be removed

        Returns
            True if successfully removed
            False if error during operation
        '''

        if not self.auth.keys['google']['ACCESS_TOKEN']: self.auth.getGoogleAccessToken()

        # Make API request to remove user
        HEADERS = {
            'Authorization': 'Bearer ' + self.auth.keys['google']['ACCESS_TOKEN'],
            'Content-type': 'application/json',
        }
        removedUser = requests.delete(f'https://www.googleapis.com/admin/directory/v1/users/{userEmail}', headers=HEADERS)
        if removedUser.status_code == 204:
            self.log.write(f"removeGSuiteUser ==> Removed {userEmail} from Obscura domain\n")
            return True
        else:
            self.log.write(f"removeGSuiteUser ==>  Something went wrong with the request. {userEmail} not removed\n{removedUser}\n")
            return False

 
    def generatePassword(self):
        l = string.ascii_lowercase + string.ascii_uppercase
        d = string.digits
        newPassword = ''.join(random.sample(l, 10)) + ''.join(random.sample(d, 5))
        return newPassword

        
    def resetGSuitePassword(self, user):
        ''' 
        Generates a random password and sends an email to the administrator with credentials
        
        Arguments
            user: Dictionary of user data

        Returns
            updatedUser if successfully reset
            False if error during operation
        '''
        if not self.auth.keys['google']['ACCESS_TOKEN']: self.auth.getGoogleAccessToken()
        newPassword = self.generatePassword()
        print(newPassword)
        print(user['primaryEmail'])
        # Define variables
        HEADERS = {
            'Authorization': 'Bearer ' + self.auth.keys['google']['ACCESS_TOKEN'],
            'Content-type': 'application/json',
        }
        USER_DATA = {
            "password": newPassword,
            "changePasswordAtNextLogin": 'true',
        }
        
        # Make API request to reset password
        updatedUser = requests.put(f'https://www.googleapis.com/admin/directory/v1/users/{user["primaryEmail"]}', headers=HEADERS, json=USER_DATA)
        
        csv = open('../files/email_passwords.csv', 'a+')
        if updatedUser.status_code == 200:
            msg = (
                f'Greetings from your IT department,'
                f'As a reminder, during the next step in our migration to MSG Platforms, we’ll be separating the '
                f'connection between MSG\'s active directory and G Suite, and as part of this separation, you '
                f'will be required to use a new password to access G Suite starting tomorrow at 6:00pm. We’ve provided you with your new password below: '
                f'\n{newPassword}'
                f'\nPlease reach out to the MSG Service Desk at 212-465-6565 if you experience any issues. Thank you for your cooperation, and have a great day!'
            )
            #self.log.write(f"resetPassword ==> Reset password for {user['primaryEmail']} from Obscura domain\n")
            csv.write(f'{user["primaryEmail"]},{newPassword}\n')
            csv.close()
            self.sendEmail(f"{self.auth.keys['admin_email']}, {user['primaryEmail']}", f"Password reset for {user['primaryEmail']}", msg, 'plain', user)
            print(updatedUser)
            return updatedUser
        else:
            #self.log.write(f"resetPassword ==>  Something went wrong with the request. {user['workEmail']} password was not changed.\n")
            print(updatedUser)
            return updatedUser


    def addToGSuiteGroups(self, user, groups): 
        '''
        Adds a user to email group aliases

        Arguments
            user: The person who will be added to groups
            groups: A list of the group names to which the user will be added
        Returns
            Google response in json object, if successfully added
            False if error occurs
        '''

        if not self.auth.keys['google']['ACCESS_TOKEN']: self.auth.getGoogleAccessToken()
        
        # Define variables
        USER_DATA = {
            "email": user['workEmail'],
            "role": 'MEMBER',
        }
        HEADERS = {
            'Authorization': 'Bearer ' + self.auth.keys['google']['ACCESS_TOKEN'],
            'Content-type': 'application/json',
        }

        # Make an API request for each group in the list
        for group in groups:
            addedUser = requests.post(f'https://www.googleapis.com/admin/directory/v1/groups/{group}@obscuradigital.com/members', headers=HEADERS, json=USER_DATA)
            if addedUser.status_code == 200:
                self.log.write(f"addToGSuiteGroups ==> {user['firstName']} {user['lastName']} successfully added to {group}@obscuradigital.com\n{addedUser.json()}\n")
                return addedUser.json()
            else:
                self.log.write(f"addToGSuiteGroups ==>  Something went wrong with the request. {user['firstName']} {user['lastName']} not added to {group}@obscuradigital.com\n{addedUser.json()}\n")
                return False

    def sendEmail(self, destination, subject, msg, type='plain', user={}): 
        '''
        Sends an email to using Gmail messages API. Sender is the user with the access token
            https://developers.google.com/gmail/api/v1/reference/users/messages/send
        Arguments
            destination: The recipient's email address
            subject: The subject line of the email
            msg: The body of the email message
            type: Format of message, i.e. text, html, etc
            user: User object
        Returns
            True if email sent successfully
            False if not sent
        '''

        if not self.auth.keys['google']['ACCESS_TOKEN']: self.auth.getGoogleAccessToken()
        
        # Define variables
        URL = 'https://www.googleapis.com/gmail/v1/users/me/messages/send'
        HEADERS = {
            'Authorization': 'Bearer ' + self.auth.keys['google']['ACCESS_TOKEN'],
            'Content-type': 'application/json',
        }
        if msg == '': msg = self.createWelcomeEmail(user)
        message = MIMEText(msg, type)
        message['to'] = destination
        message['from'] = self.auth.keys['admin_email']
        message['subject'] = subject
        DATA = {'raw': base64.urlsafe_b64encode( message.as_string().encode('UTF-8') ).decode('ascii')}
       
        # Make POST request
        response = requests.post(url = URL, json = DATA, headers = HEADERS)
        res = response.json()
              
        # Print result
        if response.status_code == 200:
            print(f"sendEmail ==> Email sent to {destination}\n{res}\n\n")
            return True
        else: 
            print(f"sendEmail ==> ERROR {res}\n\n")
            return False

    
    def createWelcomeEmail(self, user):
        email = (
            '<html><body>'
            '<h2>A welcome from your IT team!</h2>'
            f'<p>Hello, {user["firstName"]}. We are thrilled that you will be joining us soon. '
            'Here are a few things that will help you be prepared for your first day:</p>'
            
            '<h3>Email</h3>'
            f'<p>Your new Obscura email account has been created. Your address is {user["workEmail"]} and the default password is {self.auth.keys["default_password"]}. '
            'You can login at <a href="https://mail.google.com">mail.google.com</a> to start setting up your inbox</p>'
            
            '<h3>Slack</h3>'
            '<p>Your inbox should contain an invitation to our <a href="https://obscurahq.slack.com">Slack channel</a>. '
            'The "all sf" channel is used primarily for work related announcements, whereas the "watercooler" channel '
            'is the space for more personal conversations.  Feel free to drop a line any time!</p>'

            '<h3>Zoom</h3>'
            '<p>Your inbox should also contain an invitation to your new Zoom account. We use Zoom a lot to communicate with vendors and the MSG offices in New York. '
            'Once you get your computer, you should download the <a href="https://zoom.us/download">Zoom Client for Meetings</a> app for easy access to Zoom\'s many features. '
            'If you use Chrome, <a href="https://chrome.google.com/webstore/detail/zoom-scheduler/kgjfgplpablkjnlkjmjdecgdpfankdle?hl=en-US">click here</a> for a nifty Zoom extension that is great for creating meetings in Google calendar.</p>'
        )

        # if user['status'] != 'temp': email += (
        #     '<h3>Harvest</h3>'
        #     '<p>Harvest is the software we use for time tracking. That will be the last '
        #     'invitation you\'ll find in your inbox.  <a href="https://youtu.be/AA1oUDPO6Ns">Watch this video</a> to get up to speed on how '
        #     'Obscura uses this platform.</p></br>'
        # )

        email += (
            f'<p>New Hire orientation will be at 10:00am on {user["startDate"].strftime("%B %d, %Y")}.  We look forward to meeting you then.  If you have any questions about this email or need '
            'assistance with setting up your accounts, you can contact us by sending an email to ithelp@obscuradigital.com.</p></br>'
            '<p>Welcome aboard!</p></br></br>'
            '<p>Your IT team</p>'
            '</body></html>'
        )
        return email