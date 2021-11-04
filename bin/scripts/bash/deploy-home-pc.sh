
xcode-select --install

#Install homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

brew tap caskroom/cask
brew install awscli git node yarn python@3.8 postgresql
brew cask install notion calibre chromedriver cyberduck docker emacs google-chrome microsoft-office zoomus nordvpn adobe-creative-cloud alfred aerial iterm2 java transmission slack kindle lastpass little-snitch plex local spotify vnc-viewer visual-studio-code vlc

#pcloud spark trello