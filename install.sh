#!/usr/bin/env bash

app_path_name="/opt/Vpn_Monitor"

check_install () {

    read -p "Proceed ? (Y/n) " response;

    if [[ "${response,}" == y* || -z $response ]];then
        sudo mkdir $app_path_name
        sudo chown -R $USER $app_path_name
    else
        echo "install.sh exited.";
        exit 0;
    fi

}

# getting the option of app version.
echo "write from [gi / qt] the version of app you want to install";
echo "Note: [qt] is the default choice ..".
read -p "[gi / QT] ? " install_option;


if [[ $(python3 -c "import sys; print(sys.argv[1].strip().lower()[:2])" "$install_option") == "gi" ]]; then

# case installing gi version
    echo "installing gi version"
    check_install
    running_script="ExpressVpn_Monitor.py"
    EXEC_SCRIPT_PATH="$app_path_name/$running_script"

    # check if packages exists
    pak=$(python3 -c """import os; got = os.popen('apt list --installed 2>/dev/null').read(); print('install' if any([pkg not in got for pkg in ['python3-gi', 'gir1.2-appindicator3-0.1'] ]) else '');""")

    if [[ $pak == "install" ]]; then
        sudo apt update && sudo apt install gir1.2-appindicator3-0.1 python3-gi -y
    fi
else
    echo "installing QT version.."
    check_install
    running_script="ExpressVpn_pyqt.py"

    # create env
    python3 -m venv --system-site-packages $app_path_name/env
    source $app_path_name/env/bin/activate

    pip3 install -r requirements.txt
    EXEC_SCRIPT_PATH="$app_path_name/env/bin/python3 $app_path_name/$running_script"
    # end of env needed 
    
    cp vpn_working.png icon.ico
    sudo cp ExpressVpn_pyqt.py icon.ico $app_path_name

# Ending (choosing option)
fi


# setting paths
service_file_name="startExpressVpn_Monitor.service"


# copying the needed files into app folder
sudo cp ExpressVpn_Monitor.py common_functions.py vpn_working.png wrong.png $app_path_name

# checking if the needed systemd dir exists
if [ ! -d "/home/$USER/.config/systemd/user" ];then
    if [ ! -d "/home/$USER/.config/systemd" ];then
        mkdir /home/$USER/.config/systemd
        echo "Created ~/.config/systemd"
    fi

	mkdir /home/$USER/.config/systemd/user
	echo "Created ~/.config/systemd/user dir"
fi

#create service file
cat > $service_file_name <<EOL
[Unit]
Description=ExpressVpn Monitoring

[Service]
ExecStart=$EXEC_SCRIPT_PATH
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=default.target
EOL


# binding the service to graphical-session.target
if [[ `systemctl --user is-active graphical-session.target ` == "active" ]]; then
	sed -i "2 a BindsTo=graphical-session.target " $service_file_name
	sed -i "3 a After=graphical-session.target " $service_file_name
fi

# copy service file
cp $service_file_name /home/$USER/.config/systemd/user/

# add service to start on startup apps from user ..> to avoid crashing before loading user gui
if [ ! -d "/home/$USER/.config/autostart" ];then
        mkdir /home/$USER/.config/autostart
        echo "Created ~/.config/autostart"
    fi

cp  ExpressVpn_Monitor.desktop /home/$USER/.config/autostart/
sed -i "4d" ExpressVpn_Monitor.desktop
cp  ExpressVpn_Monitor.desktop /home/$USER/.local/share/applications/
sed -i "3 a X-GNOME-Autostart-enabled=true" ExpressVpn_Monitor.desktop

sudo chmod +x $app_path_name/*
sudo chown -R $USER $app_path_name

# refresh systemctl and run the service
systemctl --user daemon-reload
systemctl --user start $service_file_name

# sleep for 3 seconds to make sure that the script is reading the right status of the service.
sleep 3

# check the service state
if [[ `systemctl --user is-active $service_file_name` == "active" ]]; then
    echo "system `systemctl --user is-active $service_file_name` - Installation Completed .. Done .. BYE :)";
else echo "Installation Failed .... ";
fi
