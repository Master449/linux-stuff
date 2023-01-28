#!/usr/bin/env bash

set -u

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

#
#    This function is for apt packages
#    It takes 1 arg
#
#      1: the apt package
#
get-apt () {
	echo ""
	echo "--------------------------------------------------"
	echo "                  Getting $1 "
	echo "--------------------------------------------------"
	echo ""
	sleep 1s
	
	apt-get install $1 -y
}

#
#    This function is for deb packages
#    These are for applications that I don't want hindered
#    by being snap/flatpak packages
#    
#    This function takes 2 args
#      1: What to name the wget file
#      2: The deb download link
#
get-deb () {
	echo ""
	echo "--------------------------------------------------"
	echo "                  Downloading $1 "
	echo "--------------------------------------------------"
	echo ""
	sleep 1s
	
	wget -O $1.deb '$2'
	dpkg -i $1.deb
}

echo "--------------------------------------------------"
echo "      This script will install a lot of stuff.    "
echo "  It may take a while depending on internet speed."
echo "      The script will start in 10 seconds.        "
echo "                CTRL + C to Abort                 "
echo "--------------------------------------------------"
sleep 7s
echo "3"
sleep 1s
echo "2"
sleep 1s
echo "1"
sleep 1s

# apt 
echo ""
echo "--------------------------------------------------"
echo "                  Updating APT                    "
echo "--------------------------------------------------"
echo ""
sleep 1s
echo "apt update"

get-apt curl
get-apt git
get-apt gnome-tweaks
get-apt libvirt-daemon
get-apt openjdk-17-jdk
get-apt openjdk-17-jre
get-apt python3
get-apt qemu-kvm
get-apt steam
get-apt virt-manager
get-apt wine

get-deb discord 'https://discord.com/api/download?platform=linux&format=deb'
get-deb vivaldi 'https://downloads.vivaldi.com/stable/vivaldi-stable_5.6.2867.62-1_amd64.deb'
