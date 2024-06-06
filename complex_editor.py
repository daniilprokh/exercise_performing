from ui_complex_editor import Ui_ComplexEditor

from exercise_editor import ExerciseEditor
from exercise_info import ExerciseInfo, ExerciseInfoLabel, ExerciseInfoDialog

from pose_utils import Landmarks

from PySide6.QtCore import Qt, Slot, QFile, QIODevice, QDataStream
from PySide6.QtWidgets import (QDialog, QWidget, QListWidgetItem, QMessageBox,
    QFileDialog, QVBoxLayout, QHBoxLayout, QPushButton)

from typing import Optional, Dict, List

class ComplexEditor(QDialog):
    def __init__(
            self,
            parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._ui = Ui_ComplexEditor()
        self._ui.setupUi(self)

        self._exercises = []
        self._complex_file_path = None

        self._ui.add_button.clicked.connect(self.add_exercise)
        self._ui.edit_button.clicked.connect(self.edit_exercise)
        self._ui.delete_button.clicked.connect(self.delete_exercise)

        self._ui.save_button.clicked.connect(self.save)
        self._ui.save_as_button.clicked.connect(self.save_as)
        self._ui.cancel_button.clicked.connect(self.reject)
  
    def _add_exercise(self, 
                      exercise_name: str,
                      exercise_description: str,
                      exercise_repetition_count: int,
                      exercise: List[Landmarks]) -> None:
        self._exercises.append(exercise)

        exercise_list_item = QListWidgetItem(self._ui.exercise_list_widget)
        exercise_list_item.setWhatsThis(exercise_description)
        exercise_list_item_label = ExerciseInfoLabel()
        exercise_list_item_label.set_exercise_name(exercise_name)
        exercise_list_item_label.set_exercise_pose_count(len(exercise))
        exercise_list_item_label.set_exercise_repetition_count(
            exercise_repetition_count)
        exercise_list_item.setSizeHint(exercise_list_item_label.sizeHint())
        self._ui.exercise_list_widget.addItem(exercise_list_item)
        self._ui.exercise_list_widget.setItemWidget(exercise_list_item,
                                                    exercise_list_item_label)
        self._ui.exercise_list_widget.setCurrentItem(exercise_list_item)
        self._ui.edit_button.setEnabled(True)
        self._ui.delete_button.setEnabled(True)

    def get_complex_name(self) -> str:
        return self._ui.complex_name_edit.text()

    def get_complex_exercises(self) -> Dict[str, ExerciseInfo]:
        complex_exercises = {}
        for row in range(self._ui.exercise_list_widget.count()):
            exercise_item = self._ui.exercise_list_widget.item(row)
            exercise_item_label = self._ui.exercise_list_widget.itemWidget(exercise_item)
            exercise_name = exercise_item_label.get_exercise_name()
            complex_exercises[exercise_name] = ExerciseInfo(
                exercise_item.whatsThis(),
                exercise_item_label.get_exercise_repetition_count(),
                self._exercises[row]) 
        return complex_exercises
    
    def get_comlex_file_path(self) -> str:
        return self._complex_file_path
    
    def set_complex_name(self, complex_name: str) -> None:
        self._ui.complex_name_edit.setText(complex_name)

    def set_complex_exercises(
            self, 
            complex_exercises: Dict[str, ExerciseInfo]) -> None:
        for exercise_name, exercise_info in complex_exercises.items():
            self._add_exercise(exercise_name,
                               exercise_info.description,
                               exercise_info.repetition_count,
                               exercise_info.poses)

    def set_comlex_file_path(self, complex_file_path: str) -> None:
        self._complex_file_path = complex_file_path

    @Slot()
    def add_exercise(self) -> None:
        exercise_editor = ExerciseEditor(self)
        exercise_editor.setModal(True)
        exercise_editor.show()
        result = exercise_editor.exec()
        if result == ExerciseEditor.DialogCode.Rejected:
            exercise_editor.deleteLater()
            return
        
        self._add_exercise(
            exercise_editor.get_exercise_name(),
            exercise_editor.get_exercise_description(),
            exercise_editor.get_exercise_repetition_count(),
            exercise_editor.get_exercise_poses())
        
    @Slot()
    def edit_exercise(self) -> None:
        item = self._ui.exercise_list_widget.currentItem()
        exercise_label = self._ui.exercise_list_widget.itemWidget(item)

        exercise_edit_dialog = ExerciseInfoDialog(self)
        exercise_edit_dialog.resize(550, 500)
        exercise_edit_dialog.setModal(True)

        exercise_info_edit = exercise_edit_dialog.get_exercise_info_edit()
        exercise_info_edit.set_exercise_name(
            exercise_label.get_exercise_name())
        exercise_info_edit.set_exercise_description(item.whatsThis())
        exercise_info_edit.set_exercise_repetition_count(
            exercise_label.get_exercise_repetition_count())
        exercise_info_edit.set_exercise_pose_count(
            exercise_label.get_exercise_pose_count())
        exercise_edit_dialog.show()
        result = exercise_edit_dialog.exec()
        if result == ExerciseInfoDialog.DialogCode.Rejected:
            exercise_edit_dialog.deleteLater()
            return
        
        exercise_label.set_exercise_name(
            exercise_info_edit.get_exercise_name())
        item.setWhatsThis(exercise_info_edit.get_exercise_description())
        exercise_label.set_exercise_pose_count(
            exercise_info_edit.get_exercise_pose_count())
        exercise_label.set_exercise_repetition_count(
            exercise_info_edit.get_exercise_repetition_count())
    
    @Slot()
    def delete_exercise(self) -> None:
        item = self._ui.exercise_list_widget.currentItem()
        self._ui.exercise_list_widget.removeItemWidget(item)
        row = self._ui.exercise_list_widget.row(item)
        item = self._ui.exercise_list_widget.takeItem(row)
        del item
        if self._ui.exercise_list_widget.count() == 0:
            self._ui.edit_button.setEnabled(False)
            self._ui.delete_button.setEnabled(False)

    def _save_check(self) -> bool:
        if self._ui.exercise_list_widget.count() == 0:
            QMessageBox.warning(self,
                u'Предупреждение',
                u'Отсутствуют упражнения!')
            return False
        elif not self._ui.complex_name_edit.text():
            QMessageBox.warning(self,
                u'Предупреждение',
                u'Отсутствует наименование комплекса!')
            return False
        return True

    def _save(self) -> None:
        file = QFile(self._complex_file_path)
        file.open(QIODevice.OpenModeFlag.WriteOnly)
        stream = QDataStream(file)
        stream.writeString(self._ui.complex_name_edit.text())
        exercise_count = self._ui.exercise_list_widget.count()
        stream.writeInt64(exercise_count)
        for row in range(exercise_count):
            exercise_item = self._ui.exercise_list_widget.item(row)
            exercise_item_label = self._ui.exercise_list_widget.itemWidget(exercise_item)
            stream.writeString(exercise_item_label.get_exercise_name())
            stream.writeString(exercise_item.whatsThis())
            stream.writeInt64(exercise_item_label.get_exercise_pose_count())
            stream.writeInt64(exercise_item_label.get_exercise_repetition_count())
            poses = self._exercises[row]
            for pose in poses:
                stream.writeInt64(len(pose))
                for landmark in pose:
                    stream.writeFloat(landmark.x)
                    stream.writeFloat(landmark.y)
                    stream.writeBool(landmark.visible)
        file.close()

    @Slot()
    def save(self) -> None:
        if not self._save_check():
            return
        
        if not self._complex_file_path:
            complex_file_path, _ = QFileDialog.getSaveFileName(
                self,
                u'Сохранение комплекса',
                '',
                u'Комплекс (*.cmplx)')
            if not complex_file_path:
                return
            self._complex_file_path = complex_file_path
            
        self._save()

        super().accept()

    @Slot()
    def save_as(self) -> None:
        if not self._save_check():
            return
        
        complex_file_path, _ = QFileDialog.getSaveFileName(
                self,
                u'Сохранение комплекса',
                '',
                u'Комплекс (*.cmplx)')
        if not complex_file_path:
            return
        self._complex_file_path = complex_file_path

        self._save()

        super().accept()
