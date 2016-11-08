#!/usr/bin/env python2
# -*- coding: utf8 -*-
import os
from shutil import copy

class PermissionsError(RuntimeError):
    pass

rpackages = [
              "apport",
              "resolvconf",
              "cups",
              "libreoffice-core",
              "ufw",
              "fcitx",
              "fcitx-bin",
              "friendly-recovery",
              "gdebi",
              "abiword",
              "gnumeric",
              "gnumeric-common",
              "im-config",
              "modemmanager",
              "printer-driver-pnm2ppa",
              "resolvconf",
              "sylpheed",
              "system-config-printer-common",
              "system-config-printer-gnome",
              "ubuntu-release-upgrader-core",
              "ubuntu-release-upgrader-gtk",
              "update-manager",
              "update-manager-core",
              "update-notifier",
              "update-notifier-common",
              "usb-creator-common",
              "usb-creator-gtk",
              "whoopsie",
              "fonts-noto-cjk"
            ]

ipackages = [
              "fabric",
              "curl",
              "vim",
              "htop",
              "git",
              "rake",
              "tmux",
              "strace",
              "lsof",
              "rsync",
              "nmap",
              "tcpdump"
            ]

def change_repo_mirror():
    src = os.path.join(os.getcwd(), 'sources.list')
    dst = '/etc/apt/sources.list'
    copy(dst, (dst + '.bak'))
    copy(src, dst)

def resolvconf_fix():
    if os.path.islink('/etc/resolv.conf'):
        os.remove('/etc/resolv.conf')
        os.system('apt-get -y remove resolvconf')
        os.system('systemctl disable resolvconf')
        os.system('systemctl stop resolvconf')
        os.system('echo "nameserver 192.168.1.1" >> /etc/resolv.conf')
        os.system('chattr +i /etc/resolv.conf')

def post_install():
    if os.getuid() == 0:
        change_repo_mirror()
        resolvconf_fix()
        os.environ['DEBIAN_FRONTEND'] = 'noninteractive'
        os.system('apt-get -y update')
        os.system('apt-get -y remove {}'.format(' '.join(rpackages)))
        os.system('apt-get -y autoremove')
        os.system('apt-get -y upgrade')
        os.system('apt-get -y install --no-install-recommends {}'.format(' '.join(ipackages)))
    else:
        raise PermissionsError('Must be root')

if __name__ == '__main__':
    post_install()
