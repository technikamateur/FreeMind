# FreeMind
## FreeMind is no longer under active development.

<img align="right" src="https://github.com/technikamateur/FreeMind/blob/master/logo/linux-server-128px.png" alt="logo FreeMind">

***

[![License](https://img.shields.io/badge/License-GPLv3-blue.svg?style=flat-square)](https://www.gnu.org/licenses/gpl.txt)
[![Stable](https://img.shields.io/badge/Master%20Version-none-green.svg?style=flat-square)](https://github.com/technikamateur/FreeMind/releases)
[![Stable](https://img.shields.io/badge/Slave%20Version-none-green.svg?style=flat-square)](https://github.com/technikamateur/FreeMind/releases)

Current Beta:

[![beta](https://img.shields.io/badge/Master%20Beta%20Version-none-yellow.svg?style=flat-square)](https://github.com/technikamateur/FreeMind/releases)
[![beta](https://img.shields.io/badge/Slave%20Beta%20Version-1.0-yellow.svg?style=flat-square)](https://github.com/technikamateur/FreeMind/releases)

#### Important information:
All releases, wich are marked with the *beta* tag are not stable! Use them only for testing purposes and if you absolutely know what you are doing!

The usage of FreeMind and all components is your own risk! Please understand that this software comes with NO WARRANTY! For more information see *LICENSE.txt*.

***

## TODO:
- Check todos in the project with `grep -R todo`...
- Some modularizing around the `actions` has to be done...

## About:
FreeMind is a simple webinterface, based on HTML and CSS and a powerful python3 backend. FreeMind makes it easy to manage your Samba-Fileserver, detect problems, create a backup, use snapshots, manage a recycle bin and some more pretty cool things wich safe a lot of time - actually your time. If you are interested in a detailed list of all features, see *Features*.

### Features:
- installs security patches in the background for you - never get worry about security
- shutdown and restart - you can shutdown your server without leaving your chair
- displays the status of your server e.g. HDD, free memory, utilization
- manages the backup of your data and makes it easy to restore - no more worries about lost data
- helps you to solve problems e.g. if a HDD crashes

## How to install:
1. Make sure that your drives are mounted in /etc/fstab (the drives you want to manage with FreeMind)
2. Get a copy of FreeMind. Go to ['releases'](https://github.com/technikamateur/FreeMind/releases) and download the latest version using

    `wget (link adress)`

3. Extract the archive and save the files to a directory of your choice.

    `tar xvf (name)`

4. Now run the setup.sh file. **Make sure you are still connected to the internet!** 

    `bash setup.sh`

   FreeMind will now setup itself and install all requiered dependencies.

## How to install the Web Interface
1. Run `pip install -e FreeMind` to install the Package
2. Run `export FLASK_APP=FreeMind`
3. And finally `flask run` - enjoy

### Config files wich will be replaced:
**the replaced config files can be found in /etc/freemind/old-conf**
- /etc/nginx/nginx.conf
- /etc/crontab
- /etc/samba/smb.conf

### Config files wich must be edited:
- **defhdd.conf** - insert all HDD's (you want to monitor) and a Description wich will be displayed at the admin panel
- **spacegrabber.sh** - insert all your HDD's (you want to monitor). Take a look at the comments!

### Dependencies:
**'setup.sh' will install them automatically**
- python3
- sqlite3
- curl
- htop
- rsync
- smartmontools
- nginx
- php-fpm
- php-sqlite3
- btrfs-tools
- and of course samba and samba-common

#### Dependencies to access webinterface:
- min. resolution: 1280 x 720 px (FullHD recommended)
- Firefox 52 or higher
- Chrome 49 or higher
- Internet Explorer 8 or higher (IE 11 recommended)
- Opera and Edge not tested

## License:
<img align="right" src="https://github.com/technikamateur/FreeMind/blob/master/logo/gplv3.png" alt="GPLv3">

This project is licensed under "GPLv3"! For more information see *LICENSE.txt*.

## Integrated projects & frameworks:
- [CSS Percentage Circle](http://circle.firchow.net/)
- [Bootstrap 3.3.7](https://github.com/twbs/bootstrap)
- [jQuery 3.1.1](https://github.com/jquery/jquery)
- [reflex grid 1.5](http://leejordan.github.io/reflex/docs/)
