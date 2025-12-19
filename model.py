# model.py
import cv2
import mediapipe as mp
import numpy as np

class PostureModel:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, 
                                      min_detection_confidence=0.6, 
                                      min_tracking_confidence=0.6)
        self.lm = self.mp_pose.PoseLandmark

    def calculate_angle(self, a, b, c):
        a = np.array(a) 
        b = np.array(b) 
        c = np.array(c) 
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0: angle = 360 - angle
        return angle

    def get_coord(self, landmarks, landmark_name, w, h):
        return [landmarks[landmark_name.value].x * w,
                landmarks[landmark_name.value].y * h]

    def process_frame(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = self.pose.process(image_rgb)
        
        data = {
            "landmarks": None,
            "angle": 0,
            "leg_angle": 0,      
            "arm_angle": 0,
            "state": "Unknown",
            "is_bad_posture": False
        }

        if results.pose_landmarks:
            lms = results.pose_landmarks.landmark
            data["landmarks"] = lms
            h, w, _ = frame.shape
            
            ear = self.get_coord(lms, self.lm.LEFT_EAR, w, h)
            shoulder = self.get_coord(lms, self.lm.LEFT_SHOULDER, w, h)
            hip = self.get_coord(lms, self.lm.LEFT_HIP, w, h)
            knee = self.get_coord(lms, self.lm.LEFT_KNEE, w, h)
            ankle = self.get_coord(lms, self.lm.LEFT_ANKLE, w, h)

            shoulder_r = self.get_coord(lms, self.lm.RIGHT_SHOULDER, w, h)
            elbow_r = self.get_coord(lms, self.lm.RIGHT_ELBOW, w, h)
            wrist_r = self.get_coord(lms, self.lm.RIGHT_WRIST, w, h)

            torso_angle = self.calculate_angle(ear, shoulder, hip) 
            leg_angle = self.calculate_angle(hip, knee, ankle)
            arm_angle = self.calculate_angle(shoulder_r, elbow_r, wrist_r)
            
            data["angle"] = torso_angle
            data["leg_angle"] = leg_angle
            data["arm_angle"] = arm_angle
            
            if arm_angle > 150 and abs(wrist_r[1] - shoulder_r[1]) < h * 0.15:
                data["state"] = "PUNCHING"
                data["is_bad_posture"] = False 

            elif leg_angle > 165:
                data["state"] = "STANDING"
                if torso_angle < 160:
                    data["is_bad_posture"] = True
                else:
                    data["is_bad_posture"] = False

            else:
                data["state"] = "SITTING"
                if torso_angle < 150:
                    data["is_bad_posture"] = True
                else:
                    data["is_bad_posture"] = False
                
        return data, results