#!/bin/bash

# Send info to log.txt
exec 1>/home/david/Desktop/revertlog.out 2>&1

# Unpin CPUs
systemctl set-property --runtime -- user.slice AllowedCPUs=0-31
systemctl set-property --runtime -- system.slice AllowedCPUs=0-31
systemctl set-property --runtime -- init.scope AllowedCPUs=0-31

# debugging
set -x

# load vars
source "/etc/libvirt/hooks/kvm.conf"

# Unload VFIO
modprobe -r vfio_pci
modprobe -r vfio_iommu_type1
modprobe -r vfio

# Rebind GPU
virsh nodedev-reattach $VIRSH_GPU_VIDEO
virsh nodedev-reattach $VIRSH_GPU_AUDIO

# Load AMD and Intel Audio Drivers
modprobe amdgpu
modprobe snd_hda_intel

# Sleep to let it apply
sleep 3

# start gdm3
systemctl start display-manager
