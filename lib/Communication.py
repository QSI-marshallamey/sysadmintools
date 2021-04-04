#! /usr/bin/env python3

'''
COMMUNICATION
A class for sending/receiving correspondence via email and SMS

VARIABLES

    TwilioNumber = '+14152127915'   
    gmailServer = 'smtp.gmail.com'
    gmailPort = 587

FUNCTIONS

    __init__(keyFilePath):
        Description: Creates an Authentication object. The default keyFilePath is ./myAdminKeys.py
        Arguments: (keyFilePath) Path to the file containing the API and oAuth keys
        Returns: None

    sendSMS(self, destination, msg):   
        Description: 
        Arguments: None
        Returns: None

    sendEmail(self, destination, msg):
        Description: 
        Arguments: None
        Returns: None

    getEmail(self, username, password):
        Description: 
        Arguments: None
        Returns: None

    * More to come...
'''
from datetime import date
from twilio.rest import Client
from imapclient import IMAPClient
# import pyzmail


class Communication:

    TwilioNumber = '+14152127915'   
    gmailServer = 'smtp.gmail.com'
    gmailPort = 587

    def __init__(self, auth = None):
        # Save keys in file keys object
        #For every user, format data and add to user list
        self.auth = auth

    def sendSMS(self, destination, msg):   
        print(self.auth)
        twilioCli = Client(self.auth.keys['twilio']['ACCOUNT_SID'], self.auth.keys['twilio']['ACCESS_TOKEN'])
        message = twilioCli.messages.create(
            body = msg, 
            from_ = self.TwilioNumber, 
            to = destination,
        )
        print(message.sid)

    def sendEmail(self, destination, msg):
        username = self.auth.keys['google']['EMAIL']
        password = self.auth.keys['google']['PASSWORD']          
        from smtplib import SMTP
        server = SMTP(self.gmailServer, self.gmailPort)
        print('Saying hello to Gmail:', server.ehlo())
        print('Starting TLS:', server.starttls())
        print('Logging in:', server.login(username, password))
        print('Sending mail:', server.sendmail(username, destination, msg))
        print('Disconnecting from server:', server.quit())

    def login(self, username, password):
        
        server = IMAPClient('imap.gmail.com', ssl=True)
        return server.login(username, password)

    def getEmail(self, username, password):
        server = IMAPClient('imap.gmail.com', ssl=True)
        print('Logging in:', server.login(username, password))
        import pprint
        pprint.pprint(server.list_folders())
        server.select_folder('INBOX', readonly=True)
        UIDs = server.search([u'ON', date(2019, 4, 25)])
        messages = server.fetch(UIDs, ['BODY[]'])
        
        # for UID in UIDs:
        #     #print(messages[UID])
        #     message = pyzmail.PyzMessage.factory(messages[UID][b'BODY[]'])
        #     print('EMAIL', UID)
        #     print(message.get_subject())
        #     print('FROM:', message.get_addresses('from'))
        #     print('TO:', message.get_addresses('to'))
        #     print('CC:', message.get_addresses('cc'))
        #     if message.text_part != None:
        #         if message.text_part.charset != None:
        #             print(message.text_part.get_payload().decode(message.text_part.charset))
        #             input('Press ENTER to see next message')


def communicationTest():
    return None

if __name__ == '__main__':
    communicationTest()
#c = Communication()
#c.sendSMS(marshallCell, 'Hey Marshall!!')
#c.sendEmail(marshallEmail, 'Subject: TEST MESSAGE2\nThis is a test message.  Hello WORLD!')
#c.getEmail()