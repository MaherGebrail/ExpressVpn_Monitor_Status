sudo rm -rf /opt/Vpn_Monitor/
user_name=`whoami`
rm /home/$user_name/.config/autostart/ExpressVpn_Monitor.desktop

systemctl --user stop startExpressVpn_Monitor.service

rm /home/$user_name/.config/systemd/user/startExpressVpn_Monitor.service
