#!/usr/bin/env bash

set -u

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

#
#    This function is for apt packages
#
#    It takes 1 arguement
#      1: the apt package
#      2: (optional) The repo that it is in
#
get-apt () {
	echo ""
	echo "--------------------------------------------------"
	echo "                  Getting $1 "
	echo "--------------------------------------------------"
	echo ""
	sleep 1s
	if [ $# -eq 1 ]
		then
			echo "apt-get install $1 -y"
		else
			echo "add-apt-repository $2"
			echo "apt update"
			echo "apt-get install $1 -y"
	fi
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

	echo "wget -O $1.deb '$2'"

echo ""
	echo "--------------------------------------------------"
	echo "                  Installing $1 "
	echo "--------------------------------------------------"
	echo ""
	sleep 1s
	echo "dpkg -i $1.deb"
}

: '
echo "--------------------------------------------------"
echo "      This script will install a lot of stuff.    "
echo " It may take a while depending on internet speed. "
echo "      The script will start in 10 seconds.        "
echo "                CTRL + C to Abort                 "
echo "          THIS WILL REBOOT YOUR SYSTEM            "
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

get-apt bridge-utils
get-apt code "'deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main'"
get-apt curl
get-apt git
get-apt gnome-tweaks
get-apt qemu-kvm
get-apt qemu-utils
get-apt libvirt-daemon-system
get-apt libvirt-clients
get-apt openjdk-17-jdk
get-apt openjdk-17-jre
get-apt ovmf
get-apt python3
get-apt qemu-kvm
get-apt steam
get-apt virt-manager
get-apt wine
get-apt virt-manager
'

#get-deb discord 'https://discord.com/api/download?platform=linux&format=deb'
#get-deb vivaldi 'https://downloads.vivaldi.com/stable/vivaldi-stable_5.6.2867.62-1_amd64.deb'

BOOT_CONFIG_FILE="/etc/default/grub"

if ! grep -i -q "amd_iommu" "$BOOT_CONFIG_FILE"; then
    $(sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/&amd_iommu=on iommu=pt /' "$BOOT_CONFIG_FILE")
else 
    echo "AMD IOMMU All Good!"
fi

echo "grub-update"

echo "cp -R ./hooks/ /etc/libvirt/"

echo "usermod -a -G libvirt $(whoami)"

echo "systemctl start libvirt"

echo "systemctl enable libvirt"

echo "reboot now"
