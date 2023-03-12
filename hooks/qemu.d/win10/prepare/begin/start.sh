#!/bin/bash

# Send info to log.txt
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>/home/david/Desktop/startlog.out 2>&1

# Isolate CPUs
systemctl set-property --runtime -- user.slice AllowedCPUs=0-15
systemctl set-property --runtime -- system.slice AllowedCPUs=0-15
systemctl set-property --runtime -- init.scope AllowedCPUs=0-15

#debugging
set -x

#load vars
source "/etc/libvirt/hooks/kvm.conf"

# Kill GDM3
systemctl stop gdm3.service

# I forgot what these do
echo 0 > /sys/class/vtconsole/vtcon0/bind
echo 0 > /sys/class/vtconsole/vtcon1/bind

# Sleep to let those changes apple
sleep 5

# Unload AMD and Intel Audio
modprobe -r amdgpu
modprobe -r snd_hda_intel

# Unbind GPU
#virsh nodedev-detach $VIRSH_GPU_VIDEO
#virsh nodedev-detach $VIRSH_GPU_AUDIO

# Load VFIO Drivers
modprobe vfio
modprobe vfio_pci
modprobe vfio_iommu_type1
