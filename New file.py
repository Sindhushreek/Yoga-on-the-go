import streamlit as st
import cv2
import numpy as np
import streamlit as st
import cv2
import numpy as np


try:
    from mediapipe.solutions import pose as mp_pose
    from mediapipe.solutions import drawing_utils as mp_drawing
except ImportError:

    import mediapipe as mp
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

# Initialize the pose model
pose_engine = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# --- CONFIG & STYLING ---
st.set_page_config(page_title="ZenStream AI", layout="wide")
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# --- DATABASE (Example) ---
YOGA_DB = {
    "High": [
        {"name": "Warrior II", "image": "https://example.com/warrior2.jpg", "target_angle": 90},
        {"name": "Plank", "image": "https://example.com/plank.jpg", "target_angle": 180}
    ],
    "Low": [
        {"name": "Child's Pose", "image": "https://example.com/childs.jpg", "target_angle": 0},
        {"name": "Tree Pose", "image": "https://example.com/tree.jpg", "target_angle": 160}
    ]
}

def calculate_angle(a, b, c):
    a = np.array(a) # First point
    b = np.array(b) # Mid point
    c = np.array(c) # End point
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360-angle
    return angle

# --- UI ---
st.title("🧘 ZenStream: AI Yoga Guide")

col1, col2 = st.columns([1, 2])

with col1:
    energy = st.select_slider("Select Energy Level", options=["Low", "Medium", "High"])
    st.subheader("Your Sequence")
    sequence = YOGA_DB.get(energy if energy != "Medium" else "High")
    
    for pose_item in sequence:
        st.write(f"**{pose_item['name']}**")
        st.image(pose_item['image'], width=200)

    # Music Feature
    st.write("---")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") 
    st.caption("Background: Calming Zen Flute")

with col2:
    st.subheader("AI Alignment Camera")
    run = st.checkbox('Start Camera')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while run:
        ret, frame = camera.read()
        if not ret: break
        
        # Process Frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # Example: Correcting Knee Alignment in Warrior II (Left Knee)
            # Hip: 23, Knee: 25, Ankle: 27
            hip = [landmarks[23].x, landmarks[23].y]
            knee = [landmarks[25].x, landmarks[25].y]
            ankle = [landmarks[27].x, landmarks[27].y]
            
            angle = calculate_angle(hip, knee, ankle)
            
            # Visual Feedback
            color = (0, 255, 0) if 85 < angle < 95 else (255, 0, 0)
            cv2.putText(frame, f"Knee Angle: {int(angle)}°", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            if color == (255, 0, 0):
                cv2.putText(frame, "Adjust: Sink deeper!", (50, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        FRAME_WINDOW.image(frame)
    else:
        st.write("Camera is off. Check the box above to start.")
