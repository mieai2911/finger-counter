import cv2

from config import (
    CAMERA_INDEX,
    COUNT_COLOR,
    FRAME_HEIGHT,
    FRAME_WIDTH,
    TEXT_COLOR,
    TITLE_BACKGROUND,
    WINDOW_NAME,
)
from finger_counting import count_fingers
from hand_tracker import HandTracker


def draw_interface(frame, message: str) -> None:
    """Ve vung nen va cac dong chu len khung hinh."""
    cv2.rectangle(frame, (10, 10), (455, 85), TITLE_BACKGROUND, -1)
    cv2.putText(
        frame,
        message,
        (25, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.85,
        COUNT_COLOR,
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "Nhan Q de thoat",
        (25, 115),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        TEXT_COLOR,
        2,
        cv2.LINE_AA,
    )


def run_camera_app() -> None:
    """Chay ung dung dem ngon tay bang webcam cho den khi nhan Q."""
    camera = cv2.VideoCapture(CAMERA_INDEX)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not camera.isOpened():
        raise RuntimeError(
            "Khong mo duoc webcam. Hay kiem tra camera hoac doi CAMERA_INDEX "
            "trong config.py thanh 1."
        )

    tracker = None
    try:
        tracker = HandTracker()

        while True:
            ok, frame = camera.read()
            if not ok:
                print("Khong doc duoc hinh anh tu webcam.")
                break

            frame = cv2.flip(frame, 1)

            results = tracker.process(frame)
            message = "Hay dua mot ban tay vao khung hinh"

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                handedness_label = "Right"
                if results.multi_handedness:
                    handedness_label = (
                        results.multi_handedness[0].classification[0].label
                    )

                number_of_fingers = count_fingers(
                    hand_landmarks,
                    handedness_label,
                )
                message = f"So ngon tay: {number_of_fingers}"

                tracker.draw_landmarks(frame, hand_landmarks)

            draw_interface(frame, message)
            cv2.imshow(WINDOW_NAME, frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.release()
        if tracker is not None:
            tracker.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_camera_app()
