from PySide6.QtMultimedia import (QCamera, QCameraDevice, 
                                  QMediaCaptureSession, QMediaDevices,
                                  QVideoSink, QVideoFrame)
from PySide6.QtGui import QImage
from PySide6.QtCore import QObject, Signal, Slot

class CameraHandler(QObject):
    current_image_changed = Signal(QImage)

    def __init__(self,
                 parent: QObject | None = ...,
                 device: QCameraDevice = QMediaDevices.defaultVideoInput()):
        super().__init__(parent)

        self._device = device
        self._camera = None
        self._capture_session = None

        self._video_sink = QVideoSink(self)

    @Slot()
    def start_camera(self):
        if self.is_running():
            return

        self._camera = QCamera(self._device)
        
        self._capture_session = QMediaCaptureSession()
        self._capture_session.setCamera(self._camera)
        
        self._capture_session.setVideoSink(self._video_sink)
        self._video_sink.videoFrameChanged.connect(self.process_frame)

        self._camera.start()

    @Slot(QVideoFrame)
    def process_frame(self, frame : QVideoFrame):
        if not frame.isValid():
            return
        image = frame.toImage()
        if image.format() == QImage.Format.Format_Invalid:
            return
        image.mirror(True, False)
        self.current_image_changed.emit(image)

    @Slot()
    def stop_camera(self):
        if not self.is_running():
            return

        self._video_sink.videoFrameChanged.disconnect(self.process_frame)
        self._camera.stop()

        self._capture_session.deleteLater()
        self._capture_session = None
        self._camera.deleteLater()
        self._camera = None

    def change_camera_device(self, device: QCameraDevice):
        if (self._device == device):
            return
        
        self._device = device
        if self._camera:
          self._camera.setCameraDevice(device)

    def is_running(self):
        return True if self._camera else False
