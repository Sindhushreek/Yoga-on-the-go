import random

class YogaPose:
    def __init__(self, name, duration, environment, energy, category):
        self.name = name
        self.duration = duration  # in minutes
        self.environment = environment  # ['Office', 'WFH', 'Home']
        self.energy = energy  # ['Calming', 'Energizing', 'Neutral']
        self.category = category  # ['Breathing', 'Exercise', 'Meditation']

# 1. Setup a Sample Library
pose_library = [
    YogaPose("Box Breathing", 2, ["Office", "WFH", "Home"], "Calming", "Breathing"),
    YogaPose("Seated Cat-Cow", 3, ["Office", "WFH"], "Neutral", "Exercise"),
    YogaPose("Desk Plank", 2, ["Office", "WFH"], "Energizing", "Exercise"),
    YogaPose("Standing Sun Salutation", 5, ["Home"], "Energizing", "Exercise"),
    YogaPose("Eye Palming", 2, ["Office", "WFH", "Home"], "Calming", "Exercise"),
    YogaPose("Neck Rolls", 2, ["Office", "WFH"], "Neutral", "Exercise"),
    YogaPose("Quick Mindfulness", 3, ["Office", "WFH", "Home"], "Calming", "Meditation"),
    YogaPose("Warrior II", 4, ["Home", "WFH"], "Energizing", "Exercise"),
    YogaPose("Wrist Stretches", 2, ["Office", "WFH"], "Neutral", "Exercise"),
]

def generate_sequence(total_minutes, env, energy_goal):
    # Filter library based on user environment and energy
    eligible_poses = [
        p for p in pose_library 
        if env in p.environment and (p.energy == energy_goal or p.energy == "Neutral")
    ]
    
    sequence = []
    current_time = 0
    
    # Simple logic: keep adding poses until the time is reached
    random.shuffle(eligible_poses)
    
    for pose in eligible_poses:
        if current_time + pose.duration <= total_minutes:
            sequence.append(pose)
            current_time += pose.duration
            
    return sequence, current_time

# --- EXECUTION ---
user_time = 15  # 15 to 60 mins
user_env = "Office"
user_energy = "Energizing"

my_session, final_time = generate_sequence(user_time, user_env, user_energy)

print(f"--- Your {final_time}-minute {user_env} Yoga Session ({user_energy}) ---")
for i, pose in enumerate(my_session, 1):
    print(f"{i}. {pose.name} ({pose.duration} mins) - [{pose.category}]")
