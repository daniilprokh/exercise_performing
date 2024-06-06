from ui_exercise_window import Ui_ExerciseWindow

from complex_editor import ComplexEditor
from exercise_info import (ExerciseInfo, ExerciseInfoLabel,
    ExerciseRepetitionDialog)

from camera_handler import CameraHandler

import pose_utils as pu

from PySide6.QtMultimedia import QCameraDevice, QMediaDevices
from PySide6.QtWidgets import (QMainWindow, QWidget, QFileDialog,
    QListWidgetItem, QMessageBox)
from PySide6.QtGui import (QImage, QPixmap, QAction, QActionGroup,
    QPainter, QFontMetrics)
from PySide6.QtCore import Qt, Slot, QIODevice, QFile, QDataStream

from typing import Optional, List

class ExerciseWindow(QMainWindow):
    def __init__(self,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._ui = Ui_ExerciseWindow()
        self._ui.setupUi(self)

        self._window_title = self.windowTitle()

        self._is_training = False
        self._is_demonstration = False

        self._pose_detector = None
        self._pose_transformer = None
        self._pose_painter = None
        self._stat_painter = None

        self._complex_file_path = None
        self._complex_name = None
        self._complex_exercises = {}
        
        self._curent_exercise_position = 0
        self._curent_counter = 0
        self._curent_exercise_idx = 0

        self._current_exercise_label = None
        self._current_poses = None
        self._current_exercise_landmarks = None

        self._camera_action_group = QActionGroup(self)
        self._camera_action_group.triggered.connect(self.choose_camera)

        self._device_info = QMediaDevices(self)
        self._camera_map = None
        self._current_camera = self._device_info.defaultVideoInput()
        self._set_camera_list(self._device_info.videoInputs)
        self._device_info.videoInputsChanged.connect(self.update_camera_list)
        self._ui.preview_action.toggled.connect(self.demonstrate_camera_image)

        self._camera_handler = CameraHandler(self)

        self._ui.add_complex_action.triggered.connect(self.create_complex)
        self._ui.edit_complex_action.triggered.connect(self.change_complex)
        self._ui.choose_complex_action.triggered.connect(self.choose_complex)
        self._ui.close_complex_action.triggered.connect(self.close_complex)
        self._ui.exit_action.triggered.connect(self.close)

        self._ui.edit_rep_count_button.clicked.connect(
            self.edit_exercise_rep_count)
        self._ui.exercise_button.clicked.connect(self.control_exercise)

    def _set_camera_list(self, camera_list: List[QCameraDevice]):
        self._camera_map = {}
        if len(camera_list()) == 0:
            self._ui.preview_action.setEnabled(False)
            if self._is_training:
                self.control_exercise()
            return
        self._ui.preview_action.setEnabled(True)
        for camera in camera_list():
            camera_descr = camera.description()
            action = self._camera_action_group.addAction(camera_descr)
            action.setCheckable(True)
            if camera == self._current_camera:
                action.setChecked(True)
            self._camera_map[camera_descr] = camera
            self._ui.camera_menu.addAction(action)

    def _set_image(self, image: QImage):
        scaled_image = image.scaled(self._ui.exercise_image.size(),
                                    Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation)
        pixmap = QPixmap.fromImage(scaled_image)
        self._ui.exercise_image.setPixmap(pixmap)

    def _set_complex(self):
        self._ui.exercise_list.clear()
        for exercise_name, exercise_info in self._complex_exercises.items():
            item = QListWidgetItem()
            item.setText(exercise_name)
            item.setWhatsThis(exercise_info.description)

    @Slot()
    def update_camera_list(self):
        actions = self._camera_action_group.actions()
        if len(actions()) != 0:
            for action in actions():
                self._ui.camera_menu.removeAction(action)
                self._camera_action_group.removeAction(action)
        self._set_camera_list(self.device_info.videoInputs())
            
    @Slot(QAction)
    def choose_camera(self, action: QAction):
        self._current_camera = self._camera_map[action.text()]
        self._camera_handler.change_camera_device(self._current_camera)

    @Slot(QImage)
    def change_current_camera_image(self, image: QImage):
        self._set_image(image)

    @Slot(bool)
    def demonstrate_camera_image(self, is_demonstration: bool):
        self._is_demonstration = is_demonstration
        if self._is_training:
            return

        if self._is_demonstration:
            self._camera_handler.current_image_changed.connect(
                self.change_current_camera_image)
            self._camera_handler.start_camera()
        else:
            self._camera_handler.current_image_changed.disconnect(
                self.change_current_camera_image)
            self._camera_handler.stop_camera()
            self._ui.exercise_image.clear()
    
    def _set_training_mode(self):
        enabled = not self._is_training
        self._ui.add_complex_action.setEnabled(enabled)
        self._ui.edit_complex_action.setEnabled(enabled)
        self._ui.choose_complex_action.setEnabled(enabled)
        self._ui.close_complex_action.setEnabled(enabled)
        self._ui.camera_menu.setEnabled(enabled)
        self._ui.exercise_list_widget.setEnabled(enabled)
        self._ui.edit_rep_count_button.setEnabled(enabled)

    @Slot()
    def control_exercise(self):
        self._is_training = not self._is_training
        if self._is_training:
            if self._current_camera.isNull():
                QMessageBox.warning(self,
                                    u'Предупреждение',
                                    u'Отсутсвует веб-камера!')
                self._is_training = not self._is_training
                return
            
            if self._ui.exercise_list_widget.count() == 0:
                QMessageBox.warning(self,
                                    u'Предупреждение',
                                    u'Отсутствуют упражнения!')
                self._is_training = not self._is_training
                return

            if not self._camera_handler.is_running():
                self._camera_handler.start_camera()
            self._ui.exercise_button.setText(u'Стоп')
            if self._is_demonstration:
                self._camera_handler.current_image_changed.disconnect(
                    self.change_current_camera_image)
                self._ui.exercise_image.clear()

            self._pose_detector = pu.PoseDetector()
            self._pose_transformer = pu.PoseTransformer()
            self._pose_painter = pu.PosePainter()    
            self._stat_painter = QPainter()

            exercise_item = self._ui.exercise_list_widget.item(
                self._curent_exercise_idx)
            self._current_exercise_label = self._ui.exercise_list_widget.itemWidget(
                exercise_item)
            exercise_name = self._current_exercise_label.get_exercise_name()
            self._current_poses = self._complex_exercises[exercise_name].poses
            self._current_exercise_landmarks = self._current_poses[self._curent_exercise_position]

            self._camera_handler.current_image_changed.connect(
                self.perform_exercise)
        else:
            self._camera_handler.current_image_changed.disconnect(
                self.perform_exercise)
            self._ui.exercise_image.clear()
            if self._is_demonstration:
                self._camera_handler.current_image_changed.connect(
                    self.change_current_camera_image)
            else:
                self._camera_handler.stop_camera()
            self._ui.exercise_button.setText(u'Старт')

            del self._pose_detector
            del self._pose_transformer
            del self._pose_painter
            del self._stat_painter

            self._curent_exercise_position = 0
            self._curent_counter = 0
            self._curent_exercise_idx = 0

            self._current_exercise_label = None
            self._current_poses = None
            self._current_exercise_landmarks = None
        self._set_training_mode()

    def _set_exercises(self):
        self._ui.exercise_list_widget.clear()
        for exercise_name, exercise_info in self._complex_exercises.items():
            exercise_list_item = QListWidgetItem(self._ui.exercise_list_widget)
            exercise_list_item.setWhatsThis(exercise_info.description)
            exercise_list_item_label = ExerciseInfoLabel()
            exercise_list_item_label.set_exercise_name(exercise_name)
            exercise_list_item_label.set_exercise_pose_count(
                len(exercise_info.poses))
            exercise_list_item_label.set_exercise_repetition_count(
                exercise_info.repetition_count)
            exercise_list_item.setSizeHint(exercise_list_item_label.sizeHint())
            self._ui.exercise_list_widget.addItem(exercise_list_item)
            self._ui.exercise_list_widget.setItemWidget(
                exercise_list_item,
                exercise_list_item_label)
            self._ui.exercise_list_widget.setCurrentItem(exercise_list_item)

    @Slot()
    def create_complex(self):
        complex_editor = ComplexEditor(self)
        complex_editor.setModal(True)
        complex_editor.show()
        result = complex_editor.exec()
        if result == ComplexEditor.DialogCode.Rejected:
            complex_editor.deleteLater()
            return
        
        self._complex_file_path = complex_editor.get_comlex_file_path()
        self._complex_name = complex_editor.get_complex_name()
        new_window_title = '{0} - {1}'.format(self._window_title,
                                              self._complex_name)
        self.setWindowTitle(new_window_title)

        self._complex_exercises = complex_editor.get_complex_exercises()

        self._set_exercises()
        
        self._ui.edit_rep_count_button.setEnabled(True)
        self._ui.close_complex_action.setEnabled(True)
        self._ui.edit_complex_action.setEnabled(True)
    
    @Slot()
    def change_complex(self):
        complex_editor = ComplexEditor(self)
        complex_editor.setModal(True)
        complex_editor.set_comlex_file_path(self._complex_file_path)
        complex_editor.set_complex_name(self._complex_name)
        complex_editor.set_complex_exercises(self._complex_exercises)
        complex_editor.show()
        result = complex_editor.exec()
        if result == ComplexEditor.DialogCode.Rejected:
            complex_editor.deleteLater()
            return
        
        self._complex_name = complex_editor.get_complex_name()
        new_window_title = '{0} - {1}'.format(self._window_title,
                                              self._complex_name)
        self.setWindowTitle(new_window_title)

        self._complex_exercises = complex_editor.get_complex_exercises()

        self._set_exercises()
    
    @Slot()
    def choose_complex(self):
        self._complex_file_path, _ = QFileDialog.getOpenFileName(
            self,
            u'Выбрать комплекс',
            '',
            u'Комплекс (*.cmplx)')
        if not self._complex_file_path:
            return
        
        file = QFile(self._complex_file_path)
        if not file.open(QIODevice.OpenModeFlag.ReadOnly):
            del self._complex_file_path
            return
        
        stream = QDataStream(file)
        self._complex_name = stream.readString()
        print('Complex name: {0}'.format(self._complex_name))
        exercise_count = stream.readUInt64()
        print('Exercise count: {0}'.format(exercise_count))
        exercise_names = []
        complex_exercises = {}
        for exercise_idx in range(exercise_count):
            print('-Exercise {0}:'.format(exercise_idx + 1))
            exercise_name = stream.readString()
            print('--Name: {0}'.format(exercise_name))
            exercise_description = stream.readString()
            print('--Description: {0}'.format(exercise_description))
            pose_count = stream.readUInt64()
            print('--Pose count: {0}'.format(pose_count))
            repetition_count = stream.readUInt64()
            print('--Repetition count: {0}'.format(repetition_count))
            poses = []
            for pose_idx in range(pose_count):
                print('---Pose {0}:'.format(pose_idx + 1))
                landmark_count = stream.readUInt64()
                landmarks = []
                for landmark_idx in range(landmark_count):
                    landmark = pu.Landmark()
                    landmark.x = stream.readFloat()
                    landmark.y = stream.readFloat()
                    landmark.visible = stream.readBool()
                    landmarks.append(landmark)
                    print('----Landmark {0}: x = {1}, y = {2}, visible = {3}'.format(
                        landmark_idx + 1,
                        landmark.x,
                        landmark.y,
                        landmark.visible))
                poses.append(landmarks)
            complex_exercises[exercise_name] = ExerciseInfo(
                exercise_description,
                repetition_count,
                poses)
            exercise_names.append(exercise_name)
        file.close()

        new_window_title = '{0} - {1}'.format(self._window_title,
                                              self._complex_name)
        self.setWindowTitle(new_window_title)

        self._complex_exercises = complex_exercises
        
        self._set_exercises()

        self._ui.edit_rep_count_button.setEnabled(True)
        self._ui.close_complex_action.setEnabled(True)
        self._ui.edit_complex_action.setEnabled(True)
    
    @Slot()
    def close_complex(self):
        self._complex_file_path = None
        self._complex_name = None
        del self._complex_exercises
        self._ui.exercise_list_widget.clear()

        self.setWindowTitle(self._window_title)
        
        self._ui.close_complex_action.setEnabled(False)
        self._ui.edit_complex_action.setEnabled(False)
        self._ui.edit_rep_count_button.setEnabled(False)

    @Slot()
    def edit_exercise_rep_count(self):
        item = self._ui.exercise_list_widget.currentItem()
        exercise_label = self._ui.exercise_list_widget.itemWidget(item)

        exercise_rep_dialog = ExerciseRepetitionDialog(
            exercise_label.get_exercise_name(),
            exercise_label.get_exercise_repetition_count(),
            self)
        exercise_rep_dialog.setModal(True)
        exercise_rep_dialog.resize(700, 70)
        exercise_rep_dialog.show()
        result = exercise_rep_dialog.exec()
        if result == ExerciseRepetitionDialog.DialogCode.Rejected:
            exercise_rep_dialog.deleteLater()
            return
        
        exercise_label.set_exercise_repetition_count(
            exercise_rep_dialog.get_exercise_repetition_count())

    @Slot()
    def perform_exercise(self, image: QImage):
        demo_image = image
        rep_count = self._current_exercise_label.get_exercise_repetition_count()
        self._stat_painter.begin(demo_image)

        font = self._stat_painter.font()
        font.setPixelSize(48)
        self._stat_painter.setFont(font)
        font_metric = QFontMetrics(font)
        name_stat = 'Упражнение: {}'.format(
            self._current_exercise_label.get_exercise_name())
        rect = font_metric.boundingRect(name_stat)
        rect.moveTo(5, 5)
        rect.setWidth(rect.width() + 5)
        self._stat_painter.fillRect(rect, Qt.GlobalColor.yellow)
        self._stat_painter.drawText(
            rect,
            0,
            name_stat
        )
        
        rep_stat = 'Повторение: {0} / {1}'.format(self._curent_counter + 1,
                                                  rep_count)
        bottom = rect.bottom()
        rect = font_metric.boundingRect(rep_stat)
        rect.moveTo(5, bottom + 5)
        rect.setWidth(rect.width() + 5)
        self._stat_painter.fillRect(rect, Qt.GlobalColor.yellow)
        self._stat_painter.drawText(
            rect,
            0,
            rep_stat
        )

        self._stat_painter.end()

        self._set_image(self._pose_painter.draw_pose(
            self._current_poses[self._curent_exercise_position],
            Qt.GlobalColor.green,
            demo_image))
        
        mp_landmarks = self._pose_detector.detect_landmarks(image)
        if not mp_landmarks or not mp_landmarks[0]:
            return
        landmarks = self._pose_transformer.slice_landmarks(mp_landmarks[0])
        sim = pu.compare_landmarks(
            landmarks,
            self._current_poses[self._curent_exercise_position])
        if 1 - sim > 1e-4:
            return
        self._curent_exercise_position += 1
        if self._curent_exercise_position != len(self._current_poses):
            return
        self._curent_exercise_position = 0
            
        self._curent_counter += 1
        if self._curent_counter != self._current_exercise_label.get_exercise_repetition_count():
            return
        self._curent_counter = 0

        self._curent_exercise_idx += 1
        if self._curent_exercise_idx == self._ui.exercise_list_widget.count():
            self._curent_exercise_idx = 0
        exercise_item = self._ui.exercise_list_widget.item(
            self._curent_exercise_idx)
        self._current_exercise_label = self._ui.exercise_list_widget.itemWidget(
            exercise_item)
        exercise_name = self._current_exercise_label.get_exercise_name()
        self._current_poses = self._complex_exercises[exercise_name].poses
            