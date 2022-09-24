# ExpressVpn_Monitor_Status

```The App creates Tray-bar-icon to show the status of ExpressVpn connection .. has btns to connection status, connect, disconnect and another to quit the app. ```

- As there is only browser extensions to see the vpn status or the command-line **For linux Users** … Which is painful to keep checking most of the time (if you are suspicious like me :grin:).

- Since I find the browser extensions not the best choice for me. So I find the solution is to keep the status of the app in the tray-bar.

> So HERE We are [I Tried it on **ubuntu** ] ..

* **install.sh** : This bash script do :

  * mkdir Vpn_Monitor in /opt/ **+** add [app.py **+** icons] into it.

  * copy service file into ~/.config/systemd/user/

  * copy desktop file to:
    * ~/.config/autostart/ **_to start the service with pc_**.
    * ~/.local/share/applications/ **_to let user able to run it from applications if it is not running_**.


* **ExpressVpn_Monitor.desktop** : Run the app on startup & from applications.

* **startExpressVpn_Monitor.service** : install.sh creates it in process.

* **ExpressVpn_Monitor.py** : The app itself, if you want to run it by yourself as script.

* **common_functions.py**: script that collects many functions and libs that the app needs to work.

* **clean_install.sh** : It removes all the installed app's files from their different places.

* <strong> *.png </strong> : app's icons.

<hr>

> QT version Of The App

``` Since Qt has more support and can work with distributions other than ubuntu, I have added [ ExpressVpn_pyqt.py, requirements.txt, icon.ico ]. ```

```install.sh now gives you the choice while running to choose between [gi/QT] versions ```

* **ExpressVpn_pyqt.py** : it imports funcs from **ExpressVpn_Monitor.py**, So to work properly the 2 files **+** **common_functions.py** must be placed together.

* **requirements.txt** : it's only needed for **ExpressVpn_pyqt.py** script.

* **icon.ico**: same image as **'vpn_working.png'**, which is why it's generated while installing [qt]-app version ... it's different name purpose is to avoid error with **plyer - notification** lib.

<hr>

```If you want to enable the service without startup.desktop FILE .. you may uncomment check_display_availability function inside common_functions.py file - To avoid errors in systemd .. although you don't have to.```
