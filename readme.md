# new-ubuntu

This is just a repo to store some scripts and some handy guides that I had found/wrote for my specific system

## Packages

`installer.sh` Will run and install all the packages I ususally grab

`test-installer.sh` Is the exact same, but its just a dry run with echo instead of running the commands

## Single GPU Passthrough for QEMU/KVM

All of this is under the hooks directory. There is a readme within there.

I can verify as of 02/22/2023 that I got it working with 
 - Windows 10
 - Windows 11
 - MacOS Monterey
 - MacOS Ventura
   - Even xcode works on both!
