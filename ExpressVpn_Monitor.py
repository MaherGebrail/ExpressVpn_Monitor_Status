#!/usr/bin/env python3
from common_functions import *


class ExpressStatus:
    def __init__(self):
        notify.init(APPINDICATOR_ID)

        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, error_image,
                                                    appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())

        # check existence of the app
        self.existence_checker()

        gtk.main()

    def existence_checker(self):
        """check first if the express-vpn app exist, And prepare the thread of checking the status of the app"""
        self.app_exist = cli_code()
        if not self.app_exist:
            self.test_app_existance = threading.Thread(target=self.check_existence)
            self.test_app_existance.daemon = True
            self.test_app_existance.start()

        self.test_connectivity = threading.Thread(target=self.check_status)
        self.test_connectivity.daemon = True
        if self.app_exist:
            self.test_connectivity.start()

    def do_func(self, _, func):

        if self.app_exist:
            self.thread_fun(func)

        else:
            notify.Notification.new(f"ExpressVpn Status", "It Seems that ExpressVpn-app doesn't Exist on the system",
                                    working_image).show()

    def thread_fun(self, func):
        """It starts a thread for the input-func"""
        do_chosen_fun = threading.Thread(target=eval(f"self.{func}"))
        do_chosen_fun.daemon = True
        do_chosen_fun.start()

    def check_existence(self):
        """this function runs if the app doesn't exist, so it keeps checking and breaks if the app got installed"""
        while True:
            self.app_exist = cli_code()
            if self.app_exist:
                self.test_connectivity.start()
                break
            time.sleep(15)

    def check_status(self):
        """This function checks the status of the connection of the app"""
        while True:
            s = app_output()
            img_exist = self.indicator.get_icon()

            if True not in s:
                if img_exist != error_image:
                    self.indicator.set_icon(error_image)
            elif img_exist != working_image:
                self.indicator.set_icon(working_image)

            time.sleep(3)

    @staticmethod
    def express_status():
        s = get_status()
        notify.Notification.new(f"ExpressVpn Status", s, working_image).show()

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
        status_btn.connect('activate', self.do_func, 'express_status')

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


if __name__ == "__main__":
    import gi

    gi.require_version("Gtk", "3.0")
    gi.require_version("AppIndicator3", "0.1")
    gi.require_version('Notify', '0.7')

    from gi.repository import Gtk as gtk
    from gi.repository import AppIndicator3 as appindicator
    from gi.repository import Notify as notify

    ExpressStatus()

