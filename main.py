# main.py
from controller import PostureController

if __name__ == "__main__":
    app = PostureController(video_source=r"C:\Disk\Study\test (Python)\PostureAI_Project\demo_posture.mp4")  

    app.run()