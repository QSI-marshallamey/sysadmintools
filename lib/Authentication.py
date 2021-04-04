#! /usr/bin/env python3
import os
import time
import json

import requests
import importlib.util
import urllib.request
import urllib.parse as urlparse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Authentication:
    '''
    AUTHENTICATION

    A class for obtaining and using credentials for scripts in the SysAdminTools package
    This includes passwords, keys, access tokens, etc.

    In order to function, the user must provide a properly formatted file with the necessary credentials.
    The default key file is called ADMIN_KEYS.py and a template can be found in the root directory of the repository.
    By default, the class assumes that ADMIN_KEYS.py is located in the root directory.  
    If not, the script will require you to input the correct path to the file.

    FUNCTIONS

        __init__(keyFilePath):
            Description: Creates an Authentication object. The default keyFilePath is ./ADMIN_KEYS.py
            Arguments: (keyFilePath) Path to the file containing the API and oAuth keys
            Returns: None

        getKeys(keyFilePath):
            Description: Called whenever an Authenticatino object is created.
            Arguments: (keyFilePath) Path to the file containing the API and oAuth keys
            Returns: Dictionary of keys, if found. Else returns False

        removeKeys():
            Description: Removes ADMIN_KEYS.py file from the working directory if present
            Arguments: None
            Returns: True if removed, otherwise False

        getGoogleAccessToken():
            Description: Completes Google oAuth flow to retrieve an access token
            Arguments: None
            Returns: None
    '''


    def __init__(self, keyFilePath='../ADMIN_KEYS.py'):        
        '''Construct an Authentication object with keys and a web driver'''
        self.keys = self.getKeys(keyFilePath)
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {
            'profile.default_content_setting_values.notifications': 2,
            'profile.managed_default_content_settings.popups': 2,
            'profile.managed_default_content_settings.geolocation': 2,
        })
        self.browser = {}


    def getKeys(self, keyFilePath):
        '''Retrieve keys from ADMIN_KEYS.py'''       
        if keyFilePath == '../ADMIN_KEYS.py' and not os.path.isfile('../ADMIN_KEYS.py'):
            keyFilePath = input('Admin keys not found in root directory. Where are they located?: ')          
        try:
            spec = importlib.util.spec_from_file_location('admin.keys', keyFilePath)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            print('Authentication.getKeys ==> Keys successfully retrieved!') 
            return mod.keys
        except ImportError:
            print('Authentication.getKeys ==> ERROR:: Could not import keys')
            return False


    def removeKeys(self):
        '''Remove keys from root directory''' 
        if os.path.isfile('../ADMIN_KEYS.py'):
            os.remove('../ADMIN_KEYS.py')
            return not os.path.isfile('../ADMIN_KEYS.py')
        else: 
            print('Authentication.removeKeys ==> No keys to remove.')
            return False


    def getGoogleAccessToken(self):       
        '''Complete Google oAuth flow to retrieve access token'''  
        print('Authentication.getGoogleAccessToken ==> Starting Google oAuth flow...')

        try:
            self.browser = webdriver.Chrome(options=self.browserProfile)
        except:
            print('Could not open Chrome browser.')
        
        
        # Define variables for GET request 
        SCOPE = 'https://www.googleapis.com/auth/admin.directory.user https://www.googleapis.com/auth/admin.directory.group https://www.googleapis.com/auth/gmail.compose'
        CLIENT_ID = self.keys['google']['CLIENT_ID']
        CLIENT_SECRET = self.keys['google']['CLIENT_SECRET']
        STATE = self.keys['google']['STATE']
        REDIRECT = self.keys['REDIRECT_URI']

        self.browser.get(f"https://accounts.google.com/o/oauth2/v2/auth?scope={SCOPE}&state={STATE}&redirect_uri={REDIRECT}&response_type=code&client_id={CLIENT_ID}")
        time.sleep(2)

        # Input Google email
        URL = self.browser.current_url
        if URL.startswith('https://accounts.google.com/o/oauth2/v2/auth/identifier'):
            usernameInput = self.browser.find_element_by_name('identifier')
            usernameInput.send_keys(self.keys['google']['EMAIL'])
            usernameInput.send_keys(Keys.ENTER)
            time.sleep(2)

        # Manually input verifcation code
        URL = self.browser.current_url
        if URL.startswith('https://accounts.google.com/o/oauth2/v2/auth/identifier'):
            input('Authentication.getGoogleAccessToken ==> Your input is necessary.  Press ENTER when done')

        # Input Google password
        URL = self.browser.current_url
        if URL.startswith('https://accounts.google.com/signin/v2/challenge/pwd'):
            passwordInput = self.browser.find_element_by_name('password')
            passwordInput.send_keys(self.keys['google']['PASSWORD'])
            passwordInput.send_keys(Keys.ENTER)
            time.sleep(2)

        # Allow authorization
        URL = self.browser.current_url
        if URL.startswith('https://accounts.google.com/signin/oauth/consent'):
            allowBtn = self.browser.find_element_by_id('submit_approve_access')
            allowBtn.click()
            time.sleep(2)

        # Get authorization code
        URL = self.browser.current_url
        par = urlparse.parse_qs(urlparse.urlparse(URL).query)
        self.keys['google']['AUTH_CODE'] = par['code'][0]
        print('Authentication.getGoogleAccessToken ==> Received Authorization Code!')
        
        # Get access token
        PARAMS = {
            'code': self.keys['google']['AUTH_CODE'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': self.keys['REDIRECT_URI'],
            'grant_type': 'authorization_code'
        }
        response = requests.post('https://www.googleapis.com/oauth2/v4/token', data = PARAMS)
        if response.status_code == 200:
            print('Authentication.getGoogleAccessToken ==> Received access token!\n') 
            r = response.json()
            self.keys['google']['ACCESS_TOKEN'] = r['access_token']  
            return True 
        else:
            print('Authentication.getGoogleAccessToken ==> Something went wrong!\n')
            print(response.json())  
            return False


def authenticationTest():
    # Try with keys
    auth = Authentication()
    print(auth.getGoogleAccessToken())
    
    input('Press any key to remove keys')
    auth.removeKeys()

    # Try without keys
    auth_no_keys = Authentication()
    print(auth_no_keys.getGoogleAccessToken())

if __name__ == '__main__':
    authenticationTest()