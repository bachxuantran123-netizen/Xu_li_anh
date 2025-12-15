# model.py
import cv2
import mediapipe as mp
import numpy as np

class PostureModel:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, 
                                      min_detection_confidence=0.5, 
                                      min_tracking_confidence=0.5)

    def calculate_angle(self, a, b, c):
        """Tính góc giữa 3 điểm a, b, c (b là đỉnh)."""
        a = np.array(a) 
        b = np.array(b) 
        c = np.array(c) 
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle

    def process_frame(self, frame):
        """Xử lý frame ảnh để tìm landmark và tính góc."""
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = self.pose.process(image_rgb)
        
        data = {
            "landmarks": None,
            "angle": 0,
            "stage": "UNKNOWN",
            "is_bad_posture": False
        }

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            data["landmarks"] = landmarks
            h, w, _ = frame.shape
            
            # Lấy tọa độ (Giả định camera quay sườn trái - LEFT)
            ear = [landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value].x * w,
                   landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value].y * h]
            shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
            hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x * w,
                   landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y * h]

            angle = self.calculate_angle(ear, shoulder, hip)
            data["angle"] = angle

            # Logic ngưỡng cảnh báo
            # > 160: Tốt, < 140: Xấu (Em có thể tinh chỉnh số này)
            if angle > 160: 
                data["stage"] = "GOOD"
                data["is_bad_posture"] = False
            elif angle < 140:
                data["stage"] = "BAD"
                data["is_bad_posture"] = True
            else:
                data["stage"] = "NORMAL"
                data["is_bad_posture"] = False
                
        return data, results