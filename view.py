# view.py
import cv2
import mediapipe as mp

class PostureView:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

    def render(self, frame, data, raw_results):
        h, w, _ = frame.shape

        # 1. Cảnh báo đỏ nếu sai tư thế (Giữ nguyên logic cũ)
        if data["is_bad_posture"]:
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 255), -1)
            cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
            cv2.putText(frame, "SAI TU THE!", (50, int(h/2)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        # 2. Vẽ xương (Giữ nguyên)
        if raw_results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame, raw_results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
            )

        # Vẽ nền đen nhỏ góc trái để chữ dễ đọc
        cv2.rectangle(frame, (0, 0), (250, 120), (0, 0, 0), -1)
        
        # Dòng 1: Trạng thái (Ngồi/Đứng/Đấm)
        cv2.putText(frame, f"State: {data['state']}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Dòng 2: Góc lưng
        cv2.putText(frame, f"Torso Angle: {int(data['angle'])}", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # Dòng 3: Góc chân
        cv2.putText(frame, f"Leg Angle: {int(data['leg_angle'])}", (10, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        return frame