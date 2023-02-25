#!/usr/bin/env bash

set -u

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Packages to install
Packages=(
	bridge-utils
	curl
	git
	gnome-tweaks
	qemu-kvm
	qemu-utils
	libvirt-daemon-system
	libvirt-clients
	openjdk-17-jdk
	openjdk-17-jre
	ovmf
	python3
	qemu-kvm
	steam
	virt-manager
	wine
	virt-manager
)

secs=10

# Boot config file to add IOMMU too (if not there)
BOOT_CONFIG_FILE="/etc/default/grub"

# Just some colors
RED="\e[31m"
ENDCOLOR="\e[0m"

# Function to install packages
#   Sends output to /dev/null
get-apt () {
	echo -e "\n             Getting $1 "
	echo -e "--------------------------------------------------\n"	
	
	apt-get install $1 -y &> /dev/null
}



echo -e "\n${RED}"
echo -e "   THIS SCRIPT WILL REBOOT WHEN IT IS FINISHED    "

# Countdown
while [ $secs -gt 0 ]; do
	echo -ne "       It will start in $secs seconds.\033[0K\r"
	sleep 1
	: $((secs--))
done
 
# Update APT before installing
echo -e "\n${ENDCOLOR}--------------------------------------------------"
echo -e "                  Updating APT                    "
echo -e "--------------------------------------------------\n"

apt update

# Loop to call get-apt function
for i in "${Packages[@]}"; do get-apt "$i"; done

# Check if IOMMU is enabled
if ! grep -i -q "amd_iommu" "$BOOT_CONFIG_FILE"; then
    $(sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/&amd_iommu=on iommu=pt /' "$BOOT_CONFIG_FILE")
    grub-update
else 
    echo "AMD IOMMU All Good!"
fi

# Check if libvirt hooks folder exists
if [ -d "/etc/libvirt/hooks" ]; then
	echo "Libvirt hooks folder found. Leaving Alone."
else
	cp -R ./hooks/ /etc/libvirt/
fi

# Add user to libvirt group
usermod -a -G libvirt $(whoami)

# Check if libvirt service is running
if [ $(systemctl is-active libvirtd) ]; then
	echo "Libvirt Service found. Leaving Alone."
else
	systemctl start libvirt
    systemctl enable libvirt
fi

#reboot now
