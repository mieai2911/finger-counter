import cv2
import mediapipe as mp

from config import (
    MAX_NUM_HANDS,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    MODEL_COMPLEXITY,
)


class HandTracker:
    """Quan ly vong doi MediaPipe Hands va cac thao tac lien quan."""

    def __init__(self) -> None:
        self._mp_hands = mp.solutions.hands
        self._mp_drawing = mp.solutions.drawing_utils
        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_NUM_HANDS,
            model_complexity=MODEL_COMPLEXITY,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        )

    def process(self, frame_bgr):
        """Nhan frame BGR tu OpenCV, chuyen sang RGB va tra ket qua MediaPipe."""
        rgb_frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = self._hands.process(rgb_frame)
        return results

    def draw_landmarks(self, frame_bgr, hand_landmarks) -> None:
        """Ve cac landmarks va duong noi len frame BGR."""
        self._mp_drawing.draw_landmarks(
            frame_bgr,
            hand_landmarks,
            self._mp_hands.HAND_CONNECTIONS,
        )

    def close(self) -> None:
        """Giai phong tai nguyen MediaPipe."""
        self._hands.close()

