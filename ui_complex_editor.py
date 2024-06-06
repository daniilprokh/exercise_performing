# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'complex_editor.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QDialog, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QListView,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ComplexEditor(object):
    def setupUi(self, ComplexEditor):
        if not ComplexEditor.objectName():
            ComplexEditor.setObjectName(u"ComplexEditor")
        ComplexEditor.resize(799, 521)
        self.verticalLayout_2 = QVBoxLayout(ComplexEditor)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.complex_name_layout = QFormLayout()
        self.complex_name_layout.setObjectName(u"complex_name_layout")
        self.complex_name_label = QLabel(ComplexEditor)
        self.complex_name_label.setObjectName(u"complex_name_label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        self.complex_name_label.setFont(font)

        self.complex_name_layout.setWidget(0, QFormLayout.LabelRole, self.complex_name_label)

        self.complex_name_edit = QLineEdit(ComplexEditor)
        self.complex_name_edit.setObjectName(u"complex_name_edit")
        font1 = QFont()
        font1.setPointSize(12)
        self.complex_name_edit.setFont(font1)

        self.complex_name_layout.setWidget(0, QFormLayout.FieldRole, self.complex_name_edit)


        self.verticalLayout_2.addLayout(self.complex_name_layout)

        self.label = QLabel(ComplexEditor)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.label.setFont(font2)

        self.verticalLayout_2.addWidget(self.label)

        self.exrercise_layout = QHBoxLayout()
        self.exrercise_layout.setObjectName(u"exrercise_layout")
        self.exercise_list_widget = QListWidget(ComplexEditor)
        self.exercise_list_widget.setObjectName(u"exercise_list_widget")
        self.exercise_list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.exercise_list_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.exercise_list_widget.setResizeMode(QListView.Adjust)

        self.exrercise_layout.addWidget(self.exercise_list_widget)

        self.exercise_control_layout = QVBoxLayout()
        self.exercise_control_layout.setObjectName(u"exercise_control_layout")
        self.add_button = QPushButton(ComplexEditor)
        self.add_button.setObjectName(u"add_button")

        self.exercise_control_layout.addWidget(self.add_button)

        self.edit_button = QPushButton(ComplexEditor)
        self.edit_button.setObjectName(u"edit_button")
        self.edit_button.setEnabled(False)

        self.exercise_control_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton(ComplexEditor)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setEnabled(False)

        self.exercise_control_layout.addWidget(self.delete_button)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.exercise_control_layout.addItem(self.vertical_spacer)


        self.exrercise_layout.addLayout(self.exercise_control_layout)


        self.verticalLayout_2.addLayout(self.exrercise_layout)

        self.control_button_layout = QHBoxLayout()
        self.control_button_layout.setObjectName(u"control_button_layout")
        self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.control_button_layout.addItem(self.horizontal_spacer)

        self.save_button = QPushButton(ComplexEditor)
        self.save_button.setObjectName(u"save_button")

        self.control_button_layout.addWidget(self.save_button)

        self.save_as_button = QPushButton(ComplexEditor)
        self.save_as_button.setObjectName(u"save_as_button")

        self.control_button_layout.addWidget(self.save_as_button)

        self.cancel_button = QPushButton(ComplexEditor)
        self.cancel_button.setObjectName(u"cancel_button")

        self.control_button_layout.addWidget(self.cancel_button)


        self.verticalLayout_2.addLayout(self.control_button_layout)


        self.retranslateUi(ComplexEditor)

        QMetaObject.connectSlotsByName(ComplexEditor)
    # setupUi

    def retranslateUi(self, ComplexEditor):
        ComplexEditor.setWindowTitle(QCoreApplication.translate("ComplexEditor", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0441\u0430 \u0443\u043f\u0440\u0430\u0436\u043d\u0435\u043d\u0438\u0439", None))
        self.complex_name_label.setText(QCoreApplication.translate("ComplexEditor", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435:", None))
        self.label.setText(QCoreApplication.translate("ComplexEditor", u"\u0423\u043f\u0440\u0430\u0436\u043d\u0435\u043d\u0438\u044f", None))
        self.add_button.setText(QCoreApplication.translate("ComplexEditor", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c...", None))
        self.edit_button.setText(QCoreApplication.translate("ComplexEditor", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c...", None))
        self.delete_button.setText(QCoreApplication.translate("ComplexEditor", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.save_button.setText(QCoreApplication.translate("ComplexEditor", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.save_as_button.setText(QCoreApplication.translate("ComplexEditor", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043a\u0430\u043a..", None))
        self.cancel_button.setText(QCoreApplication.translate("ComplexEditor", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi

