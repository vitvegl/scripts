import os
import shutil
import subprocess
from fabric.api import local
from systemctl import __systemctl__
from systemctl import __daemon__reload__

BASHRC = os.path.join(os.environ['HOME'], '.bashrc')
PYENV_HOME = os.path.join(os.environ['HOME'], '.pyenv')
VIMRC = os.path.join(os.environ['HOME'], '.vimrc')

def vimrc_copy():
    ''' copying minimal vim config '''
    if not os.path.exists(VIMRC):
        shutil.copy('vimrc', VIMRC)

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
              "synaptic",
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
              "whoopsie"
            ]

ipackages = [
              "fabric",
              "curl",
              "htop",
              "vim",
              "git",
              "rake",
              "tmux",
              "rsync",
              "squashfs-tools",
              "lsof",
              "strace",
              "nmap",
              "tcpdump"
            ]

def change_repo_mirror():
    ''' mirror over https: "https://ftp.lysator.liu.se"
    '''
    src = os.path.join(os.getcwd(), 'sources.list')
    dst = os.path.realpath('/etc/apt/sources.list')
    shutil.copy(dst, (dst + '.bak'))
    shutil.copy(src, dst)

def resolvconf_fix():
    ''' resolvconf fix
    '''
    if os.path.islink('/etc/resolv.conf'):
        os.remove(rconf)
        local('systemctl disable resolvconf')
        local('systemctl stop resolvconf')
        local('systemctl mask resolvconf')
        local('echo "nameserver 192.168.1.1" > /etc/resolv.conf')
        local('chattr +i /etc/resolv.conf')

def configure_iptables():
    ''' configure iptables (Ubuntu-specific)
    '''
    iptrulesdir = os.path.realpath('/etc/iptables')
    iptunitdir = os.path.realpath('/lib/systemd/system')
    if os.getuid() == 0:
        if not os.path.isdir(iptrulesdir):
            os.mkdir(iptrulesdir, 0700)
        shutil.copy('iptables.rules', iptrulesdir)
        if not os.path.isfile(os.path.join(iptunitdir, 'iptables.service')):
            shutil.copy('iptables.service', iptunitdir)
            local('systemctl daemon-reload')
            local('systemctl enable iptables')
            local('systemctl start iptables')
    else:
        raise RuntimeError("Must be root only")

def post_install():
    ''' Update, upgrade, remove trash from system and install
        required packages '''
    if os.getuid() == 0:
        resolvconf_fix()
        change_repo_mirror()
        configure_iptables()
        local('apt-get -y update')
        local('apt-get -y upgrade')
        local('apt-get -y remove {}'.format(' '.join(rpackages)))
        local('apt-get -y autoremove')
        local('apt-get -y install --no-install-recommends {}'.format(' '.join(ipackages)))
    else:
        raise RuntimeError("Must be root")
    print('\x1b[6;30;42m' + 'Everything is ok !' + '\x1b[0m')

def install_pyenv():
    ''' pyenv easy install into $HOME '''
    if not os.path.isdir(PYENV_HOME):
        local('git clone https://github.com/yyuu/pyenv.git ~/.pyenv')
        line1 = 'export PYENV_ROOT="$HOME/.pyenv"'
        line2 = 'export PATH="$PYENV_ROOT/bin:$PATH"'
        line3 = 'eval "$(pyenv init -)"'
        f = open(BASHRC, 'a')
        f.write('{}\n{}\n{}\n'.format(line1, line2, line3))
        f.close()
        subprocess.call(['exec $SHELL'], shell = True)
