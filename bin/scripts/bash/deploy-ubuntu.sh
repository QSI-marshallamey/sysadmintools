#! /bin/bash

# Change to ROOT
sudo su

echo 'DOWNLOADING REPOSITORIES...'
wget https://github.com/oguzhaninan/Stacer/releases/download/v1.0.4/Stacer_1.0.4_amd64.deb
wget https://go.skype.com/skypeforlinux-64.deb
add-apt-repository "deb https://deb.opera.com/opera/ stable non-free"
wget -O - https://deb.opera.com/archive.key | apt-key add -
add-apt-repository ppa:kelleyk/emacs -y
add-apt-repository ppa:kasra-mp/ubuntu-indicator-weather -y
add-apt-repository ppa:peek-developers/stable -y
add-apt-repository ppa:kazam-team/stable-series -y

echo 'UPDATING APT...'
apt update

echo 'INSTALLING APPLICATIONS...'
apt install emacs26 conky indicator-weather peek kazam opera-stable ./skypeforlinux-64.deb -y
dpkg --install Stacer_1.0.4_amd64.deb
snap install --classic code
snap install spotify
snap install tldr
sudo -v && wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sh /dev/stdin

# Change back to USER
sudo su marshall

# Add .bash_aliases
echo 'ADDING YOUR ALIASES...'
cp ~/pCloudDrive/Installers/Linux/config/.bash_aliases ~/

# Add VSCode configs
echo 'CONFIGURING VSCODE...'
cp ~/pCloudDrive/Installers/Settings/Code/settings.json ~/.config/Code/User
cp -r ~/pCloudDrive/Installers/Settings/Code/extensions/. ~/.vscode/extensions

#Connect to nordVPN
echo 'ADDING NORDVPN...'
sudo apt install ~/pCloudDrive/Installers/Linux/nordvpn-release_1.0.0_all.deb -y
sudo apt update -y
sudo apt install nordvpn -y
nordvpn login
nordvpn connect

sudo apt upgrade -y
echo 'UBUNTU CONFIGURATION COMPLETE!!\n\n'


