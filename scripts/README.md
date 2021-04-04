# AVAILABLE SCRIPTS
    !! Make sure the scripts folder is in your $PATH !!
    !! Make sure the scripts are executable !!

&nbsp;

## SCRIPTS FOR USING ENVIRONMENT VARIABLES
    All the important variables used for these scripts and libraries are located in the Parameter Store of AWS Systems Manager.Remember not to save sensitive information directly in scripts!


### set-env-variable 
*Add an environment variable to the Parameter Store*

#### Required Arguments
* -n, -name: Name of the variable
* -v, -value: Value of the variable
* -d, -desc: Description of the variable
#### Optional Arguments
* -t, -type: Type of variable. Choices: 'String'|'StringList'|**'SecureString'**
* -o, -overwrite: Whether to overwrite the variable value, if it already exists. Choices: True|**False**

#### Output
Returns nothing, if successful

#### Example
```
set-env-variable -n 'testVariable' -v '1234567890' -d 'A variable for testing only' -t 'String' -o True
```
&nbsp;

### get-env-variable
*Retrieve an environment variable from the Parameter Store*

#### Required Arguments
* -n, -name: Name of the variable

&nbsp;

### delete-env-variable 
*Delete an environment variable from the Parameter Store*

#### Required Arguments
* -n, -name: Name of the variable


## SCRIPTS FOR DEALING WITH USERS
    All the important variables used for these scripts and libraries are located in the Parameter Store of AWS Systems Manager.Remember not to save sensitive information directly in scripts!


### get-okta-user-list
*Obtain a list of all users in an Okta instance*

&nbsp;

**onboard-new-employees**
**reset-gsuite-passwords.py** - *Resets GSuite password for all users*

**update-gsuite-emails**
**update-slack-emails**
**update-zoom-emails**

**send-email**
**send-text**

You will need access tokens to use many of the methods in the Staff class. The `getKeys()` method in the *Authentication* class will retrieve them from the *ADMIN_KEYS.py* file for use in other methods. A template for this file is included in the *files* directory.

*  Option 1: Place a copy of ADMIN_KEYS.py in the root directory.  The `removeKeys()` function will delete the file after each run of a script. 
*  Option 2: If no copy of ADMIN_KEYS.py is found in the root directory, `getKeys()` will ask you to provide the path to your key file.

**DO NOT UPLOAD YOUR KEYS TO A REPOSITORY! KEEP THEM STORED IN A SECURE PLACE!**

#### GOOGLE
To use the [G Suite Admin SDK](https://developers.google.com/admin-sdk), all requests must include an authorization token which is provided by 
Google to an authorized user.  You'll need a client ID and client secret.  Follow the instructions [here](https://developers.google.com/admin-sdk/directory/v1/guides/authorizing) to get the required credentials.  The `getGoogleAccessToken()` function will use the credentials in ADMIN_KEYS.py to take you through the OAuth flow and retrieve the necessary access token.  Manual input may be required.

#### SLACK
You can provision and manage user accounts and groups with the Slack SCIM API. An OAuth token with the admin scope is required to access the SCIM API. The simplest way to acquire this token is for an admin on a Workspace to create a new Slack app, add the admin OAuth scope, install the app, and use the generated token.  More information can be found [here](https://api.slack.com/scim)

#### ZOOM
Zooms API uses OAuth and JWT to authenicate API requests. This library uses a JWT app. You can generate your API credentials for your app by logging into [Marketplace](http://marketplace.zoom.us/) and [creating a JWT app](https://marketplace.zoom.us/docs/guides/getting-started/app-types/create-jwt-app).

#### TWILIO
All requests to Twilio's REST API require you to authenticate. Your AccountSid and AuthToken are the "master keys" to your account. To authenticate using these "master keys," use HTTP basic auth with the username set to your AccountSid and the password set to your AuthToken. Your AccountSid and AuthToken can be found on your [Account Dashboard](https://www.twilio.com/console).

#### THE REST
You get the point.  Look it up and add the software application tokens you use for your own scripts.

## USAGE 



#### CLASSES:

**Authentication** - A library for obtaining and using credentials for scripts

1. getKeys(keyFilePath)
2. removeKeys()
3. getGoogleAccessToken()

**Communication** - A library for sending correspondence via email and SMS

1. sendSMS(destination, msg)
2. sendEmail(destination, msg)
 
**Staff** - A library for performing user related tasks

1. getUserList(usersFilePath)
2. getAllGSuiteUsers(nextPageToken)
3. addGSuiteUser(user)
4. removeGSuiteUser(userEmail)
5. resetGSuitePassword(user)
6. addToGSuiteGroups(user, groups)
7. createSlackAccount(user)
8. createZoomAccount()
9. createHarvestAccount()
10. scheduleOrientation()
11. sendWelcomeMail()


**Happy coding!**