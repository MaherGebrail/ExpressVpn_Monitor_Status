#!/usr/bin/env python3
from ExpressVpn_Monitor import *

from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from plyer import notification


icon_image = os.path.join(used_path, 'icon.ico')


class ExpressStatusQT(ExpressStatus):
    def __init__(self):
        # create the gui icon
        self.main()

        # check existence of the app
        self.existence_checker()

    def do_func(self, func):

        if self.app_exist:
            self.thread_fun(func)

        else:
            notification.notify(
                title="ExpressVpn Status",
                message="It Seems that ExpressVpn-app doesn't Exist on the system",
                app_icon=icon_image, timeout=2
            )

    def check_status(self):
        """This function checks the status of the connection of the app"""
        while True:
            s = app_output()

            if True not in s:
                if self.img_exist != error_image:
                    self.tray.setIcon(QIcon(error_image))
                    self.img_exist = error_image
            elif self.img_exist != working_image:
                self.tray.setIcon(QIcon(working_image))
                self.img_exist = working_image

            time.sleep(3)

    @staticmethod
    def express_status():
        s = get_status()

        notification.notify(
            title="ExpressVpn Status",
            message=s, app_icon=icon_image, timeout=2
        )

    def main(self):
        self.app = QApplication(sys.argv)

        self.img_exist = error_image
        self.icon = QIcon(self.img_exist)

        # setting TrayIcon
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        # Creating the options
        self.menu = QMenu()

        self.status_btn = QAction('Express status')
        self.status_btn.triggered.connect(lambda: self.do_func('express_status'))

        self.connect_btn = QAction('Express Connect')
        self.connect_btn.triggered.connect(lambda: self.do_func('connect_smart'))

        self.disable_btn = QAction('Express Disable')
        self.disable_btn.triggered.connect(lambda: self.do_func("connect_stop"))

        self.quit = QAction("Quit")
        self.quit.triggered.connect(self.app.quit)

        # add btns to Menu
        self.menu.addAction(self.status_btn)
        self.menu.addAction(self.connect_btn)
        self.menu.addAction(self.disable_btn)

        # To quit the app
        self.menu.addAction(self.quit)

        # add the menu to tray
        self.tray.setContextMenu(self.menu)

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    app = ExpressStatusQT()
    app.run()
