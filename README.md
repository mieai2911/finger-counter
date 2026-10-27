# Finger Counter with MediaPipe

Tên: Giáp Trinh Đăng

MSSV: 26520242

## Requirements
- Python 3.12 hoặc uv
- Webcam

## Installation

```bash
pip install -r requirements.txt
```
Hoặc nếu sử dụng uv
```bash
uv sync
```

## Usage

```bash
python main.py
```
Hoặc nếu sử dụng uv
```bash
uv run main.py
```

Đưa lòng bàn tay về camera. Số ngón tay sẽ hiển thị trên video. Nhấn `Q` để thoát.

## Đọc bàn tay
- `__init__()`: Khởi tạo `mp.solutions.hands.Hands` với các tham số từ `config.py`.
- `process(frame_bgr)`: Chuyển khung hình từ BGR sang RGB, tắt writeable để tăng hiệu năng, sau đó gọi hands.process() và trả về results.
- `draw_landmarks(frame_bgr, hand_landmarks)`: Vẽ 21 điểm và các đường nối lên khung hình để quan sát trực quan.

# Đếm ngón
MediaPipe trả về 21 landmarks cho mỗi bàn tay (đánh số 0-20). Thuật toán dựa vào việc so sánh vị trí tương đối giữa đầu ngón và khớp bên dưới (PIP/IP) để xác định ngón có đang duỗi hay không.

Các hằng số quan trọng:
```
FINGER_TIPS = (8, 12, 16, 20) # Đầu ngón trỏ, giữa, áp út, út
FINGER_PIPS = (6, 10, 14, 18) # Khớp PIP tương ứng
THUMB_TIP   = 4 # Đầu ngón cái
THUMB_IP    = 3 # Khớp IP của ngón cái
```

- 4 ngón (trỏ, giữa, áp út, út): so sánh theo trục y. Trong hệ tọa độ ảnh của OpenCV, gốc (0,0) ở góc trên bên trái, y tăng dần xuống dưới.
- Nếu ngón đang duỗi thẳng lên, đầu ngón (tip) sẽ có y nhỏ hơn khớp PIP (nằm cao hơn trong khung hình).
- Nếu ngón đang co lại, đầu ngón sẽ bị hạ xuống, gần bằng hoặc lớn hơn y của PIP.
- Vì vậy, điều kiện landmarks[tip_id].y < landmarks[pip_id].y đồng nghĩa với "đầu ngón cao hơn khớp" -> ngón đang duỗi -> cộng 1.

Ngón cái được xử lý riêng `is_thumb_extended` vì nó di chuyển theo chiều ngang nhiều hơn chiều dọc.

- Lấy thumb_tip_x = landmarks[4].x, thumb_ip_x = landmarks[3].x (tọa độ chuẩn hóa x trong 0,1).
- Do khung hình đã được lật ngang trong main.py (giống gương), cách so sánh phải phụ thuộc vào tay trái/phải do MediaPipe xác định

# Demo

![Demo video](./demo.mp4)

a