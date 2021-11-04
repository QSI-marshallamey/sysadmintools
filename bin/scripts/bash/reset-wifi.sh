#!/bin/bash

# Remove and reinsert the Wifi kernel module
modprobe -r mwifiex_pcie
modprobe mwifiex_pcie

#Restart Network Manager
echo 'Restarting Network Manager.  Please wait...'
service network-manager restart
