from ui_exercise_editor import Ui_ExerciseEditor

from exercise_info import ExerciseInfoEdit

from camera_handler import CameraHandler

import pose_utils as pu

from PySide6.QtMultimedia import QCameraDevice, QMediaDevices
from PySide6.QtCore import Qt, Slot, QTimer, QSize
from PySide6.QtGui import QImage, QPixmap, QPainter, QFont, QFontMetrics, QIcon
from PySide6.QtWidgets import (QDialog, QWidget, QListView,
    QListWidgetItem, QMessageBox, QStackedWidget,
    QLabel, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QCheckBox, QSpacerItem,
    QSizePolicy, QSpinBox, QPushButton, QListWidget, QLineEdit, QTextEdit, QFrame)


from typing import Optional, List

import qimage2ndarray

import numpy as np

class ExerciseEditor(QDialog):
    def __init__(
            self,
            parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle(u'Создание упражнения')
        
        __main_layout = QVBoxLayout(self)

        self.__stage_names = [u'Выбор веб-камеры',
                              u'Детектирование положений',
                              u'Результаты детектирования',
                              u'Информация об упражнении']
        self.__stage_label = QLabel(self.__stage_names[0], self)
        stage_font = self.font()
        stage_font.setBold(True)
        stage_font.setPointSize(14)
        self.__stage_label.setFont(stage_font)
        __main_layout.addWidget(self.__stage_label)

        self.__stage_widget = QStackedWidget(self)
        # camera
        __camera_widget = QWidget()
        __camera_widget_layout = QVBoxLayout(__camera_widget)

        __camera_device_layout = QFormLayout()
        self.__camera_combo_box = QComboBox(__camera_widget)
        __camera_device_layout.addRow(u'Камера:', self.__camera_combo_box)
        self.__preview_check_box = QCheckBox(__camera_widget)
        __camera_device_layout.addRow(u'Предпросмотр:',
                                      self.__preview_check_box)
        __camera_widget_layout.addLayout(__camera_device_layout)
        __camera_widget_layout.addSpacerItem(QSpacerItem(
            20,
            40,
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding))
        __camera_image_layout = QHBoxLayout()
        __camera_image_layout.addSpacerItem(QSpacerItem(
            40,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred))
        self.__camera_image_label = QLabel(__camera_widget)
        self.__camera_image_label.setSizePolicy(QSizePolicy.Policy.Preferred,
                                                QSizePolicy.Policy.Fixed)
        self.__camera_pixmap_demo = QPixmap(
            'resources/active-woman-working-out-home.jpg')
        self.__camera_pixmap_demo = self.__camera_pixmap_demo.scaled(500, 500)
        self.__camera_image_label.setPixmap(self.__camera_pixmap_demo)
        self.__camera_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__camera_image_label.setScaledContents(False)
        __camera_image_layout.addWidget(self.__camera_image_label)
        __camera_image_layout.addSpacerItem(QSpacerItem(
            40,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred))
        __camera_widget_layout.addLayout(__camera_image_layout)
        __camera_widget_layout.addSpacerItem(QSpacerItem(
            20,
            40,
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding) 
        )
        self.__stage_widget.addWidget(__camera_widget)
        # detection
        __detection_widget = QWidget()
        __detection_widget_layout = QVBoxLayout(__detection_widget)
        __detection_widget_layout.addSpacerItem(QSpacerItem(
            20,
            40,
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding)
        )
        __detection_image_layout = QHBoxLayout()
        __detection_image_layout.addSpacerItem(QSpacerItem(
            40,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred))
        self.__detection_image_label = QLabel(__detection_widget)
        self.__detection_image_label.setPixmap(self.__camera_pixmap_demo)
        self.__detection_image_label.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )
        self.__detection_image_label.setScaledContents(False)
        __detection_image_layout.addWidget(self.__detection_image_label)
        __detection_image_layout.addSpacerItem(QSpacerItem(
            40,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred))
        __detection_widget_layout.addLayout(__detection_image_layout)
        __detection_widget_layout.addSpacerItem(QSpacerItem(
            20,
            40,
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding)
        )
        __detection_control_layout = QHBoxLayout()
        __detection_time_control_layout = QVBoxLayout()
        __detection_time_control_label = QLabel(u'Настройки детектирования',
                                                __detection_widget)
        font = self.font()
        font.setPointSize(12)
        __detection_time_control_label.setFont(font)
        __detection_time_control_layout.addWidget(
            __detection_time_control_label)
        __detection_timer_layout = QFormLayout()
        self.__detection_timer_spin_box = QSpinBox(__detection_widget)
        self.__detection_timer_spin_box.setRange(2, 10)
        self.__detection_timer_spin_box.setValue(5)
        self.__detection_timer_spin_box.setSuffix(u' секунд')
        __detection_timer_layout.addRow(u'Время детектирования:',
                                        self.__detection_timer_spin_box)
        self.__detection_pause_spin_box = QSpinBox(__detection_widget)
        self.__detection_pause_spin_box.setRange(2, 10)
        self.__detection_pause_spin_box.setValue(5)
        self.__detection_pause_spin_box.setSuffix(u' секунд')
        __detection_timer_layout.addRow(u'Пауза после детектирования:',
                                        self.__detection_pause_spin_box)
        __detection_time_control_layout.addLayout(__detection_timer_layout)
        __detection_control_layout.addLayout(__detection_time_control_layout)
        self.__detection_button = QPushButton(u'Старт', __detection_widget)
        self.__detection_button.setSizePolicy(QSizePolicy.Policy.Fixed,
                                              QSizePolicy.Policy.Minimum)
        __detection_control_layout.addWidget(self.__detection_button)
        __detection_widget_layout.addLayout(__detection_control_layout)

        self.__stage_widget.addWidget(__detection_widget)
        # detection result
        __detection_result_widget = QWidget()
        __detection_result_widget_layout = QVBoxLayout(
            __detection_result_widget)
        self.__pose_list_widget = QListWidget(__detection_result_widget)
        self.__pose_list_widget.setIconSize(QSize(200,200))
        self.__pose_list_widget.setViewMode(QListView.ViewMode.IconMode)
        self.__pose_list_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__pose_list_widget.setResizeMode(QListView.ResizeMode.Adjust)
        self.__pose_list_widget.setMovement(QListView.Movement.Static)
        __detection_result_widget_layout.addWidget(self.__pose_list_widget)
        self.__stage_widget.addWidget(__detection_result_widget)
        # exercise info widget
        self.__exercise_info_widget = ExerciseInfoEdit()
        self.__stage_widget.addWidget(self.__exercise_info_widget)

        __main_layout.addWidget(self.__stage_widget)

        __dialog_button_layout = QHBoxLayout()
        __dialog_button_layout.addSpacerItem(QSpacerItem(
            40,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum))
        self.__prev_button = QPushButton(
            QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious),
            u'Назад',
            self
        )
        self.__prev_button.setVisible(False)
        __dialog_button_layout.addWidget(self.__prev_button)
        self.__next_button = QPushButton(
            QIcon.fromTheme(QIcon.ThemeIcon.GoNext),
            u'Далее',
            self
        )
        __dialog_button_layout.addWidget(self.__next_button)
        self.__cancel_button = QPushButton(u'Отмена', self)
        __dialog_button_layout.addWidget(self.__cancel_button)
        __main_layout.addLayout(__dialog_button_layout)

        self._is_detection = False
        self._is_preview = False

        self._pose_detector = None
        self._pose_painter = None
        self._pose_transformer = None
        self._mode_painter = None

        self._last_landmarks = None
        self._detection_image = None
        self._exercise_poses = []

        self._device_info = QMediaDevices(self)
        self._camera_map = None
        self._current_camera = self._device_info.defaultVideoInput()
        self._set_camera_list(self._device_info.videoInputs)
        self._device_info.videoInputsChanged.connect(self.update_camera_list)
        self.__camera_combo_box.currentTextChanged.connect(self.choose_camera)
        self.__preview_check_box.toggled.connect(
            self.check_preview)

        self._camera_handler = CameraHandler(self)

        self.__detection_timer_spin_box.valueChanged.connect(
            self.change_detection_time)
        self.__detection_pause_spin_box.valueChanged.connect(
            self.change_detection_pause)

        self._detection_timer = QTimer(self)
        self._detection_timer.setSingleShot(True)
        detection_time = self.__detection_timer_spin_box.value() * 1000
        self._detection_timer.setInterval(detection_time)

        self._detection_pause_timer = QTimer(self)
        self._detection_pause_timer.setSingleShot(True)
        detection_pause = self.__detection_pause_spin_box.value() * 1000
        self._detection_pause_timer.setInterval(detection_pause)

        self.__detection_button.clicked.connect(self.control_detection)

        self.__pose_list_widget.itemDoubleClicked.connect(self.delete_exercise_pose)

        self.__prev_button.clicked.connect(self.prev_stage)
        self.__next_button.clicked.connect(self.next_stage)
        self.__cancel_button.clicked.connect(self.reject)

    def _set_camera_list(self, camera_list: List[QCameraDevice]) -> None:
        self._camera_map = {}
        if len(camera_list()) == 0:
            self.__camera_combo_box.setEnabled(False)
            return
        
        for camera in camera_list():
            camera_descr = camera.description()
            self.__camera_combo_box.addItem(camera_descr)
            if camera == self._current_camera:
                self.__camera_combo_box.setCurrentText(camera_descr)
            self._camera_map[camera_descr] = camera

    def _set_image(self, label: QLabel, image: QImage):
        scaled_image = image.scaled(label.size(),
                                    Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation)
        pixmap = QPixmap.fromImage(scaled_image)
        label.setPixmap(pixmap)

    def get_exercise_poses(self) -> List[pu.Landmarks]:
        return self._exercise_poses
    
    def get_exercise_name(self) -> str:
        return self.__exercise_info_widget.get_exercise_name()
    
    def get_exercise_description(self) -> str:
        return self.__exercise_info_widget.get_exercise_description()
    
    def get_exercise_repetition_count(self) -> int:
        return self.__exercise_info_widget.get_exercise_repetition_count()

    @Slot()
    def update_camera_list(self) -> None:
        self.__camera_combo_box.clear()
        self._set_camera_list(self.device_info.videoInputs())
            
    @Slot(str)
    def choose_camera(self, camera_descr: str) -> None:
        self._current_camera = self._camera_map[camera_descr]
        self._camera_handler.change_camera_device(self._current_camera)

    @Slot(QImage)
    def demonstrate_camera_image(self, image: QImage) -> None:
        self._set_image(self.__camera_image_label, image)
        
    @Slot(bool)
    def check_preview(self, is_preview: bool) -> None:
        self._is_preview = is_preview
        if self._is_preview:
            self._camera_handler.current_image_changed.connect(
                self.demonstrate_camera_image)
            self._camera_handler.start_camera()
        else:
            self._camera_handler.current_image_changed.disconnect(
                self.demonstrate_camera_image)
            self._camera_handler.stop_camera()
            self.__camera_image_label.setPixmap(self.__camera_pixmap_demo)
    
    @Slot(int)
    def change_detection_time(self, sec: int) -> None:
        suffix = u' секунды' if sec < 5 else u' секунд'
        self.__detection_timer_spin_box.setSuffix(suffix)
        self._detection_timer.setInterval(sec * 1000)

    @Slot(int)
    def change_detection_pause(self, sec: int) -> None:
        suffix = u' секунды' if sec < 5 else u' секунд'
        self.__detection_pause_spin_box.setSuffix(suffix)
        self._detection_pause_timer.setInterval(sec * 1000)

    @Slot()
    def control_detection(self) -> None:
        self._is_detection = not self._is_detection
        if self._is_detection:
            self._detection_timer.timeout.connect(self.add_exercise_pose)
            self._camera_handler.start_camera()
            self.__detection_button.setText(u'Стоп')

            self._pose_detector = pu.PoseDetector()
            self._pose_transformer = pu.PoseTransformer()
            self._pose_painter = pu.PosePainter()
            self._mode_painter = QPainter()

            self._camera_handler.current_image_changed.connect(
                self.detect_exercise_pose)
        else:
            self._detection_timer.timeout.disconnect(self.add_exercise_pose)
            self._detection_timer.stop()
            
            self._camera_handler.current_image_changed.disconnect(
                self.detect_exercise_pose)
            self._camera_handler.stop_camera()

            self.__detection_image_label.setPixmap(self.__camera_pixmap_demo)

            self.__detection_button.setText(u'Старт')

            self._detection_image = None

            del self._pose_detector
            del self._pose_transformer
            del self._pose_painter
            del self._mode_painter

    @Slot(QImage)
    def detect_exercise_pose(self, image: QImage) -> None:
        mp_landmarks = self._pose_detector.detect_landmarks(image)
        if not mp_landmarks or not mp_landmarks[0]:
            if self._detection_timer.isActive():
                self._detection_timer.stop()
            self._set_image(self.__detection_image_label, image)
            return
        landmarks = self._pose_transformer.slice_landmarks(mp_landmarks[0])
        color = None
        
        if not self._detection_pause_timer.isActive():
            mode = 'Детектирование'
            if self._last_landmarks:
                sim = pu.compare_landmarks(landmarks, self._last_landmarks)
                if 1 - sim <= 5e-5:
                    color = Qt.GlobalColor.green
                else:
                    if self._detection_timer.isActive():
                        self._detection_timer.stop()
                    self._last_landmarks = None
                    color = Qt.GlobalColor.red
            else:
                self._detection_timer.start()
                self._last_landmarks = landmarks
                
                color = Qt.GlobalColor.green
                self._detection_image = image
        else:
            mode = 'Пауза'
            color = Qt.GlobalColor.blue
        image = self._pose_painter.draw_pose(landmarks, color, image)
        self._mode_painter.begin(image)
        
        font = self._mode_painter.font()
        font.setPixelSize(48)
        self._mode_painter.setFont(font)
        font_metric = QFontMetrics(font)
        mode = 'Режим: {}'.format(mode)
        rect = font_metric.boundingRect(mode)
        rect.moveTo(5, 5)
        rect.setWidth(rect.width() + 5)
        self._mode_painter.fillRect(rect, Qt.GlobalColor.yellow)
        self._mode_painter.drawText(rect, 0, mode)
        self._mode_painter.end()
        self._set_image(self.__detection_image_label, image)

    @Slot()
    def add_exercise_pose(self) -> None:
        self._detection_pause_timer.start()
        exercise_pose_pixmap = QPixmap.fromImage(self._detection_image)
        exercise_pose_icon = QIcon(exercise_pose_pixmap)
        exercise_pose_item = QListWidgetItem()
        exercise_pose_item.setIcon(exercise_pose_icon)
        self.__pose_list_widget.addItem(exercise_pose_item)
        self._exercise_poses.append(self._last_landmarks)
        self._last_landmarks = None

    @Slot(QListWidgetItem)
    def delete_exercise_pose(self, item: QListWidgetItem) -> None:
        idx = self.__pose_list_widget.row(item)
        item = self.__pose_list_widget.takeItem(idx)
        del item
        del self._exercise_poses[idx]

    @Slot()
    def prev_stage(self):
        prev_stage_idx = self.__stage_widget.currentIndex() - 1
        match prev_stage_idx:
            case 0:
                self.__prev_button.setVisible(False)
            case 2:
                self.__next_button.clicked.disconnect(self.accept)
                self.__next_button.clicked.connect(self.next_stage)
                self.__next_button.setText(u'Далее')
        
        self.__stage_widget.setCurrentIndex(prev_stage_idx)
        self.__stage_label.setText(self.__stage_names[prev_stage_idx])

    @Slot()
    def next_stage(self):
        next_stage_idx = self.__stage_widget.currentIndex() + 1
        match next_stage_idx:
            case 1:
                if self.__camera_combo_box.count() == 0:
                    QMessageBox.warning(
                        self,
                        u'Предупреждение',
                        u'Отсутсвует веб-камера!')
                    return
                
                if self._is_preview:
                    self.__preview_check_box.setChecked(False)

                self.__prev_button.setVisible(True)
            case 2:
                if self._is_detection:
                    QMessageBox.warning(
                        self,
                        u'Предупреждение',
                        u'Не завершено детектирование положений упражнения!')
                    return
            case 3:
                if self.__pose_list_widget.count() < 2:
                    QMessageBox.warning(
                        self,
                        u'Предупреждение',
                        u'Количество положений упражнения меньше 2!')
                    return
                
                self.__exercise_info_widget.set_exercise_pose_count(
                    len(self._exercise_poses))
                self.__next_button.clicked.disconnect(self.next_stage)
                self.__next_button.clicked.connect(self.accept)
                self.__next_button.setText(u'ОК')
        self.__stage_widget.setCurrentIndex(next_stage_idx)
        self.__stage_label.setText(self.__stage_names[next_stage_idx])

    @Slot()
    def accept(self) -> None:
        if not self.__exercise_info_widget.get_exercise_name():
            QMessageBox.warning(
                self,
                u'Предупреждение',
                u'Не указано наименование упражнения!')
            return

        return super().accept()
