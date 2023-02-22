#debugging
set -x

# PCIe Variables
source "/etc/libvirt/hooks/kvm.conf"

# Kill the display managers and sessions
systemctl stop gdm3.service
killall gdm-wayland-session

# Kill Pulse Audio (for GPU HDMI)
pulse_pid=$(pgrep -u YOURUSERNAME pulseaudio)
pipewire_pid=$(pgrep -u YOURUSERNAME pipewire-media)
kill $pulse_pid
kill $pipewire_pid

echo 0 > /sys/class/vtconsole/vtcon0/bind
echo 0 > /sys/class/vtconsole/vtcon1/bind

# Sleep to let all that finish
sleep 5

# Unload AMD and Intel Audio Drivers
modprobe -r amdgpu
modprobe -r snd_hda_intel

# Unbind the GPU
virsh nodedev-detach $VIRSH_GPU_VIDEO
virsh nodedev-detach $VIRSH_GPU_AUDIO

# Load VFIO Drivers
modprobe vfio
modprobe vfio_pci
modprobe vfio_iommu_type1
