# ExpressVpn_Monitor_Status

```The App creates Top-bar-icon to show the status of ExpressVpn connection .. has btns to connection status, connect, disconnect and another to quit the app.  ```

- As there is only browser extensions to see the vpn status or the command-line **For linux Users** … Which is painful to keep checking most of the time (if you are suspicious like me :grin:).

- Since I find the browser extensions not the best choice for me. So I find the solution is to keep the status of the app in the top-bar.

> So HERE We are [I Tried it on **ubuntu** ] ..

* **install.sh** : This bash script do :

  * mkdir Vpn_Monitor in /opt/ **+** add [app.py **+** icons] into it.

  * copy service file into ~/.config/systemd/user/

  * copy desktop file to:
    * ~/.config/autostart/ **_to start the service with pc_**.
    * ~/.local/share/applications/ **_to let user able to run it from applications if it is not running_**.


* **ExpressVpn_Monitor.desktop** : Run the app on startup & from applications.

* **startExpressVpn_Monitor.service** : install.sh creates it in process.

* **ExpressVpn_Monitor.py** : The app itself, which is the only thing you need if you want to run it by yourself as script.

* **clean_install.sh** : It removes all the app's files from its different places.

* <strong> *.png </strong> : app's icons.
