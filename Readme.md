# Pardus Power Manager
Simple power manager tools written python.

## Features
* performance & powersave profile switch
* automatic profile switch on ac/bat modes
* uses own service

## How to install from source
```shell
# install source
make install
# enable systemd service (if available)
systemctl enable ppm
# reboot required
reboot
```
## Configuration
Configuration files store in **/etc/pardus/ppm.conf** file and **/etc/pardus/ppm.conf.d/** directory.

## Usage
You can use `ppm` command for changing profile or brightless
```
Usage: ppm [set/get] [mode/backlight] (value)
```
Also you can use indicator from system tray.