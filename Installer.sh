#!/usr/bin/env bash

set -u

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

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

RED="\e[31m"
ENDCOLOR="\e[0m"

get-apt () {
	echo -e "\n             Getting $1 "
	echo -e "--------------------------------------------------\n"	
	
	apt-get install $1 -y &> /dev/null
}



echo -e "\n${RED}"
echo -e "   THIS SCRIPT WILL REBOOT WHEN IT IS FINISHED    "

while [ $secs -gt 0 ]; do
	echo -ne "       It will start in $secs seconds.\033[0K\r"
	sleep 1
	: $((secs--))
done
 

echo -e "\n${ENDCOLOR}--------------------------------------------------"
echo -e "                  Updating APT                    "
echo -e "--------------------------------------------------\n"

apt update

for i in "${Packages[@]}"; do get-apt "$i"; done

BOOT_CONFIG_FILE="/etc/default/grub"

if ! grep -i -q "amd_iommu" "$BOOT_CONFIG_FILE"; then
    $(sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/&amd_iommu=on iommu=pt /' "$BOOT_CONFIG_FILE")
else 
    echo "AMD IOMMU All Good!"
fi

grub-update

cp -R ./hooks/ /etc/libvirt/

usermod -a -G libvirt $(whoami)

systemctl start libvirt

systemctl enable libvirt

reboot now
