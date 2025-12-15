# controller.py
import cv2
import threading
import time
import platform
# Import class từ các file khác cùng thư mục
from model import PostureModel
from view import PostureView

# Xử lý import winsound chỉ cho Windows
if platform.system() == "Windows":
    import winsound

class PostureController:
    def __init__(self, video_source=0):
        self.cap = cv2.VideoCapture(video_source)
        self.model = PostureModel()
        self.view = PostureView()
        
        # Cấu hình âm thanh
        self.last_alert_time = 0
        self.alert_cooldown = 2.0 # Thời gian nghỉ giữa 2 lần kêu (giây)

    def play_sound(self):
        """Hàm chạy trong luồng riêng."""
        try:
            if platform.system() == "Windows":
                winsound.Beep(1000, 500) # Tần số 1000Hz, 500ms
            else:
                # MacOS/Linux
                print('\a') 
        except Exception:
            pass

    def trigger_alert(self):
        """Kiểm tra thời gian và kích hoạt âm thanh."""
        current_time = time.time()
        if current_time - self.last_alert_time > self.alert_cooldown:
            t = threading.Thread(target=self.play_sound)
            t.daemon = True 
            t.start()
            self.last_alert_time = current_time

    def run(self):
        print("Đang khởi động Posture AI" \
        "Nhấn 'q' để thoát.")
        
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("Không nhận được tín hiệu camera.")
                break

            # 1. Model xử lý toán học
            data, raw_results = self.model.process_frame(frame)

            # 2. Controller kiểm tra logic nghiệp vụ (Cảnh báo âm thanh)
            if data["is_bad_posture"]:
                self.trigger_alert()

            # 3. View hiển thị hình ảnh
            output_frame = self.view.render(frame, data, raw_results)

            # Hiển thị
            cv2.imshow('Posture Corrector AI', output_frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()