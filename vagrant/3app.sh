#! /bin/bash

###########################
#
#  RUNS NON PRIVILEGED - VAAGRANT USER
#
###########################
gnome_settings(){
#  gsettings get org.gnome.shell favorite-apps
   echo "[$(date +%H:%M:%S)]: Setting the userspace"
   gsettings set org.gnome.desktop.lockdown disable-lock-screen 'true'
   gsettings set org.gnome.shell favorite-apps "['org.gnome.Terminal.desktop', 'firefox.desktop', 'chromium_chromium.desktop', 'org.gnome.Nautilus.desktop', 'pycharm-community_pycharm-community.desktop', 'atom_atom.desktop','pgadmin3.desktop']"
}


get_repo(){
   mkdir ~/workspace && cd workspace
   git clone git@github.com:petermat/malbox-greenhouse.git 
}

main(){
    echo "[$(date +%H:%M:%S)]: XXX 3app.sh script started"
    gnome_settings    
    get_repo
    echo "[$(date +%H:%M:%S)]: XXX 3app.sh script finished"
}

main
exit 0
