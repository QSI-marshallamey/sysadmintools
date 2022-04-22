# AVAILABLE SCRIPTS
    !! Make sure the scripts folder is in your $PATH !!
    !! Make sure the scripts are executable !!

&nbsp;
## SCRIPTS FOR OKTA
---
### 1. clean-up-okta-groups
*Removes all deactivated users from groups*
#### Required Arguments
* -c, -company: Subdomain of Okta URL  (Using 'all' with comma-separated list as env variable (COMPANIES) will run as loop)

## SCRIPTS FOR USING ENVIRONMENT VARIABLES
---
All the important variables used for these scripts and libraries are located in the Parameter Store of AWS Systems Manager.Remember not to save sensitive information directly in scripts!

### 1. set-env-variable 
*Adds an environment variable to the AWS Parameter Store*

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

### 2. get-env-variable
*Retrieves an environment variable from the AWS Parameter Store*

#### Required Arguments
* -n, -name: Name of the variable

#### Example
```
get-env-variable -name 'testVariable'
```

&nbsp;

### 3. delete-env-variable 
*Delete an environment variable from the AWS Parameter Store*

#### Required Arguments
* -n, -name: Name of the variable

#### Example
```
delete-env-variable -name 'testVariable'
```

&nbsp;

## SCRIPTS FOR DEALING WITH USERS
---
All the important variables used for these scripts and libraries are located in the Parameter Store of AWS Systems Manager.Remember not to save sensitive information directly in scripts!

### 1. get-okta-user-list
*Obtains a list of all users in an Okta instance*

&nbsp;

### 2. reset-gsuite-password
*Resets GSuite password for one or more users*

&nbsp;

### 3. update-gsuite-emails

&nbsp;

### 4. update-slack-emails

&nbsp;

### 5. update-zoom-emails

&nbsp;

## SCRIPTS FOR ONBOARDING
---
### 1. onboard-new-employees

&nbsp;

## SCRIPTS FOR COMMUNICATING
---
### 1. send-email

&nbsp;

### 2. send-text

