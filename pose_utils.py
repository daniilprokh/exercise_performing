import math

from typing import Optional, List, Tuple, Union

from mediapipe import Image, ImageFormat
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarker
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QImage, QPainter, QPen

import qimage2ndarray

import numpy as np

class Landmark():
    def __init__(self) -> None:
        self.x = -1.0
        self.y = -1.0
        self.visible = False
      
Landmarks = List[Landmark]

class PoseDetector():
    def __init__(self):
        self._detector = PoseLandmarker.create_from_model_path("models/pose_landmarker_full.task")

    def detect_landmarks(self,
                         image: QImage) -> List[List[NormalizedLandmark]]:
        rgb_view = qimage2ndarray.rgb_view(image)
        rgb_view = np.ascontiguousarray(rgb_view, dtype=np.uint8)
        mp_image = Image(image_format=ImageFormat.SRGB, data=rgb_view)
        detection_result = self._detector.detect(mp_image)
        return detection_result.pose_landmarks

class PoseTransformer():
    def __init__(self) -> None:
        self.__keypoint_idxes = [11, 12, 13, 14, 15, 16,
                                 23, 24, 25, 26, 27, 28]

    def slice_landmarks(
            self,
            mp_landmarks: List[NormalizedLandmark]) -> Landmarks:
        landmarks = []
        for idx in self.__keypoint_idxes :
            landmark = Landmark()
            mp_landmark = mp_landmarks[idx]
            landmark.x = mp_landmark.x
            landmark.y = mp_landmark.y
            landmark.visible = bool(
                mp_landmark.visibility > 0.5 and mp_landmark.presence > 0.5)
            landmarks.append(landmark)
        return landmarks

class PosePainter():
    def __init__(self) -> None:
        self.__painer = QPainter()

        self.__connections = frozenset(
            [(0, 1), (0, 2), (2, 4),
             (1, 3), (3, 5), (0, 6),
             (1, 7), (6, 7), (6, 8),
             (7, 9), (8, 10), (9, 11)])

    def __is_valid_normalized_value(self, value: float) -> bool:
        return ((value > 0 or math.isclose(0, value)) and
               (value < 1 or math.isclose(1, value)))

    def __normalized_to_pixel_coordinates(
            self, 
            landmark: Landmark,
            image_width: int, 
            image_height: int) -> Union[None,Tuple[int, int]]:
        if (not landmark.visible or 
            not self.__is_valid_normalized_value(landmark.x) or
            not self.__is_valid_normalized_value(landmark.y)):
            return None
        
        x_px = min(math.floor(landmark.x * image_width), image_width - 1)
        y_px = min(math.floor(landmark.y * image_height), image_height - 1)

        return x_px, y_px

    def draw_pose(self,
                  landmarks: Landmarks,
                  color: Qt.GlobalColor,
                  image: QImage) -> QImage:
        keypoints = {}
        for idx, landmark in enumerate(landmarks):
            keypoint = self.__normalized_to_pixel_coordinates(landmark,
                                                              image.width(),
                                                              image.height())
            if keypoint:
                keypoints[idx] = keypoint
        
        self.__painer.begin(image)

        self.__painer.setPen(QPen(color, 7))

        for connection in self.__connections:
            idx = connection[0]
            jdx = connection[1]
            if idx not in keypoints or jdx not in keypoints:
                continue
            lhs_keypoint = keypoints[idx]
            rhs_keypoint = keypoints[jdx]
            self.__painer.drawLine(lhs_keypoint[0], lhs_keypoint[1],
                                   rhs_keypoint[0], rhs_keypoint[1])

        for _, keypoint in keypoints.items():
            self.__painer.drawEllipse(QPoint(keypoint[0], keypoint[1]), 5, 5)

        self.__painer.end()
        return image

def compare_landmarks(lhs: Landmarks, rhs: Landmarks) -> float:
  res = 0.0
  n = len(lhs)
  for idx in range(n):
      lhs_landmark = lhs[idx]
      rhs_landmark = rhs[idx]

      a = (lhs_landmark.x * rhs_landmark.x +
           lhs_landmark.y * rhs_landmark.y)
    
      b = (math.sqrt(lhs_landmark.x**2 + lhs_landmark.y**2) *
           math.sqrt(rhs_landmark.x**2 + rhs_landmark.y**2))

      res += a / b
  return res / n