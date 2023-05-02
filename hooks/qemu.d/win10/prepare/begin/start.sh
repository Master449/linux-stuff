#!/bin/bash

# Send info to log.txt
exec 1>/home/david/Desktop/startlog.out 2>&1

# Isolate CPUs
systemctl set-property --runtime -- user.slice AllowedCPUs=8-15,24-31
systemctl set-property --runtime -- system.slice AllowedCPUs=8-15,24-31
systemctl set-property --runtime -- init.scope AllowedCPUs=8-15,24-31

#debugging
set -x

#load vars
source "/etc/libvirt/hooks/kvm.conf"

# Kill Display Manager
systemctl stop display-manager

# These are unneeded on AMD 6000 GPUs
#echo 0 > /sys/class/vtconsole/vtcon0/bind
#echo 0 > /sys/class/vtconsole/vtcon1/bind

# Sleep to let those changes apple
sleep 5

# Unload AMD and Intel Audio
modprobe -r amdgpu
modprobe -r snd_hda_intel

# Load VFIO Drivers
modprobe vfio
modprobe vfio_pci
modprobe vfio_iommu_type1
