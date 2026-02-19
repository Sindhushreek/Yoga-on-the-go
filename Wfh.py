import streamlit as st
import random
import time
import pandas as pd

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Corporate Zen", page_icon="🧘", layout="wide")

# Fixed the argument to 'unsafe_allow_html' to avoid the TypeError
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        border-radius: 12px; 
        height: 3em; 
        background-color: #4CAF50; 
        color: white;
        font-weight: bold;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE EXTENDED ASANA LIBRARY ---
YOGA_DB = [
    {"name": "Box Breathing", "mins": 4, "env": ["Office", "WFH", "Home"], "energy": "Calming", "type": "Breathing", "desc": "Inhale 4s, Hold 4s, Exhale 4s, Hold 4s."},
    {"name": "Seated Cat-Cow", "mins": 3, "env": ["Office", "WFH"], "energy": "Neutral", "type": "Exercise", "desc": "Arch and round your back while sitting to release the spine."},
    {"name": "Desk Plank", "mins": 2, "env": ["Office", "WFH"], "energy": "Energizing", "type": "Exercise", "desc": "Hands on desk, step back into a plank. Hold core tight."},
    {"name": "Sun Salutations", "mins": 10, "env": ["Home"], "energy": "Energizing", "type": "Exercise", "desc": "Flowing sequence of standing and floor poses."},
    {"name": "Eye Palming", "mins": 2, "env": ["Office", "WFH", "Home"], "energy": "Calming", "type": "Meditation", "desc": "Rub hands to create heat, then cup over closed eyes."},
    {"name": "Neck & Shoulder Release", "mins": 4, "env": ["Office", "WFH"], "energy": "Neutral", "type": "Exercise", "desc": "Gently tilt head side to side and roll shoulders back."},
    {"name": "Wrist Stretches", "mins": 2, "env": ["Office", "WFH"], "energy": "Neutral", "type": "Exercise", "desc": "Extend arm, pull fingers back gently to counter typing strain."},
    {"name": "Warrior II", "mins": 5, "env": ["Home", "WFH"], "energy": "Energizing", "type": "Exercise", "desc": "Wide stance, arms out, look over front hand. Builds strength."},
    {"name": "Tree Pose", "mins": 4, "env": ["WFH", "Home"], "energy": "Neutral", "type": "Exercise", "desc": "Balance on one leg to improve focus and calm the mind."},
    {"name": "Chair Spinal Twist", "mins": 3, "env": ["Office", "WFH"], "energy": "Calming", "type": "Exercise", "desc": "Sit sideways, use the chair back to gently twist the torso."},
    {"name": "Legs up the Wall", "mins": 6, "env": ["Home"], "energy": "Calming", "type": "Meditation", "desc": "Lie on back with legs vertical against a wall. Great for circulation."},
    {"name": "Alternate Nostril Breathing", "mins": 5, "env": ["Office", "WFH", "Home"], "energy": "Neutral", "type": "Breathing", "desc": "Balance brain hemispheres by breathing through one nostril at a time."}
]

# --- 3. CORE LOGIC ---
def generate_sequence(target_mins, env, energy):
    # Priority 1: Match Environment AND Energy
    # Priority 2: Match Environment AND Neutral energy (as fillers)
    pool = [p for p in YOGA_DB if env in p['env'] and (p['energy'] == energy or p['energy'] == "Neutral")]
    
    sequence = []
    total_time = 0
    random.shuffle(pool)
    
    for pose in pool:
        if total_time + pose['mins'] <= target_mins:
            sequence.append(pose)
            total_time += pose['mins']
            
    return sequence, total_time

# --- 4. APP INTERFACE ---
st.title("🧘 Corporate Zen")
st.caption("Custom yoga sequences for the modern workspace.")

# Use Sidebar for Settings on iPad to save screen real estate
with st.sidebar:
    st.header("Session Settings")
    u_env = st.selectbox("Current Setting", ["Office", "WFH", "Home"])
    u_energy = st.select_slider("Target Energy", options=["Calming", "Neutral", "Energizing"])
    u_time = st.slider("Duration (Minutes)", 15, 60, 15)
    
    st.divider()
    gen_button = st.button("✨ Generate Sequence")
    
    if st.button("🤫 Meeting Mode (2m Quick Fix)"):
        quick = random.choice([p for p in YOGA_DB if u_env in p['env']])
        st.info(f"Quick Fix: **{quick['name']}**\n\n{quick['desc']}")

# Main App Area
if gen_button or 'active_seq' in st.session_state:
    if gen_button:
        res, actual_t = generate_sequence(u_time, u_env, u_energy)
        st.session_state['active_seq'] = res
        st.session_state['total_t'] = actual_t

    seq = st.session_state.get('active_seq', [])
    actual_t = st.session_state.get('total_t', 0)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"Your {actual_t}-Minute {u_energy} Routine")
        for i, p in enumerate(seq):
            with st.expander(f"{i+1}. {p['name']} ({p['mins']} min)"):
                st.write(f"**Type:** {p['type']}")
                st.write(p['desc'])
                if st.button(f"Start {p['name']} Timer", key=f"timer_{i}"):
                    # Visual Timer
                    progress_text = f"Practicing {p['name']}..."
                    my_bar = st.progress(0, text=progress_text)
                    for percent_complete in range(100):
                        time.sleep(p['mins'] * 0.1) # Speeding up for demo; use (p['mins']*0.6) for real seconds
                        my_bar.progress(percent_complete + 1, text=progress_text)
                    st.balloons()

    with col2:
        st.subheader("Summary")
        st.markdown(f"""
        <div class="metric-card">
        <b>Environment:</b> {u_env}<br>
        <b>Intensity:</b> {u_energy}<br>
        <b>Poses:</b> {len(seq)}
        </div>
        """, unsafe_allow_html=True)
        
        st.image("https://img.freepik.com/free-vector/hand-drawn-yoga-pose-collection_23-2148850608.jpg", caption="Focus on your form.")

else:
    # Onboarding screen
    st.info("👈 Use the sidebar to set your preferences and generate your first sequence!")
    

# --- 5. LIBRARY VIEW ---
with st.expander("📚 View Full Asana Library"):
    df = pd.DataFrame(YOGA_DB)
    st.dataframe(df.drop(columns=['env']), use_container_width=True)
