## Tools Needed

Run `apt install qemu-kvm qemu-utils libvirt-daemon-system libvirt-clients bridge-utils virt-manager ovmf`

Reboot

Run `virsh net-start default`

Run `virsh net-autostart default`

## Preping GRUB

Add `amd_iommu=on iommu=pt iommu=1 video=efifb:off` on the end of `GRUB_CMDLINE_LINUX_DEFAULT` inside of `/etc/default/grub`

Run `sudo grub-mkconfig -o /boot/grub/grub.cfg` to apply.

Reboot.

## File Placement
The hooks folder files would reside inside of `/etc/libvirt/`

and the GPU BIOS (in my case an MSI RX 6600 XT) would reside in `/usr/share/vgabios`

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
