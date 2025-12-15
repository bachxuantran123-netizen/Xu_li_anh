# view.py
import cv2
import mediapipe as mp

class PostureView:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

    def render(self, frame, data, raw_results):
        h, w, _ = frame.shape

        # 1. Vẽ hiệu ứng cảnh báo đỏ nếu sai tư thế
        if data["is_bad_posture"]:
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 255), -1)
            alpha = 0.3
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
            
            cv2.putText(frame, "SAI TU THE!", (int(w/2) - 150, int(h/2)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4, cv2.LINE_AA)

        # 2. Vẽ khung xương
        if raw_results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame, raw_results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
            )

        # 3. Hiển thị thông số góc
        # Vẽ bảng nền
        cv2.rectangle(frame, (0, 0), (225, 80), (245, 117, 16), -1)
        
        # Góc
        cv2.putText(frame, str(int(data["angle"])), (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Trạng thái
        cv2.putText(frame, data["stage"], (80, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        return frame