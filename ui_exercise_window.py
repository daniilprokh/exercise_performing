# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exercise_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QHBoxLayout,
    QLabel, QListView, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QVBoxLayout,
    QWidget)

class Ui_ExerciseWindow(object):
    def setupUi(self, ExerciseWindow):
        if not ExerciseWindow.objectName():
            ExerciseWindow.setObjectName(u"ExerciseWindow")
        ExerciseWindow.resize(1150, 713)
        self.add_complex_action = QAction(ExerciseWindow)
        self.add_complex_action.setObjectName(u"add_complex_action")
        self.edit_complex_action = QAction(ExerciseWindow)
        self.edit_complex_action.setObjectName(u"edit_complex_action")
        self.edit_complex_action.setEnabled(False)
        self.choose_complex_action = QAction(ExerciseWindow)
        self.choose_complex_action.setObjectName(u"choose_complex_action")
        self.exit_action = QAction(ExerciseWindow)
        self.exit_action.setObjectName(u"exit_action")
        self.preview_action = QAction(ExerciseWindow)
        self.preview_action.setObjectName(u"preview_action")
        self.preview_action.setCheckable(True)
        self.close_complex_action = QAction(ExerciseWindow)
        self.close_complex_action.setObjectName(u"close_complex_action")
        self.close_complex_action.setEnabled(False)
        self.main_layout = QWidget(ExerciseWindow)
        self.main_layout.setObjectName(u"main_layout")
        self.horizontalLayout = QHBoxLayout(self.main_layout)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter = QSplitter(self.main_layout)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(4)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.exercise_Layout = QVBoxLayout(self.verticalLayoutWidget)
        self.exercise_Layout.setObjectName(u"exercise_Layout")
        self.exercise_Layout.setContentsMargins(0, 0, 0, 0)
        self.exercise_label = QLabel(self.verticalLayoutWidget)
        self.exercise_label.setObjectName(u"exercise_label")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.exercise_label.setFont(font)
        self.exercise_label.setAlignment(Qt.AlignCenter)

        self.exercise_Layout.addWidget(self.exercise_label)

        self.exercise_list_widget = QListWidget(self.verticalLayoutWidget)
        self.exercise_list_widget.setObjectName(u"exercise_list_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exercise_list_widget.sizePolicy().hasHeightForWidth())
        self.exercise_list_widget.setSizePolicy(sizePolicy)
        self.exercise_list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.exercise_list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.exercise_list_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.exercise_list_widget.setDragEnabled(True)
        self.exercise_list_widget.setDragDropMode(QAbstractItemView.InternalMove)
        self.exercise_list_widget.setResizeMode(QListView.Adjust)

        self.exercise_Layout.addWidget(self.exercise_list_widget)

        self.button_layout = QHBoxLayout()
        self.button_layout.setObjectName(u"button_layout")
        self.edit_rep_count_button = QPushButton(self.verticalLayoutWidget)
        self.edit_rep_count_button.setObjectName(u"edit_rep_count_button")
        self.edit_rep_count_button.setEnabled(False)
        font1 = QFont()
        font1.setPointSize(12)
        self.edit_rep_count_button.setFont(font1)

        self.button_layout.addWidget(self.edit_rep_count_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.button_layout.addItem(self.horizontalSpacer)

        self.exercise_button = QPushButton(self.verticalLayoutWidget)
        self.exercise_button.setObjectName(u"exercise_button")
        self.exercise_button.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.exercise_button.sizePolicy().hasHeightForWidth())
        self.exercise_button.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.exercise_button.setFont(font2)

        self.button_layout.addWidget(self.exercise_button)


        self.exercise_Layout.addLayout(self.button_layout)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.exercise_image = QLabel(self.splitter)
        self.exercise_image.setObjectName(u"exercise_image")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.exercise_image.sizePolicy().hasHeightForWidth())
        self.exercise_image.setSizePolicy(sizePolicy2)
        self.exercise_image.setMinimumSize(QSize(500, 0))
        self.exercise_image.setAlignment(Qt.AlignCenter)
        self.splitter.addWidget(self.exercise_image)

        self.horizontalLayout.addWidget(self.splitter)

        ExerciseWindow.setCentralWidget(self.main_layout)
        self.menubar = QMenuBar(ExerciseWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1150, 37))
        self.complex_menu = QMenu(self.menubar)
        self.complex_menu.setObjectName(u"complex_menu")
        self.camera_menu = QMenu(self.menubar)
        self.camera_menu.setObjectName(u"camera_menu")
        ExerciseWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.complex_menu.menuAction())
        self.menubar.addAction(self.camera_menu.menuAction())
        self.complex_menu.addAction(self.add_complex_action)
        self.complex_menu.addAction(self.edit_complex_action)
        self.complex_menu.addAction(self.choose_complex_action)
        self.complex_menu.addAction(self.close_complex_action)
        self.complex_menu.addSeparator()
        self.complex_menu.addAction(self.exit_action)
        self.camera_menu.addAction(self.preview_action)
        self.camera_menu.addSeparator()

        self.retranslateUi(ExerciseWindow)

        QMetaObject.connectSlotsByName(ExerciseWindow)
    # setupUi

    def retranslateUi(self, ExerciseWindow):
        ExerciseWindow.setWindowTitle(QCoreApplication.translate("ExerciseWindow", u"\u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0441\u0430 \u0443\u043f\u0440\u0430\u0436\u043d\u0435\u043d\u0438\u0439", None))
        self.add_complex_action.setText(QCoreApplication.translate("ExerciseWindow", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c...", None))
        self.edit_complex_action.setText(QCoreApplication.translate("ExerciseWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c...", None))
        self.choose_complex_action.setText(QCoreApplication.translate("ExerciseWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c...", None))
        self.exit_action.setText(QCoreApplication.translate("ExerciseWindow", u"\u0412\u044b\u0445\u043e\u0434", None))
        self.preview_action.setText(QCoreApplication.translate("ExerciseWindow", u"\u041f\u0440\u0435\u0434\u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440", None))
        self.close_complex_action.setText(QCoreApplication.translate("ExerciseWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
        self.exercise_label.setText(QCoreApplication.translate("ExerciseWindow", u"\u0423\u043f\u0440\u0430\u0436\u043d\u0435\u043d\u0438\u044f", None))
        self.edit_rep_count_button.setText(QCoreApplication.translate("ExerciseWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c \u043a\u043e\u043b-\u0432\u043e \u043f\u043e\u0432\u0442\u043e\u0440\u0435\u043d\u0438\u0439...", None))
        self.exercise_button.setText(QCoreApplication.translate("ExerciseWindow", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.exercise_image.setText("")
        self.complex_menu.setTitle(QCoreApplication.translate("ExerciseWindow", u"\u041a\u043e\u043c\u043f\u043b\u0435\u043a\u0441", None))
        self.camera_menu.setTitle(QCoreApplication.translate("ExerciseWindow", u"\u0412\u0435\u0431-\u043a\u0430\u043c\u0435\u0440\u0430", None))
    # retranslateUi

