import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import mediapipe as mp
import cv2
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    """Calculates the angle between three points (e.g., shoulder, elbow, wrist)."""
    a = np.array(a) 
    b = np.array(b) 
    c = np.array(c) 
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    return angle

class YogaProcessor(VideoProcessorBase):
    def __init__(self):
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Process the image and find landmarks
        img.flags.writeable = False
        results = self.pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img.flags.writeable = True

        if results.pose_landmarks:
            # Draw the skeleton (The "Avatar" look)
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # Logic: Calculate Right Elbow Angle
            landmarks = results.pose_landmarks.landmark
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            angle = calculate_angle(shoulder, elbow, wrist)

            # Visual Feedback on Screen
            cv2.putText(img, f"Angle: {int(angle)}", 
                        tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        return frame.from_ndarray(img, format="bgr24")

# --- Streamlit UI ---
st.set_page_config(page_title="AI Yoga Studio", layout="wide")

st.title("🧘 AI-Powered Yoga Assistant")
st.markdown("""
### Data-Driven Alignment
This app uses your camera to map **33 skeletal landmarks**. 
No videos—just pure geometry.
""")

col1, col2 = st.columns([3, 1])

with col1:
    webrtc_streamer(key="yoga-pose", video_processor_factory=YogaProcessor)

with col2:
    st.subheader("Live Stats")
    st.metric("Focus Pose", "Warrior II")
    st.write("Keep your left arm at **180°**")
    st.progress(0.7) # Dynamic progress example
