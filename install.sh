#!/usr/bin/env bash


# check if packages exists
cat > check_list.py <<EOL

import os
got = os.popen('apt list --installed').read()
for i in ["python3-gi", "gir1.2-appindicator3-0.1"]:
    if i not in got:
        print('install')
        break

EOL

pak=`python3 check_list.py`
rm check_list.py

if [[ $pak == "install" ]]; then
    sudo apt update && sudo apt install gir1.2-appindicator3-0.1 python3-gi -y
    #sudo apt-get install python3-gi
fi

# setting paths
user_name=`whoami`
service_file_name="startExpressVpn_Monitor.service"
app_path_name="/opt/Vpn_Monitor/"

# create the app folder
sudo mkdir /opt/Vpn_Monitor

# copying the needed files into app folder
sudo cp ExpressVpn_Monitor.py vpn_working.png wrong.png $app_path_name

# checking if the needed systemd dir exists
if [ ! -d "/home/$user_name/.config/systemd/user" ];then
    if [ ! -d "/home/$user_name/.config/systemd" ];then
        mkdir /home/$user_name/.config/systemd
        echo "Created ~/.config/systemd"
    fi

	mkdir /home/$user_name/.config/systemd/user
	echo "Created ~/.config/systemd/user dir"
fi


# copy the service into it's dir
cp $service_file_name /home/$user_name/.config/systemd/user/

# make the (app & service) files executable
sudo chmod +x $app_path_name/ExpressVpn_Monitor.py

chmod +x /home/$user_name/.config/systemd/user/$service_file_name


# refresh systemctl and run the service
systemctl --user daemon-reload
systemctl --user start $service_file_name


# add systemctl to start on startup apps from user ..> to avoid crashing before loading user gui
if [ ! -d "/home/$user_name/.config/autostart" ];then
        mkdir /home/$user_name/.config/autostart
        echo "Created ~/.config/autostart"
    fi
cp ExpressVpn_Monitor.desktop /home/$user_name/.config/autostart/


# check the service state
if [[ `systemctl --user is-active $service_file_name` == "active" ]]; then 
    echo "system `systemctl --user is-active $service_file_name` - Installation Completed .. Done .. BYE :)"; 
else echo "Installation Failed .... ";
fi
