# Pardus Power Manager
Simple power manager tools written python.

## Features
* performance & powersave profile switch
* automatic profile switch on ac/bat modes
* uses own service

## How to install from source
```shell
# install source
meson setup build --prefix=/usr
ninja -C build install
# enable systemd service (if available)
systemctl enable ppm
# reboot required
reboot
```
## Configuration
Configuration files store in **/etc/pardus/ppm.conf** file and **/etc/pardus/ppm.conf.d/** directory.

## Usage
You can use `ppm` command for changing profile or brightness
```
Usage: ppm [set/get] [mode/backlight] (value)
```
Also you can use indicator from system tray.

## License
Pardus Power Manager is distributed under the terms of the GNU General Public License,
version 3 or later. See the [LICENSE](LICENSE) file for details.
