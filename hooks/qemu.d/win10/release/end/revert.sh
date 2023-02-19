# debugging
set -x

# load vars
source "/etc/libvirt/hooks/kvm.conf"

# unload vfio
modprobe -r vfio_pci
modprobe -r vfio_iommu_type1
modprobe -r vfio

# bind gpu
virsh nodedev-reattach $VIRSH_GPU_VIDEO
virsh nodedev-reattach $VIRSH_GPU_AUDIO

# rebind VTconsoles
echo 1 > /sys/class/vtconsole/vtcon0/bind
echo 0 > /sys/class/vtconsole/vtcon1/bind

# bind efi framebuffer
# echo "efi-framebuffer.0" > /sys/bus/platform/drivers/efi-framebuffer/bind

#echo "pci_0000_28_00_0" > /sys/bus/pci/drivers/amdgpu/bind
#echo "pci_0000_28_00_1" > /sys/bus/pci/drivers/snd_hda_intel/bind

# load amd drivers
#modprobe drm
modprobe amdgpu
modprobe snd_hda_intel
#modprobe radeon
#modprobe drm_kms_helper

sleep 3

# start gdm3
systemctl start gdm3.service
