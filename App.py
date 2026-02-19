import streamlit as st
import time

# Page Configuration
st.set_page_config(page_title="Yoga on the Go", page_icon="🧘‍♀️", layout="centered")

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_headers=True)

st.title("🧘‍♀️ Yoga on the Go")
st.write("### *Your Corporate Wellness Companion*")

# --- DATA ---
yoga_library = {
    "Desk Yoga (Seated)": {
        "pose": "Seated Spinal Twist",
        "steps": ["Sit upright, feet flat.", "Place right hand on left knee.", "Twist gently to the left.", "Breathe deeply for 20s."],
        "benefit": "Relieves lower back pain."
    },
    "Work From Home (Mat)": {
        "pose": "Cobra Pose",
        "steps": ["Lie on your stomach.", "Place hands under shoulders.", "Gently lift your chest.", "Keep shoulders down."],
        "benefit": "Opens chest and lungs."
    },
    "Neck & Shoulder Reset": {
        "pose": "Eagle Arms",
        "steps": ["Cross arms at elbows.", "Intertwine forearms.", "Lift elbows to shoulder height.", "Feel the upper back stretch."],
        "benefit": "Fixes 'Tech Neck' stiffness."
    }
}

# --- SIDEBAR SETTINGS ---
st.sidebar.header("Configure Session")
choice = st.sidebar.selectbox("Select your environment:", list(yoga_library.keys()))
duration = st.sidebar.slider("Stretch duration (seconds):", 10, 60, 20)

# --- MAIN UI ---
selected = yoga_library[choice]

st.subheader(f"Current Pose: {selected['pose']}")
st.success(f"🎯 **Benefit:** {selected['benefit']}")

# Display Instructions
for i, step in enumerate(selected['steps']):
    st.write(f"**{i+1}.** {step}")

st.divider()

# --- TIMER LOGIC ---
if st.button(f"Start {duration}s Timer"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(duration, -1, -1):
        # Update progress
        progress = 100 - int((i / duration) * 100)
        progress_bar.progress(progress)
        
        # Update text
        status_text.metric("Breathe deeply...", f"{i}s")
        time.sleep(1)
        
    st.balloons()
    status_text.success("✨ Great job! You're recharged.")

st.sidebar.info("Tip: Drink some water after your stretch!")
