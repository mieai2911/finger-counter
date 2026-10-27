from typing import Any

FINGER_TIPS = (8, 12, 16, 20)
FINGER_PIPS = (6, 10, 14, 18)

THUMB_TIP = 4
THUMB_IP = 3


def is_thumb_extended(landmarks: Any, handedness_label: str) -> bool:
    """Tra ve True neu ngon cai duoc xem la dang duoi.

    Anh dua vao ham duoc lat ngang nhu guong soi truoc khi MediaPipe xu ly.
    Vi vay, phep so sanh toa do x duoc chon theo nhan tay Left/Right do MediaPipe
    tra ve. Day la quy tac don gian, phu hop nhat khi long ban tay huong ve camera.
    """
    thumb_tip_x = landmarks[THUMB_TIP].x
    thumb_ip_x = landmarks[THUMB_IP].x

    if handedness_label == "Right":
        return thumb_tip_x < thumb_ip_x

    return thumb_tip_x > thumb_ip_x


def count_fingers(hand_landmarks: Any, handedness_label: str) -> int:
    """Dem so ngon duoi, ket qua trong khoang tu 0 den 5.

    Quy tac:
    - Ngon cai: so sanh toa do x cua dau ngon (landmark 4) va khop IP (3).
    - Bon ngon con lai: ngon duoi neu toa do y cua dau ngon nho hon toa do y
      cua khop PIP tuong ung. Trong anh, truc y tang theo huong xuong duoi.

    Ham tu xay dung logic dem; MediaPipe chi cung cap cac landmarks va nhan tay.
    """
    landmarks = hand_landmarks.landmark
    total = 0

    if is_thumb_extended(landmarks, handedness_label):
        total += 1

    for tip_id, pip_id in zip(FINGER_TIPS, FINGER_PIPS):
        if landmarks[tip_id].y < landmarks[pip_id].y:
            total += 1

    return total

