# main.py
from controller import PostureController

if __name__ == "__main__":
    app = PostureController(video_source=0)

    app.run()