import streamlit as st
import random

# App Config
st.set_page_config(page_title="Zen Flow Generator", page_icon="🧘")

st.title("🧘 Zen Flow Generator")
st.write("Find your balance. Tell me your energy level, and I'll suggest a flow.")

# Data
poses = {
    "Low Energy": ["Child’s Pose (Balasana)", "Legs Up the Wall (Viparita Karani)", "Cat-Cow (Marjaryasana)"],
    "Need Focus": ["Tree Pose (Vrikshasana)", "Warrior II (Virabhadrasana II)", "Eagle Pose (Garudasana)"],
    "High Energy": ["Sun Salutation A (Surya Namaskar)", "Crow Pose (Bakasana)", "Wheel Pose (Urdhva Dhanurasana)"]
}

quotes = [
    "“Yoga is the journey of the self, through the self, to the self.”",
    "“Inhale the future, exhale the past.”",
    "“The pose begins when you want to leave it.”"
]

# User Input
energy = st.select_slider(
    "How is your energy today?",
    options=["Low Energy", "Need Focus", "High Energy"]
)

if st.button("Generate My Flow"):
    pose = random.choice(poses[energy])
    quote = random.choice(quotes)
    
    st.divider()
    st.subheader(f"Today's Recommended Pose: **{pose}**")
    st.info(f"✨ **Daily Intent:** {quote}")
    
    # Simple breathing guide
    st.write("---")
    st.write("### Quick Breath Work")
    st.write("Inhale for 4s... Hold for 4s... Exhale for 4s...")
    st.balloons()
