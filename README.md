# ExpressVpn_Monitor_Status

```The App creates Top-bar-icon to show the status of ExpressVpn connection .. has btns to connection status, connect, disconnect and another to quit the app.  ```

- As there is only browser extensions to see the vpn status or the command-line **For linux Users** .. which is painful to keep checking most of the time (if you are suspicious like me :grin:).

- Since i find the browser extensions not the best choice for me .. so i find the solution is to keep the status of the app in the try-bar.

> So HERE We are [I Tried it on **ubuntu** ] ..

* **install.sh** : This bash script do :

  * mkdir Vpn_Monitor in /opt/ **+** add [app.py **+** icons] into it.

  * copy service file into ~/.config/systemd/

  * copy sartup desktop file into ~/.config/startup/
* **ExpressVpn_Monitor.desktop** : run the app on startup.

* **startExpressVpn_Monitor.service** : added to be able to watch app's log from systemd.

* **ExpressVpn_Monitor.py** : The app Itself which is the only thing you need if you want to run it by yourself as script.

* **clean_install.sh** : It removes all the app's files from it's different places.

* <strong> *.png </strong> : app's icons.
