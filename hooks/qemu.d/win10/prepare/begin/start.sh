#debugging
set -x

#load vars
source "/etc/libvirt/hooks/kvm.conf"

#stop display manager
systemctl stop gdm3.service
killall gdm-wayland-session

pulse_pid=$(pgrep -u YOURUSERNAME pulseaudio)
pipewire_pid=$(pgrep -u YOURUSERNAME pipewire-media)
kill $pulse_pid
kill $pipewire_pid

echo 0 > /sys/class/vtconsole/vtcon0/bind
echo 0 > /sys/class/vtconsole/vtcon1/bind

#Unbind efi framebuffer
#echo efi-framebuffer.0 > /sys/bus/platform/drivers/efi-framebuffer/unbind

#echo -n "pci_0000_28_00_0" > /sys/bus/pci/drivers/amdgpu/unbind
#echo -n "pci_0000_28_00_1" > /sys/bus/pci/drivers/snd_hda_intel/unbind

sleep 10

# Unload AMD
#modprobe -r drm_kms_helper
modprobe -r amdgpu
#modprobe -r radeon
#modprobe -r drm
modprobe -r snd_hda_intel

# unbind gpu
virsh nodedev-detach $VIRSH_GPU_VIDEO
virsh nodedev-detach $VIRSH_GPU_AUDIO

#load vfio
modprobe vfio
modprobe vfio_pci
modprobe vfio_iommu_type1
