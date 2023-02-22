## Tools Needed

Run `sudo apt install qemu-kvm qemu-utils libvirt-daemon-system libvirt-clients bridge-utils virt-manager ovmf`

Reboot

Run `sudo virsh net-start default`

Run `sudo virsh net-autostart default`

## Preping GRUB

Add `amd_iommu=on iommu=pt iommu=1 video=efifb:off` on the end of `GRUB_CMDLINE_LINUX_DEFAULT` inside of `/etc/default/grub`

Run `sudo grub-mkconfig -o /boot/grub/grub.cfg` to apply.

Reboot.

To Verify IOMMU Groups the following script can be run:

```sh
#!/bin/bash
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

While other sources tell me that AMD GPUs don't need this, I tended to have issues without it.

## VM Details

| Detail | Setting |
|:------:|:--------|
| Chipset | Q35 |
| Emulator | `/usr/share/OVMF/OVMF_CODE_4M.ms.fd`
| CPU Topology | Manual (almost identical but leave some cores for Linux) |
| NIC | `NAT` and `e1000e` |
| PCI Host Device | Your GPU |
| PCI Host Device | GPUs Audio Device |
| PCI Host Device | Your Keyboard |
| PCI Host Device | Your Mouse |

## And edit the Overview XML, placing this line inside the hyperv tags
```xml
<hyperv mode="custom">
  <!--  Leave the Usual Stuff -->
  <vendor_id state="on" value="12345"/>
</hyperv>
```

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

## Other Ideas

My machine was originally a dual boot. (Windows 11 on NVMe Slot 1, Ubuntu on NVMe Slot 2)

Make sure GRUB is located on the Ubuntu one (where the host is located)

Then you can pass in the NVMe of Windows 11 (make sure theres no conflicting IOMMU Groups.

And just like that I have super speed performance, and I don't have to reboot everytime to get back to my usual Windows installation.

(This may need a few reboots of the VM to work, and make sure AI Suite is uninstalled)

## Credits

Shoutout to [QaidVoids Single GPU Passthrough Script](https://github.com/QaidVoid/Complete-Single-GPU-Passthrough) and the [VFIO Subreddit](https://reddit.com/r/VFIO) and the random users across MANY boards who have run into these issues in the past. ❤️
