# main.py
from controller import PostureController

if __name__ == "__main__":
    # Khởi tạo ứng dụng với camera mặc định (index 0)
    # Nếu dùng video file, thay số 0 bằng đường dẫn: "video.mp4"
    app = PostureController(video_source=0)
    
    # Chạy ứng dụng
    app.run()