
from pose_utils import Landmarks

from typing import Optional, List

from PySide6.QtWidgets import (QWidget, QDialog, QLabel, QLineEdit, QSpinBox,
    QVBoxLayout, QHBoxLayout, QFormLayout, QLayout, QTextEdit,
    QPushButton, QSpacerItem, QSizePolicy, QMessageBox)
from PySide6.QtCore import Slot

class ExerciseInfo():
    def __init__(self, 
                 description: str,
                 repetition_count: int,
                 poses: List[Landmarks]):
        self.description = description
        self.repetition_count = repetition_count
        self.poses =  poses

class ExerciseInfoEdit(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        __main_layout = QFormLayout(self)
        self.__exercise_name_edit = QLineEdit(self)
        __main_layout.addRow(u'Наименование:', self.__exercise_name_edit)
        self.__exercise_description_edit = QTextEdit(self)
        __main_layout.addRow(u'Описание:', self.__exercise_description_edit)
        self.__exercise_pose_count_edit = QLineEdit(self)
        self.__exercise_pose_count_edit.setReadOnly(True)
        __main_layout.addRow(u'Количество положений:',
                             self.__exercise_pose_count_edit)
        self.__exercise_repetition_spin_box = QSpinBox(self)
        self.__exercise_repetition_spin_box.setRange(1, 100)
        self.__exercise_repetition_spin_box.setValue(10)
        __main_layout.addRow(u'Количество повторений:',
                             self.__exercise_repetition_spin_box)

    def get_exercise_name(self) -> str:
        return self.__exercise_name_edit.text()
    
    def get_exercise_description(self) -> str:
        return self.__exercise_description_edit.toPlainText()
    
    def get_exercise_pose_count(self) -> int:
        return int(self.__exercise_pose_count_edit.text())
    
    def get_exercise_repetition_count(self) -> int:
        return self.__exercise_repetition_spin_box.value()

    def set_exercise_name(self, exercise_name: str) -> None:
        self.__exercise_name_edit.setText(exercise_name)

    def set_exercise_description(self, exercise_description: str) -> None:
        self.__exercise_description_edit.setText(exercise_description)
    
    def set_exercise_pose_count(self, exercise_pose_count: int) -> None:
        if exercise_pose_count < 2:
            return
        self.__exercise_pose_count_edit.setText(str(exercise_pose_count))
    
    def set_exercise_repetition_count(self, exercise_repetition_count: int) -> None:
        if exercise_repetition_count < 1:
            return
        self.__exercise_repetition_spin_box.setValue(exercise_repetition_count)

class ExerciseInfoDialog(QDialog):
    def __init__(self,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle(
            u'Изменение информации об упражнении')

        main_layout = QVBoxLayout(self)
        self.__exercise_info_edit = ExerciseInfoEdit(self)
        main_layout.addWidget(self.__exercise_info_edit)

        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(
            40,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum))
        ok_button = QPushButton(u'ОК', self)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        cancel_button = QPushButton(u'Отмена', self)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)

    def get_exercise_info_edit(self) -> ExerciseInfoEdit:
        return self.__exercise_info_edit

    @Slot()
    def accept(self) -> None:
        if not self.__exercise_info_edit.get_exercise_name():
            QMessageBox.warning(
                self,
                u'Предупреждение',
                u'Не указано наименование упражнения!')
            return
        return super().accept()
       

class ExerciseRepetitionDialog(QDialog):
    def __init__(self,
                 exercise_name: str,
                 repetition_count: int,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        
        self.setWindowTitle(
            u'Изменение количества повторений упражнения - {}'.format(
                exercise_name))

        main_layout = QVBoxLayout(self)

        rep_layout = QFormLayout()
        self.__exercise_repetition_spin_box = QSpinBox(self)
        self.__exercise_repetition_spin_box.setRange(1, 100)
        self.__exercise_repetition_spin_box.setValue(repetition_count)
        rep_layout.addRow(u'Количество повторений:',
                             self.__exercise_repetition_spin_box)
        main_layout.addLayout(rep_layout)
        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(
            40,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum))
        ok_button = QPushButton(u'ОК', self)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        cancel_button = QPushButton(u'Отмена', self)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)
        
    def get_exercise_repetition_count(self) -> int:
        return self.__exercise_repetition_spin_box.value()

class ExerciseInfoLabel(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        self.__exercise_name_label = QLabel(self)
        font = self.font()
        font.setPointSize(12)
        font.setBold(True)
        self.__exercise_name_label.setFont(font)
        main_layout.addWidget(self.__exercise_name_label)
        sub_layout = QFormLayout()
        self.__exercise_pose_count_label = QLabel(self)
        sub_layout.addRow(u'Количество положений:',
                             self.__exercise_pose_count_label)
        self.__exercise_repetition_count_label = QLabel(self)
        sub_layout.addRow(u'Количество повторений:',
                          self.__exercise_repetition_count_label)
        main_layout.addLayout(sub_layout)
        main_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

    def get_exercise_name(self) -> str:
        return self.__exercise_name_label.text()
    
    def get_exercise_pose_count(self) -> int:
        return int(self.__exercise_pose_count_label.text())

    def get_exercise_repetition_count(self) -> int:
        return int(self.__exercise_repetition_count_label.text())
    
    def set_exercise_name(self, exercise_name: str) -> None:
        self.__exercise_name_label.setText(exercise_name)

    def set_exercise_repetition_count(self,
                                      exercise_repetition_count: int) -> None:
        if exercise_repetition_count < 0:
            return
        self.__exercise_repetition_count_label.setText(
            str(exercise_repetition_count))

    def set_exercise_pose_count(self, exercise_pose_count: int) -> None:
        if exercise_pose_count < 2:
            return
        self.__exercise_pose_count_label.setText(str(exercise_pose_count))
    