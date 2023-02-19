The hooks folder files would reside inside of `/etc/libvirt/`

and the GPU BIOS (in my case an MSI RX 6600 XT) would reside in `/usr/share/vgabios`

QEMU Should be setup with the following:
- Chipset: Q35
- UEFI: /usr/share/OVMF/OVMF_CODE_4M.ms.fd
- Manually setup CPU Topology
- NIC: not virtio
- USB Peripherals also passed in
- Edit the XML of the GPU like so
```xml
<hostdev mode="subsystem" type="pci" managed="yes">
  <source>
    <address domain="0x0000" bus="0x03" slot="0x00" function="0x0"/>
  </source>
  <rom file="/usr/share/vgabios/GPU.rom"/>
  <address type="pci" domain="0x0000" bus="0x05" slot="0x00" function="0x0"/>
</hostdev>
```


And of course `amd_iommu=on iommu=pt iommu=1 video=efifb:off` appended on the end of `/etc/default/grub`

`sudo grub-mkconfig -o /boot/grub/grub.cfg`
