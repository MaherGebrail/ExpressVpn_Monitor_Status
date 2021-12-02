#!/usr/bin/env python3
import os
import time
import gi
import signal
import re

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


import threading

APPINDICATOR_ID = 'express'

used_path = os.path.abspath(os.path.dirname(__file__))
error_image = used_path + '/wrong.png'
working_image = used_path + '/vpn_working.png'


class ExpressStatus:
    def __init__(self):

        notify.init(APPINDICATOR_ID)

        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, error_image,
                                                    appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())

        # check if expressvpn app exist
        self.app_exist = os.system("expressvpn status") == 0
        if not self.app_exist:
            self.test_app_existance = threading.Thread(target=self.check_existence)
            self.test_app_existance.daemon = True
            self.test_app_existance.start()

        self.test_connectivity = threading.Thread(target=self.check_status)
        self.test_connectivity.daemon = True
        if self.app_exist:
            self.test_connectivity.start()
        
        # To Avoid KeyboardInterrupt Error (Not Very Important)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        
        gtk.main()

    def do_func(self, _, func):
    
        if self.app_exist:
            do_chosen_fun = threading.Thread(target=eval(f"self.{func}"))
            do_chosen_fun.daemon = True
            do_chosen_fun.start()

        else:
            notify.Notification.new(f"ExpressVpn Status", "It Seems that Ur system doesn't have ExpressVpn app", None).show()

    def check_existence(self):
        while True:
            self.app_exist = os.system("expressvpn status") == 0
            if self.app_exist:
                self.test_connectivity.start()
                break
            time.sleep(15)

    def check_status(self):
        while True:
            s = strip_ansi(os.popen("expressvpn status").readlines()[0])
            img_exist = self.indicator.get_icon()

            if "Connected" not in s[:11]:
                if img_exist != error_image:
                    self.indicator.set_icon(error_image)
            else:
                if img_exist != working_image:
                    self.indicator.set_icon(working_image)
            time.sleep(3)

    @staticmethod
    def express_status():
        s = strip_ansi(os.popen("expressvpn status").readlines()[0])
        notify.Notification.new(f"ExpressVpn Status", s, None).show()

    @staticmethod
    def connect_smart():
        os.system("expressvpn connect")

    @staticmethod
    def connect_stop():
        os.system("expressvpn disconnect")

    @staticmethod
    def quit(_):
        notify.uninit()
        gtk.main_quit()
        exit(0)

    def build_menu(self):
        menu = gtk.Menu()

        status_btn = gtk.MenuItem(label='Express status')
        status_btn.connect('activate', self.do_func,'express_status')

        connect_smart_btn = gtk.MenuItem(label='Express Connect')
        connect_smart_btn.connect('activate', self.do_func, 'connect_smart')

        connect_stop_btn = gtk.MenuItem(label='Express Disable')
        connect_stop_btn.connect('activate', self.do_func, "connect_stop")

        quit_btn = gtk.MenuItem(label='quit')
        quit_btn.connect('activate', self.quit)

        menu.append(status_btn)
        menu.append(connect_smart_btn)
        menu.append(connect_stop_btn)
        menu.append(quit_btn)
        menu.show_all()
        return menu


def strip_ansi(text):
    ansi_escape3 = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]', flags=re.IGNORECASE)
    text = ansi_escape3.sub('', text)
    return text 


if __name__ == "__main__":
    ExpressStatus()

