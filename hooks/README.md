## Dependencies


```sh
sudo apt install qemu-kvm qemu-utils libvirt-daemon-system libvirt-clients bridge-utils virt-manager ovmf
```

Reboot

```sh
sudo virsh net-start default
sudo virsh net-autostart default
usermod -aG kvm,input,libvirt $USER
```

## Preping GRUB

Inside of GRUB (`/etc/default/grub`)

Add `amd_iommu=on iommu=pt iommu=1` on the end of `GRUB_CMDLINE_LINUX_DEFAULT` inside of `/etc/default/grub`

Should look something like: `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amd_iommu=on iommu=pt iommu=1"`

Run `sudo grub-mkconfig -o /boot/grub/grub.cfg && sudo reboot now` to apply.

## To Verify IOMMU Groups the following script can be run:

```sh
#!/usr/bin/env bash
shopt -s nullglob
for g in `find /sys/kernel/iommu_groups/* -maxdepth 0 -type d | sort -V`; do
    echo "IOMMU Group ${g##*/}:"
    for d in $g/devices/*; do
        echo -e "\t$(lspci -nns ${d##*/})"
    done;
done;
```

## File Placement
The hooks folder files would reside inside of `/etc/libvirt/`

- Under `/hooks/qemu.d/` the name after this is the name of your vm. 
- So for a vm named "win-10" it would be `/etc/libvirt/hooks/qemu.d/win-10/`

Make sure that you can execute the scripts when needed

```sh
chmod +x /etc/libvirt/hooks/qemu.d/ [VM NAME IN QEMU] /prepare/begin/start.sh 
chmod +x /etc/libvirt/hooks/qemu.d/ [VM NAME IN QEMU] /release/end/revert.sh
```

and the GPU BIOS (in my case an MSI RX 6600 XT) would reside in `/usr/share/vgabios/GPU.rom`

While other sources tell me that AMD GPUs don't need this, I had a lot of issues without it.

## VM Details

| Detail                | Setting |
|:---------------------:|:----|
| Chipset               | Q35 
| Emulator              | `/usr/share/OVMF/OVMF_CODE_4M.ms.fd` 
| CPU Topology          | Manual (almost identical but leave some cores for Linux) 
| NIC                   | `NAT` and `e1000e` 
| PCI Host Device       | Your GPU 
| PCI Host Device       | GPUs Audio Device 
| (USB) PCI Host Device | Your Keyboard 
| (USB) PCI Host Device | Your Mouse 

## And edit the Overview XML, placing this line inside the hyperv tags
```xml
<hyperv mode="custom">
  <!--  Leave the Usual Stuff -->
  <vendor_id state="on" value="12345"/>
</hyperv>
```

## CPU Pinning

By default the scripts in this folder pin threads 16 - 31 to Linux.

Under the tag `<vcpu placement...` add the following snippet

```xml
<cputune>
    <vcpupin vcpu="0" cpuset="0"/>
    <vcpupin vcpu="1" cpuset="1"/>
    <vcpupin vcpu="2" cpuset="2"/>
    <vcpupin vcpu="3" cpuset="3"/>
    <vcpupin vcpu="4" cpuset="4"/>
    <vcpupin vcpu="5" cpuset="5"/>
    <vcpupin vcpu="6" cpuset="6"/>
    <vcpupin vcpu="7" cpuset="7"/>
    <vcpupin vcpu="8" cpuset="8"/>
    <vcpupin vcpu="9" cpuset="9"/>
    <vcpupin vcpu="10" cpuset="10"/>
    <vcpupin vcpu="11" cpuset="11"/>
    <vcpupin vcpu="12" cpuset="12"/>
    <vcpupin vcpu="13" cpuset="13"/>
    <vcpupin vcpu="14" cpuset="14"/>
    <vcpupin vcpu="15" cpuset="15"/>
</cputune>
```

This of course assumes youre giving 8 cores to the guest, and leaving 8 to the host.

And inside of the `<cpu>` tags (for AMD CPUs) add this line

```xml
feature policy="require" name="topoext"/>
```

CPU Pinning loves to freak out and assume your CPU is capable of hyperthreading. This handles it for AMD CPUs.

## Edit the GPUs XML As Follows:

```xml
<hostdev mode="subsystem" type="pci" managed="yes">
  <source>
    <!--  Leave the Usual Stuff -->
  </source>
  <rom file="/usr/share/vgabios/GPU.rom"/>
  <!--  Leave the Usual Stuff -->
</hostdev>
```

Where do I get a GPU vBIOS?

You can either rip your own using GPU-Z on Windows or find your **exact model** [here](https://www.techpowerup.com/vgabios/)

## Credits

Shoutout to [QaidVoids Single GPU Passthrough Guide](https://github.com/QaidVoid/Complete-Single-GPU-Passthrough) and the [VFIO Subreddit](https://reddit.com/r/VFIO) and the random users across MANY boards who have run into these issues in the past. ❤️
