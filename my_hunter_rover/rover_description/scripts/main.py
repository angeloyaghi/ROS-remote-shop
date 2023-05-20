#! /usr/bin/env python

import rospy
import sys
import platform
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import *
from rover_description.srv import GetItems, GetItemsRequest, GetItemsResponse

# Main Window
# from file_name.py import Ui_name of the QMainWindow in the designer
from uis.ui_robotics_shopping_list import Ui_MainWindow

# Splash Screen
# from file_name.py import Ui_name of the QMainWindow in the designer
from uis.ui_splashscreen import Ui_SplashScreen

# global variables
counter = 0


# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(630, 530)

        self.ui.imagebottle.setPixmap(QPixmap(u"/home/lea/catkin_ws/src/my_hunter_rover/rover_description/scripts/list_items/bottle_green.png"))
        self.ui.imagebottle.setScaledContents(True)
        self.ui.imageclock.setPixmap(QPixmap(u"/home/lea/catkin_ws/src/my_hunter_rover/rover_description/scripts/list_items/clock.jpg"))
        self.ui.imageclock.setScaledContents(True)
        self.ui.imagecup.setPixmap(QPixmap(u"/home/lea/catkin_ws/src/my_hunter_rover/rover_description/scripts/list_items/cup.png"))
        self.ui.imagecup.setScaledContents(True)
        self.ui.imagefruits.setPixmap(QPixmap(u"/home/lea/catkin_ws/src/my_hunter_rover/rover_description/scripts/list_items/fruits.jpg"))
        self.ui.imagefruits.setScaledContents(True)

        self.ui.pushButton.clicked.connect(self.calculate)
        self.ui.checkoutbutton.clicked.connect(self.checkout)


    def checkout(self):
        bottle_quantity = self.ui.quantitybottle.value()
        cup_quantity = self.ui.quantitycup.value()
        apple_quantity = self.ui.quantityapple.value()
        banana_quantity = self.ui.quantitybanana.value()
        clock_quantity = self.ui.quantityclock.value()
        rospy.wait_for_service('get_items')
        items = [bottle_quantity, cup_quantity, clock_quantity, apple_quantity, banana_quantity]
        try:
            get_items = rospy.ServiceProxy('get_items', GetItems)
            request = GetItemsRequest(items)
            response = get_items(request)
            print("Success: ", response.success)
            print("Getting your items.")
        except rospy.ServiceException as e:
            print("Service call failed", e)

        sys.exit(app.exec_())

    def calculate(self):
        bottleprice = self.ui.quantitybottle.value() * 0.25
        cupprice = self.ui.quantitycup.value() * 2
        appleprice = self.ui.quantityapple.value() * 0.1
        bananaprice = self.ui.quantitybanana.value() * 0.1
        clockprice = self.ui.quantityclock.value() * 7

        totalprice = bottleprice + cupprice + appleprice + bananaprice + clockprice
        self.ui.totallcd.display(totalprice)

# Splash Screen
class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # UI --> INTERFACE CODES

        # Remove title bar and window border
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Drop shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(250, 250, 250, 255))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        # start Qt timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # timer in milliseconds
        self.timer.start(30)

        # change the description text in the splash screen
        QtCore.QTimer.singleShot(1200, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QtCore.QTimer.singleShot(2400, lambda: self.ui.label_description.setText("<strong>GENERATING</strong> USER INTERFACE"))

        # Show Main Window
        self.show()

        # END

    # ADD FUNCTIONS

    def progress(self):
        global counter
        # set value to progress bar
        self.ui.progressBar.setValue(counter)

        # increase counter
        counter += 1

        # close splash screen and open main window
        if counter > 100:
            # stop timer
            self.timer.stop()

            # show main window
            self.main = MainWindow()
            self.main.show()

            # close splash screen
            self.close()


if __name__ == "__main__":
    rospy.init_node('gui', anonymous=True)
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
