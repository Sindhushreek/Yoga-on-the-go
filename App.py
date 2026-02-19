import streamlit as st
import time

st.set_page_config(page_title="Yoga on the Go", page_icon="🧘‍♀️")

st.title("🧘‍♀️ Yoga on the Go")
st.markdown("### *Quick Desk-Side Resets*")

# --- DATA: Names and Step-by-Step Instructions ---
yoga_data = {
    "Desk Yoga (Seated)": {
        "pose": "Seated Spinal Twist",
        "steps": [
            "1. Sit tall with feet flat on the floor.",
            "2. Place your right hand on your left knee.",
            "3. Gently twist toward the left, looking over your shoulder.",
            "4. Hold, breathe, then switch sides."
        ],
        "focus": "Relieves lower back and spine tension."
    },
    "Work From Home (Mat)": {
        "pose": "Cat-Cow Stretch",
        "steps": [
            "1. Get on your hands and knees (Tabletop).",
            "2. Inhale: Drop your belly and look up (Cow).",
            "3. Exhale: Round your back and tuck your chin (Cat).",
            "4. Move fluidly with your breath."
        ],
        "focus": "Improves posture and spinal flexibility."
    },
    "The 'Coder' Stretch": {
        "pose": "Wrist & Forearm Release",
        "steps": [
            "1. Extend one arm forward, palm facing up.",
            "2. Use the other hand to gently pull your fingers back.",
            "3. Switch to palm facing down and repeat.",
            "4. Shake out your hands afterward."
        ],
        "focus": "Prevents wrist strain from typing."
    }
}

# --- SIDEBAR ---
st.sidebar.header("Settings")
category = st.sidebar.selectbox("Select a stretch:", list(yoga_data.keys()))
hold_time = st.sidebar.slider("Select duration (seconds):", 10, 60, 20)

# --- MAIN CONTENT ---
selected = yoga_data[category]

st.subheader(f"Focus: {selected['pose']}")
st.write(f"✨ *{selected['focus']}*")

# Instructions UI
st.write("---")
for step in selected['steps']:
    st.write(step)
st.write("---")

# --- INTERACTIVE TIMER ---
if st.button(f"⏱️ Start {hold_time}s Focus Timer"):
    # Placeholders for the countdown
    progress_bar = st.progress(0)
    timer_text = st.empty()
    
    for remaining in range(hold_time, -1, -1):
        # Update progress and text
        percent = 1.0 - (remaining / hold_time)
        progress_bar.progress(percent)
        timer_text.metric("Breathe...", f"{remaining}s")
        time.sleep(1)
    
    timer_text.success("Great job! Ready to get back to work?")
    st.balloons()

st.divider()
st.caption("Developed by sindhushreek | Built on iPad 📱")
