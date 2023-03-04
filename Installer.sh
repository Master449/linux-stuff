#!/usr/bin/env bash

set -u

DryRun=true

# Check if script is run as root if not, exit
# if DryRun is true, it will not exit
if [ $DryRun = true ]; then
	echo "--------Dry Run-------"
else
	if [[ $EUID -ne 0 ]]; then
   		echo "This script must be run as root" 
   		exit 1
	fi
fi

# Packages to install
Packages=(
	bridge-utils
	cifs-utils
	curl
	git
	gnome-shell-extensions
	gnome-shell-extension-manager
	gnome-tweaks
	htop
	libvirt-daemon-system
	libvirt-clients
	neovim
	openjdk-17-jdk
	openjdk-17-jre
	ovmf
	python3
	qemu-kvm
	qemu-utils
	steam
	virt-manager
	wine
)

# Countdown Timer
# If it's a dry run, it will only be 1 second
if [ $DryRun = true ]; then
	countdownSeconds=1
else
	countdownSeconds=10
fi

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
	
	if [ $DryRun = true ]; then
		echo "apt-get install $1 -y &> /dev/null"
	else
		apt-get install $1 -y &> /dev/null
	fi
}



echo -e "\n${RED}"
echo -e "   THIS SCRIPT WILL REBOOT WHEN IT IS FINISHED    "

# Countdown
while [ $countdownSeconds -gt 0 ]; do
	echo -ne "       It will start in $countdownSeconds seconds.\033[0K\r"
	sleep 1
	: $((countdownSeconds--))
done
 
# Update APT before installing
echo -e "\n${ENDCOLOR}--------------------------------------------------"
echo -e "                  Updating APT                    "
echo -e "--------------------------------------------------\n"

if [ $DryRun = true ]; then
	echo "apt update"
	echo "apt upgrade -y"
else
	apt update
	apt upgrade -y
fi

# Loop to call get-apt function
for i in "${Packages[@]}"; do get-apt "$i"; done

# Check if IOMMU is enabled
if ! grep -i -q "amd_iommu" "$BOOT_CONFIG_FILE"; then
	if [ $DryRun = true ]; then
		echo "Edit $BOOT_CONFIG_FILE and add amd_iommu=on iommu=pt to GRUB_CMDLINE_LINUX_DEFAULT"
	else
    	$(sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/&amd_iommu=on iommu=pt /' "$BOOT_CONFIG_FILE")
    	grub-update
	fi
else 
    echo "AMD IOMMU All Good!"
fi

# Check if libvirt hooks folder exists
if [ -d "/etc/libvirt/hooks" ]; then
	echo "Libvirt hooks folder found. Leaving Alone."
else
	if [ $DryRun = true ]; then
		echo "cp -R ./hooks/ /etc/libvirt/"
	else
		cp -R ./hooks/ /etc/libvirt/
	fi
fi

# Add user to libvirt group
if [ $DryRun = true ]; then
	echo "usermod -a -G libvirt $(whoami)"
else
	usermod -a -G libvirt $(whoami)
fi

# Check if libvirt service is running
if [ $(systemctl is-active libvirtd) ]; then
	echo "Libvirt Service found. Leaving Alone."
else
	if [ $DryRun = true ]; then
		echo "systemctl start libvirt"
		echo "systemctl enable libvirt"
	else
		systemctl start libvirt
    	systemctl enable libvirt
	fi
fi

if [ $DryRun = true ]; then
	echo "Rebooting in 10 seconds"
else
	echo "Rebooting in 10 seconds"
	sleep 10
	reboot now
fi
