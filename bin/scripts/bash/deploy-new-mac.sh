#!/bin/bash


#Allow apps to install
sudo spctl --master-disable

#Asks for the name of the new user

#terminal name (lowercase first letter)
read -p "Enter Username: "  username

#log in name (uppercase first letter)
read -p "Enter Realname: "  realname

#Create the User's Account
sudo dscl . -create /Users/$username
sudo dscl . -create /Users/$username UserShell /bin/bash
sudo dscl . -create /Users/$username RealName "$realname" 
sudo dscl . -create /Users/$username UniqueID "510"
sudo dscl . -create /Users/$username PrimaryGroupID 20
sudo dscl . -create /Users/$username NFSHomeDirectory /Users/$username
sudo dscl . -passwd /Users/$username Color123
sudo fdesetup add -usertoadd $username -p -keychain Color123
sudo dscl . -append /Groups/admin GroupMembership $username

# Changes the name of the computer
sudo scutil --set ComputerName "${username}-MacBook"
sudo scutil --set LocalHostName "${username}-MacBook"
sudo scutil --set HostName "${username}-MacBook"

# Install Chrome, meraki, and zoom

#Let stuff install

sleep 30

sudo installer -pkg ~/Downloads/newmac/zoomusInstaller.pkg -target /

sudo installer -pkg ~/Downloads/newmac/Chrome-65.0.3325.181.pkg -target /

sudo installer -pkg ~/Downloads/newmac/Slack-3.1.0.pkg -target /

#Install homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

brew tap caskroom/cask
brew install awscli git node yarn python@3.8 postgresql
brew cask install notion calibre chromedriver cyberduck docker emacs google-chrome microsoft-office zoomus nordvpn adobe-creative-cloud alfred aerial iterm2 java transmission slack kindle lastpass little-snitch plex local spotify vnc-viewer visual-studio-code vlc

#pcloud spark trello
