import streamlit as st
import random
import pandas as pd
import time

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Yoga @ Work", page_icon="🧘", layout="wide")

# Custom CSS to make it look like a modern iPad App
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; }
    .stSelectbox, .stSlider { margin-bottom: 20px; }
    </style>
    """, unsafe_content_label=True)

# --- 2. THE ASANA LIBRARY ---
# Data structure: Name, Duration(m), Environments, Energy, Type
YOGA_DB = [
    {"name": "Box Breathing", "mins": 3, "env": ["Office", "WFH", "Home"], "energy": "Calming", "type": "Breathing"},
    {"name": "Seated Cat-Cow", "mins": 2, "env": ["Office", "WFH"], "energy": "Neutral", "type": "Exercise"},
    {"name": "Desk Plank", "mins": 2, "env": ["Office", "WFH"], "energy": "Energizing", "type": "Exercise"},
    {"name": "Sun Salutations", "mins": 8, "env": ["Home"], "energy": "Energizing", "type": "Exercise"},
    {"name": "Eye Palming", "mins": 2, "env": ["Office", "WFH", "Home"], "energy": "Calming", "type": "Meditation"},
    {"name": "Neck & Shoulder Release", "mins": 3, "env": ["Office", "WFH"], "energy": "Neutral", "type": "Exercise"},
    {"name": "Wrist Rolls", "mins": 2, "env": ["Office", "WFH"], "energy": "Neutral", "type": "Exercise"},
    {"name": "Warrior II", "mins": 5, "env": ["Home", "WFH"], "energy": "Energizing", "type": "Exercise"},
    {"name": "Tree Pose", "mins": 4, "env": ["WFH", "Home"], "energy": "Neutral", "type": "Exercise"},
    {"name": "Chair Spinal Twist", "mins": 3, "env": ["Office", "WFH"], "energy": "Calming", "type": "Exercise"},
    {"name": "Legs up the Wall", "mins": 5, "env": ["Home"], "energy": "Calming", "type": "Meditation"},
]

# --- 3. APP LOGIC ---
def generate_routine(target_mins, env, energy):
    # Filter library
    pool = [p for p in YOGA_DB if env in p['env'] and (p['energy'] == energy or p['energy'] == "Neutral")]
    
    selected = []
    total = 0
    random.shuffle(pool)
    
    for p in pool:
        if total + p['mins'] <= target_mins:
            selected.append(p)
            total += p['mins']
    return selected, total

# --- 4. UI LAYOUT ---
st.title("🧘 Corporate Zen: iPad Edition")
st.write("Smart yoga sequencing for busy professionals.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Settings")
    user_env = st.radio("Where are you?", ["Office", "WFH", "Home"])
    user_energy = st.select_slider("Target Energy", ["Calming", "Neutral", "Energizing"])
    user_time = st.slider("Minutes Available", 15, 60, 20)
    
    generate_btn = st.button("Generate My Session")

with col2:
    if generate_btn:
        routine, actual_time = generate_routine(user_time, user_env, user_energy)
        st.session_state['active_routine'] = routine
        
        st.success(f"Generated a {actual_time}-minute session!")
        
        for i, pose in enumerate(routine):
            with st.expander(f"{i+1}. {pose['name']} — {pose['mins']} mins"):
                st.write(f"**Focus:** {pose['type']}")
                st.write(f"**Ideal for:** {user_env} environment.")
                if st.button(f"Play {pose['name']}", key=f"btn_{i}"):
                    st.info(f"Focus on your breath during {pose['name']}...")
    
    elif 'active_routine' not in st.session_state:
        st.info("Set your preferences and click 'Generate' to begin.")

# --- 5. LIBRARY VIEW ---
st.divider()
if st.checkbox("Show Full Asana Library"):
    st.dataframe(pd.DataFrame(YOGA_DB), use_container_width=True)
