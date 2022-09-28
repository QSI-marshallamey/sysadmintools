# System Admin Tools
*This is a toolbox for easy Python scripting in IT and System Administration*

### CLASSES:

#### ADMIN

#### AWS

#### GOOGLE
To use the [G Suite Admin SDK](https://developers.google.com/admin-sdk), all requests must include an authorization token which is provided by 
Google to an authorized user.  You'll need a client ID and client secret.  Follow the instructions [here](https://developers.google.com/admin-sdk/directory/v1/guides/authorizing) to get the required credentials.  The `getGoogleAccessToken()` function will use the credentials in ADMIN_KEYS.py to take you through the OAuth flow and retrieve the necessary access token.  Manual input may be required.

#### OKTA

#### SLACK
You can provision and manage user accounts and groups with the Slack SCIM API. An OAuth token with the admin scope is required to access the SCIM API. The simplest way to acquire this token is for an admin on a Workspace to create a new Slack app, add the admin OAuth scope, install the app, and use the generated token.  More information can be found [here](https://api.slack.com/scim)

#### ZOOM
Zooms API uses OAuth and JWT to authenicate API requests. This library uses a JWT app. You can generate your API credentials for your app by logging into [Marketplace](http://marketplace.zoom.us/) and [creating a JWT app](https://marketplace.zoom.us/docs/guides/getting-started/app-types/create-jwt-app).

#### TWILIO
All requests to Twilio's REST API require you to authenticate. Your AccountSid and AuthToken are the "master keys" to your account. To authenticate using these "master keys," use HTTP basic auth with the username set to your AccountSid and the password set to your AuthToken. Your AccountSid and AuthToken can be found on your [Account Dashboard](https://www.twilio.com/console).

#### THE REST
You get the point.  Look it up and add the software application tokens you use for your own scripts.

## USAGE 

