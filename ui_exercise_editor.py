# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exercise_editor.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFormLayout, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_ExerciseEditor(object):
    def setupUi(self, ExerciseEditor):
        if not ExerciseEditor.objectName():
            ExerciseEditor.setObjectName(u"ExerciseEditor")
        ExerciseEditor.resize(915, 782)
        self.verticalLayout = QVBoxLayout(ExerciseEditor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.detection_layout = QHBoxLayout()
        self.detection_layout.setObjectName(u"detection_layout")
        self.control_layout = QFormLayout()
        self.control_layout.setObjectName(u"control_layout")
        self.camera_label = QLabel(ExerciseEditor)
        self.camera_label.setObjectName(u"camera_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camera_label.sizePolicy().hasHeightForWidth())
        self.camera_label.setSizePolicy(sizePolicy)

        self.control_layout.setWidget(0, QFormLayout.LabelRole, self.camera_label)

        self.camera_combo_box = QComboBox(ExerciseEditor)
        self.camera_combo_box.setObjectName(u"camera_combo_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.camera_combo_box.sizePolicy().hasHeightForWidth())
        self.camera_combo_box.setSizePolicy(sizePolicy1)

        self.control_layout.setWidget(0, QFormLayout.FieldRole, self.camera_combo_box)

        self.preview_label = QLabel(ExerciseEditor)
        self.preview_label.setObjectName(u"preview_label")
        sizePolicy.setHeightForWidth(self.preview_label.sizePolicy().hasHeightForWidth())
        self.preview_label.setSizePolicy(sizePolicy)

        self.control_layout.setWidget(1, QFormLayout.LabelRole, self.preview_label)

        self.preview_check_box = QCheckBox(ExerciseEditor)
        self.preview_check_box.setObjectName(u"preview_check_box")

        self.control_layout.setWidget(1, QFormLayout.FieldRole, self.preview_check_box)

        self.timer_label = QLabel(ExerciseEditor)
        self.timer_label.setObjectName(u"timer_label")

        self.control_layout.setWidget(2, QFormLayout.LabelRole, self.timer_label)

        self.timer_spin_box = QSpinBox(ExerciseEditor)
        self.timer_spin_box.setObjectName(u"timer_spin_box")
        self.timer_spin_box.setMinimum(5)
        self.timer_spin_box.setMaximum(60)
        self.timer_spin_box.setValue(5)

        self.control_layout.setWidget(2, QFormLayout.FieldRole, self.timer_spin_box)


        self.detection_layout.addLayout(self.control_layout)

        self.detection_button = QPushButton(ExerciseEditor)
        self.detection_button.setObjectName(u"detection_button")
        self.detection_button.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.detection_button.sizePolicy().hasHeightForWidth())
        self.detection_button.setSizePolicy(sizePolicy2)

        self.detection_layout.addWidget(self.detection_button)


        self.verticalLayout.addLayout(self.detection_layout)

        self.detection_image = QLabel(ExerciseEditor)
        self.detection_image.setObjectName(u"detection_image")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.detection_image.sizePolicy().hasHeightForWidth())
        self.detection_image.setSizePolicy(sizePolicy3)
        self.detection_image.setScaledContents(False)
        self.detection_image.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.detection_image)

        self.pose_list_label = QLabel(ExerciseEditor)
        self.pose_list_label.setObjectName(u"pose_list_label")
        sizePolicy.setHeightForWidth(self.pose_list_label.sizePolicy().hasHeightForWidth())
        self.pose_list_label.setSizePolicy(sizePolicy)
        self.pose_list_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.pose_list_label)

        self.pose_list = QListWidget(ExerciseEditor)
        self.pose_list.setObjectName(u"pose_list")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pose_list.sizePolicy().hasHeightForWidth())
        self.pose_list.setSizePolicy(sizePolicy4)

        self.verticalLayout.addWidget(self.pose_list)

        self.dialog_button_layout = QHBoxLayout()
        self.dialog_button_layout.setObjectName(u"dialog_button_layout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.dialog_button_layout.addItem(self.horizontalSpacer)

        self.accept_button = QPushButton(ExerciseEditor)
        self.accept_button.setObjectName(u"accept_button")

        self.dialog_button_layout.addWidget(self.accept_button)

        self.cancel_button = QPushButton(ExerciseEditor)
        self.cancel_button.setObjectName(u"cancel_button")

        self.dialog_button_layout.addWidget(self.cancel_button)


        self.verticalLayout.addLayout(self.dialog_button_layout)


        self.retranslateUi(ExerciseEditor)

        QMetaObject.connectSlotsByName(ExerciseEditor)
    # setupUi

    def retranslateUi(self, ExerciseEditor):
        ExerciseEditor.setWindowTitle(QCoreApplication.translate("ExerciseEditor", u"\u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u0443\u043f\u0440\u0430\u0436\u043d\u0435\u043d\u0438\u044f", None))
        self.camera_label.setText(QCoreApplication.translate("ExerciseEditor", u"\u0412\u0435\u0431-\u043a\u0430\u043c\u0435\u0440\u0430:", None))
        self.preview_label.setText(QCoreApplication.translate("ExerciseEditor", u"\u041f\u0440\u0435\u0434\u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440:", None))
        self.timer_label.setText(QCoreApplication.translate("ExerciseEditor", u"\u0422\u0430\u0439\u043c\u0435\u0440:", None))
        self.timer_spin_box.setSuffix(QCoreApplication.translate("ExerciseEditor", u" \u0441\u0435\u043a\u0443\u043d\u0434", None))
        self.detection_button.setText(QCoreApplication.translate("ExerciseEditor", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.detection_image.setText("")
        self.pose_list_label.setText(QCoreApplication.translate("ExerciseEditor", u"\u041f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u0443\u043f\u0440\u0430\u0436\u043d\u0435\u043d\u0438\u044f", None))
        self.accept_button.setText(QCoreApplication.translate("ExerciseEditor", u"\u041e\u041a", None))
        self.cancel_button.setText(QCoreApplication.translate("ExerciseEditor", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi

