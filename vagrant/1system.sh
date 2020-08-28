setup_dns(){
   echo -e "    eth1:\n      nameservers:\n        addresses: [8.8.8.8, 1.1.1.1]" | tee -a /etc/netplan/01-netcfg.yaml
   netplan --debug apply
}

set_locales(){
  export LANGUAGE=en_US.UTF-8
  export LANG=en_US.UTF-8
  export LC_ALL=en_US.UTF-8
  locale-gen en_US.UTF-8
  dpkg-reconfigure --frontend noninteractive locales
  export DEBIAN_FRONTEND=noninteractive
  timedatectl set-timezone Europe/Amsterdam
  echo "[$(date +%H:%M:%S)]: Adding apt repositories..."
  }

install_desktop(){
  # Install prerequisites and useful tools
  echo "[$(date +%H:%M:%S)]: Running apt-get clean..."
  apt-get clean
  echo "[$(date +%H:%M:%S)]: Running apt-get update & upgrade..."
  apt-get -qq update
  apt-get -qq upgrade -y 2>/dev/null 
  echo "[$(date +%H:%M:%S)]: Apt install core packages"
  apt-get install -y -qq software-properties-common build-essential  < /dev/null > /dev/null
  echo "[$(date +%H:%M:%S)]: Install Ubuntu desktop..."
  
  apt-get -y -qq install tasksel
  apt-get -y -qq install ubuntu-desktop
  #startx --:7:
  #echo "[$(date +%H:%M:%S)]: Mounting vagrant dir"
  #mount -t vboxsf -o uid=`id -u vagrant`,gid=`id -g vagrant` vagrant /vagrant

}

install_virtualboxtools(){
  add-apt-repository multiverse
  apt-get -y -qq install virtualbox-guest-dkms virtualbox-guest-x11
}

install_packages(){
  apt-get -y -qq install python-software-properties
  #curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash –
  apt-get -y -qq install nodejs
  apt-get -y -qq install npm
  apt-get -y -qq python3-virtualenv
}


install_devapps(){
    snap install sublime-text --classic
    snap install chromium 
    snap install pycharm-community --classic
    snap install --classic atom
}

install_docker(){
  apt-get  install -qq -y docker.io
  usermod -aG docker vagrant
  #usermod -a -G docker www-data 
  systemctl enable docker
  systemctl start docker
}


install_vagrant(){
  apt-get install -y virtualbox
  apt-get install -y virtualbox-guest-additions-iso
  apt-get install -y vagrant
}

main(){
  setup_dns
  set_locales
  install_desktop
  install_packages
  #install_virtualboxtools
  install_devapps
  #install_docker
  install_vagrant
  echo "[$(date +%H:%M:%S)]: XXX 1system.sh script finished"
}

main
exit 0



