# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'drawboard.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(150, 70, 160, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(625, 10, 105, 21))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.horizontalLayout_2.setStretch(1,1)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(625, 60, 105, 21))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_4.addWidget(self.pushButton_2)
        self.horizontalLayout_4.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 509, 17))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menu_2)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menu_2)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(self.menu_2)
        self.menu_5.setObjectName("menu_5")
        self.menu_6 = QtWidgets.QMenu(self.menubar)
        self.menu_6.setObjectName("menu_6")
        self.menu_7 = QtWidgets.QMenu(self.menu_6)
        self.menu_7.setObjectName("menu_7")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.toolBar_2 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_2.setObjectName("toolBar_2")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_2)
        self.action1 = QtWidgets.QAction(MainWindow)
        self.action1.setObjectName("action1")
        self.action2 = QtWidgets.QAction(MainWindow)
        self.action2.setObjectName("action2")
        self.actionellipse = QtWidgets.QAction(MainWindow)
        self.actionellipse.setObjectName("actionellipse")
        self.action_DDA = QtWidgets.QAction(MainWindow)
        self.action_DDA.setObjectName("action_DDA")
        self.action_Bresenham = QtWidgets.QAction(MainWindow)
        self.action_Bresenham.setObjectName("action_Bresenham")
        self.action_DDA_2 = QtWidgets.QAction(MainWindow)
        self.action_DDA_2.setObjectName("action_DDA_2")
        self.action_Bresenham_2 = QtWidgets.QAction(MainWindow)
        self.action_Bresenham_2.setObjectName("action_Bresenham_2")
        self.action_Bezier = QtWidgets.QAction(MainWindow)
        self.action_Bezier.setObjectName("action_Bezier")
        self.action_B_spline = QtWidgets.QAction(MainWindow)
        self.action_B_spline.setObjectName("action_B_spline")
        self.action_redo = QtWidgets.QAction(MainWindow)
        self.action_redo.setObjectName("action_redo")
        self.action_move = QtWidgets.QAction(MainWindow)
        self.action_move.setObjectName("action_move")
        self.action_rotate = QtWidgets.QAction(MainWindow)
        self.action_rotate.setObjectName("action_rotate")
        self.action_scale = QtWidgets.QAction(MainWindow)
        self.action_scale.setObjectName("action_scale")
        self.action_line2 = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../ICON/line.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_line2.setIcon(icon)
        self.action_line2.setObjectName("action_line2")
        self.action_polygon2 = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../ICON/polygon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_polygon2.setIcon(icon1)
        self.action_polygon2.setObjectName("action_polygon2")
        self.action_ellipse2 = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../ICON/ellipse.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_ellipse2.setIcon(icon2)
        self.action_ellipse2.setObjectName("action_ellipse2")
        self.action_curve2 = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../ICON/curve.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_curve2.setIcon(icon3)
        font = QtGui.QFont()
        self.action_curve2.setFont(font)
        self.action_curve2.setObjectName("action_curve2")

        #self.action_text = QtWidgets.QAction(MainWindow)
        # icon3 = QtGui.QIcon()
        # icon3.addPixmap(QtGui.QPixmap("../ICON/curve.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        # self.action_curve2.setIcon(icon3)
        # font = QtGui.QFont()
        # self.action_curve.setFont(font)
        #self.action_text.setObjectName("action_text")

        self.action_move2 = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../ICON/move.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_move2.setIcon(icon4)
        self.action_move2.setObjectName("action_move2")
        self.action_rotate2 = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../ICON/rotate.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_rotate2.setIcon(icon5)
        self.action_rotate2.setObjectName("action_rotate2")
        self.action_scale2 = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../ICON/scale.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_scale2.setIcon(icon6)
        self.action_scale2.setObjectName("action_scale2")
        self.action_clip2 = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../ICON/clip.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_clip2.setIcon(icon7)
        self.action_clip2.setObjectName("action_clip2")
        self.action_pen = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("../ICON/pen.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_pen.setIcon(icon8)
        self.action_pen.setObjectName("action_pen")
        self.action_click = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("../ICON/click.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_click.setIcon(icon9)
        self.action_click.setObjectName("action_click")
        self.action_fill = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("../ICON/bucket.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_fill.setIcon(icon10)
        self.action_fill.setObjectName("action_fill")
        self.action_down = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("../ICON/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_down.setIcon(icon11)
        self.action_down.setObjectName("action_down")

        self.actioncohen_sutherland = QtWidgets.QAction(MainWindow)
        self.actioncohen_sutherland.setObjectName("actioncohen_sutherland")
        self.actionliang_barsky_action = QtWidgets.QAction(MainWindow)
        self.actionliang_barsky_action.setObjectName("actionliang_barsky_action")
        self.menu.addAction(self.action1)
        self.menu.addAction(self.action2)
        self.menu_3.addAction(self.action_DDA)
        self.menu_3.addAction(self.action_Bresenham)
        self.menu_4.addSeparator()
        self.menu_4.addAction(self.action_DDA_2)
        self.menu_4.addAction(self.action_Bresenham_2)
        self.menu_5.addAction(self.action_Bezier)
        self.menu_5.addAction(self.action_B_spline)
        self.menu_2.addAction(self.menu_3.menuAction())
        self.menu_2.addAction(self.menu_4.menuAction())
        self.menu_2.addAction(self.actionellipse)
        self.menu_2.addAction(self.menu_5.menuAction())
        self.menu_7.addAction(self.actioncohen_sutherland)
        self.menu_7.addAction(self.actionliang_barsky_action)
        self.menu_6.addAction(self.action_redo)
        self.menu_6.addAction(self.action_move)
        self.menu_6.addAction(self.action_rotate)
        self.menu_6.addAction(self.action_scale)
        self.menu_6.addAction(self.menu_7.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_6.menuAction())
        self.toolBar.addAction(self.action_click)
        self.toolBar.addAction(self.action_line2)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_polygon2)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_ellipse2)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_curve2)
        self.toolBar.addSeparator()
        #self.toolBar.addAction(self.action_text)
        self.toolBar_2.addAction(self.action_move2)
        self.toolBar_2.addAction(self.action_rotate2)
        self.toolBar_2.addAction(self.action_scale2)
        self.toolBar_2.addAction(self.action_clip2)
        self.toolBar_2.addAction(self.action_pen)
        self.toolBar_2.addAction(self.action_fill)
        self.toolBar_2.addAction(self.action_down)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "画笔"))
        #self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.label_2.setText(_translate("MainWindow", "填充"))
        #self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "绘制"))
        self.menu_3.setTitle(_translate("MainWindow", "直线"))
        self.menu_4.setTitle(_translate("MainWindow", "多边形"))
        self.menu_5.setTitle(_translate("MainWindow", "曲线"))
        self.menu_6.setTitle(_translate("MainWindow", "编辑"))
        self.menu_7.setTitle(_translate("MainWindow", "裁剪"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.toolBar_2.setWindowTitle(_translate("MainWindow", "toolBar_2"))
        self.action1.setText(_translate("MainWindow", "新建"))
        self.action2.setText(_translate("MainWindow", "保存"))
        self.action1.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.action2.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionellipse.setText(_translate("MainWindow", "椭圆"))
        self.action_DDA.setText(_translate("MainWindow", "DDA"))
        self.action_Bresenham.setText(_translate("MainWindow", "Bresenham"))
        self.action_DDA_2.setText(_translate("MainWindow", "DDA"))
        self.action_Bresenham_2.setText(_translate("MainWindow", "Bresenham"))
        self.action_Bezier.setText(_translate("MainWindow", "Bezier"))
        self.action_B_spline.setText(_translate("MainWindow", "B_spline"))
        self.action_redo.setText(_translate("MainWindow", "撤销"))
        self.action_move.setText(_translate("MainWindow", "平移"))
        self.action_rotate.setText(_translate("MainWindow", "旋转"))
        self.action_scale.setText(_translate("MainWindow", "缩放"))
        self.action_line2.setText(_translate("MainWindow", "line2"))
        self.action_line2.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.action_polygon2.setText(_translate("MainWindow", "polygon2"))
        self.action_polygon2.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.action_ellipse2.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.action_curve2.setText(_translate("MainWindow", "curve2"))
        self.action_curve2.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.action_move2.setText(_translate("MainWindow", "move2"))
        self.action_move2.setShortcut(_translate("MainWindow", "Ctrl+M"))
        self.action_rotate2.setText(_translate("MainWindow", "rotate2"))
        self.action_rotate2.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.action_scale2.setText(_translate("MainWindow", "scale"))
        self.action_scale2.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.action_clip2.setText(_translate("MainWindow", "clip2"))
        self.action_clip2.setShortcut(_translate("MainWindow", "Ctrl+B"))
        self.action_pen.setText(_translate("MainWindow", "pen"))
        self.action_fill.setText(_translate("MainWindow", "fill"))
        self.action_click.setText(_translate("MainWindow", "click"))
        self.actioncohen_sutherland.setText(_translate("MainWindow", "cohen_sutherland"))
        self.actionliang_barsky_action.setText(_translate("MainWindow", "liang_barsky_action"))
