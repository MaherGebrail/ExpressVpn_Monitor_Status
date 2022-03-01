#!/usr/bin/env bash

app_path_name="/opt/Vpn_Monitor"

check_install () {

    read -p "Proceed ? (Y/n) " response;

    if [[ "${response,}" == y* || -z $response ]];then
        sudo mkdir $app_path_name
    else
        echo "install.sh exited.";
        exit 0;
    fi

}

# getting the option of app version.
echo "write from [gi / qt] the version of app you want to install";
echo "Note: [gi] is the default choice ..".
read -p "[gi / qt] ? " install_option;


if [[ $install_option == "qt" ]]; then
    echo "installing QT version.."
    check_install
    running_script="ExpressVpn_pyqt.py"

    pip3 install -r requirements.txt

    cp vpn_working.png icon.ico
    sudo cp ExpressVpn_pyqt.py icon.ico $app_path_name

# case installing gi version
else
    echo "installing gi version"
    check_install
    running_script="ExpressVpn_Monitor.py"

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
    fi

# Ending (choosing option)
fi


# setting paths
user_name=`whoami`
service_file_name="startExpressVpn_Monitor.service"


# copying the needed files into app folder
sudo cp ExpressVpn_Monitor.py common_functions.py vpn_working.png wrong.png $app_path_name

# checking if the needed systemd dir exists
if [ ! -d "/home/$user_name/.config/systemd/user" ];then
    if [ ! -d "/home/$user_name/.config/systemd" ];then
        mkdir /home/$user_name/.config/systemd
        echo "Created ~/.config/systemd"
    fi

	mkdir /home/$user_name/.config/systemd/user
	echo "Created ~/.config/systemd/user dir"
fi

#create service file
cat > $service_file_name <<EOL
[Unit]
Description=ExpressVpn Monitoring

[Service]
Type=simple
ExecStart=$app_path_name/$running_script

[Install]
WantedBy=default.target
EOL

# binding the service to gnome-session if available
if [[ `systemctl --user is-active gnome-session-manager@ubuntu.service ` == "active" ]]; then
	sed -i "3 a ; NOTE : THIS LINE CAN BE IGNORED .. it's only usage to make sure that the service closes BEFORE being forced to fail when the pc is rebooting or shutting down and losing it's gui resources." $service_file_name
	sed -i "4 a BindsTo=gnome-session-manager@ubuntu.service\n " $service_file_name
fi

# copy service file
cp $service_file_name /home/$user_name/.config/systemd/user/

# make service file executable
chmod +x /home/$user_name/.config/systemd/user/$service_file_name


# add service to start on startup apps from user ..> to avoid crashing before loading user gui
if [ ! -d "/home/$user_name/.config/autostart" ];then
        mkdir /home/$user_name/.config/autostart
        echo "Created ~/.config/autostart"
    fi

chmod +x ExpressVpn_Monitor.desktop
cp -a ExpressVpn_Monitor.desktop /home/$user_name/.config/autostart/
sed -i "4d" ExpressVpn_Monitor.desktop
cp -a ExpressVpn_Monitor.desktop /home/$user_name/.local/share/applications/
sed -i "3 a X-GNOME-Autostart-enabled=true" ExpressVpn_Monitor.desktop

sudo chmod +x $app_path_name/*
sudo chown $user_name $app_path_name/*

# refresh systemctl and run the service
systemctl --user daemon-reload
systemctl --user start $service_file_name

# check the service state
if [[ `systemctl --user is-active $service_file_name` == "active" ]]; then
    echo "system `systemctl --user is-active $service_file_name` - Installation Completed .. Done .. BYE :)";
else echo "Installation Failed .... ";
fi
