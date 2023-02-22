# debugging
set -x

# PCIe Variables
source "/etc/libvirt/hooks/kvm.conf"

# Unload VFIO
modprobe -r vfio_pci
modprobe -r vfio_iommu_type1
modprobe -r vfio

# Rebind the GPU
virsh nodedev-reattach $VIRSH_GPU_VIDEO
virsh nodedev-reattach $VIRSH_GPU_AUDIO

# Rebind VTconsoles
echo 1 > /sys/class/vtconsole/vtcon0/bind
echo 0 > /sys/class/vtconsole/vtcon1/bind

# Reload AMD and Intel Audio Drivers
modprobe amdgpu
modprobe snd_hda_intel

sleep 3

# Start GDM3
systemctl start gdm3.service

# Login screen should pop-up shortly after the end of this
