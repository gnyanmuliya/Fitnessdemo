import streamlit as st
import requests
import json
import os
import pandas as pd
from typing import Dict, List, Optional

# ---------------- CONFIG ----------------
API_KEY = st.secrets["API_KEY"]
ENDPOINT_URL = st.secrets["ENDPOINT_URL"]

st.set_page_config(page_title="FriskaAi - Smart Fitness Advisor", layout="wide")
st.title("🏋️‍♂️ FriskaAi - Your Personal Fitness Advisor")

# Welcome message with casual chat
st.markdown("""
### 👋 Hey there! Welcome to FriskaAi! 

I'm excited to help you create a personalized fitness plan that actually works for YOU! 
Let's start by getting to know you better - think of this as a friendly chat with your personal trainer. 
Don't worry, this will only take a few minutes, and I promise it'll be worth it! 💪
""")

# ---------------- MEDICAL CONDITIONS LIST ----------------
MEDICAL_CONDITIONS = [
    "None", "Acanthosis Nigricans", "Addison's Disease", "Alzheimer's Disease", 
    "Ankylosing Spondylitis", "Anxiety Disorders", "Arrhythmias", "Asthma", 
    "Bipolar Disorder", "Bladder Cancer", "Brain Tumors", "Breast Cancer", 
    "Bronchitis", "Celiac Disease", "Cervical Cancer", "Cervical Spondylosis", 
    "Chickenpox", "Chikungunya", "Chronic Obstructive Pulmonary Disease (COPD)", 
    "Cirrhosis", "Colorectal Cancer", "Constipation", "Coronary Artery Disease (CAD)", 
    "COVID-19", "Cushing's Syndrome", "Deep Vein Thrombosis (DVT)", "Dementia", 
    "Dengue", "Depression", "Diabetic Ketoacidosis (DKA) Recovery", "Diarrheal Diseases", 
    "Disc Herniation", "Eating Disorders Recovery", "Encephalitis", "Epilepsy (Ketogenic Diet)", 
    "Fibromyalgia", "Fractures", "G6PD Deficiency", "Gallstones", 
    "Gastroesophageal Reflux Disease (GERD)", "Gastritis", "Glomerulonephritis", 
    "Gout", "Heart Failure", "Hepatitis", "Hepatitis E", "HIV/AIDS", "Hyperthyroidism", 
    "Hypertension", "Hypoglycemia", "Hypothyroidism", "Inflammatory Bowel Disease (Flare-up)", 
    "Inflammatory Bowel Disease (Remission)", "Influenza", "Insomnia", 
    "Interstitial Lung Disease", "Irritable Bowel Syndrome (IBS)", "Lactose Intolerance", 
    "Leukemia", "Low Back Pain", "Lung Cancer", "Lymphoma", "Malaria", "Measles", 
    "Meningitis", "Menopause", "Metabolic Syndrome", "Migraine", "Multiple Sclerosis", 
    "Myocardial Infarction (Heart Attack) Recovery", "Neuropathy", "Obesity", 
    "Obsessive Compulsive Disorder (OCD)", "Osteoarthritis", "Osteoporosis", 
    "Ovarian Cancer", "Pancreatic Cancer", "Parkinson's Disease", "Peptic Ulcer Disease", 
    "Perimenopause", "Peripheral Artery Disease", "Pneumonia", 
    "Polycystic Ovary Syndrome (PCOS)", "Post-Traumatic Stress Disorder (PTSD)", 
    "Prostate Cancer", "Prostate Enlargement (BPH)", "Pulmonary Embolism", 
    "Pulmonary Hypertension", "Pyelonephritis (Kidney Infection)", "Rheumatic Heart Disease", 
    "Rheumatoid Arthritis", "Schizophrenia", "Sexually Transmitted Infections (STIs)", 
    "Sickle Cell Disease", "Sleep Apnea", "Stevens-Johnson Syndrome (SJS) Recovery", 
    "Stomach Cancer", "Stroke Recovery", "Substance Use Disorder Recovery", 
    "Thalassemia", "Tuberculosis (TB)", "Type 1 Diabetes Mellitus", 
    "Type 2 Diabetes Mellitus", "Typhoid Fever", "Urinary Tract Infection (UTI)", 
    "Vitiligo", "Other"
]

# ---------------- EXERCISE DATABASE ----------------
class ExerciseDatabase:
    def __init__(self):
        self.exercises = {
            "supine_dead_bug": {
                "name": "Supine Dead Bug",
                "type": "Core Stability",
                "equipment": ["Mat"],
                "level": "Beginner",
                "reps": "10-12 reps/side",
                "benefits": "Improves core control & lumbar stability",
                "target_areas": ["Core", "Stomach"],
                "rating": 4.5,
                "steps": [
                    "Lie on your back with knees bent at 90 degrees",
                    "Extend opposite arm and leg slowly",
                    "Hold for 2-3 seconds",
                    "Return to starting position",
                    "Repeat on other side"
                ],
                "demo_video": "Core Exercise_ Dead Bug 1.mp4",
                "common_mistakes": ["Arching back", "Moving too fast", "Not engaging core"]
            },
            "supine_rotator_cuff": {
                "name": "Supine Rotator Cuff",
                "type": "Shoulder Stability",
                "equipment": ["Mat", "Small Cushion"],
                "level": "Beginner",
                "reps": "10-12 reps/arm",
                "benefits": "Strengthens rotator cuff & improves posture",
                "target_areas": ["Arms", "Back"],
                "rating": 4.2,
                "steps": [
                    "Lie on your side with arm at 90 degrees",
                    "Place cushion under head for support",
                    "Rotate forearm up slowly",
                    "Hold briefly, then lower",
                    "Complete all reps before switching sides"
                ],
                "demo_video": "4 Supine Rotator Cuff Movements 1.mp4",
                "common_mistakes": ["Using momentum", "Rotating too far", "Not supporting head"]
            },
            "upward_facing_dog": {
                "name": "Upward Facing Dog",
                "type": "Spinal Extension",
                "equipment": ["Mat"],
                "level": "Intermediate",
                "reps": "6-8 reps",
                "benefits": "Opens chest & improves spinal flexibility",
                "target_areas": ["Back", "Chest"],
                "rating": 4.7,
                "steps": [
                    "Start in plank position",
                    "Lower hips while lifting chest",
                    "Straighten arms and lift thighs off ground",
                    "Hold for 15-30 seconds",
                    "Lower back to starting position"
                ],
                "demo_video": "How to Do Upward-Facing Dog Pose in Yoga 1.mp4",
                "common_mistakes": ["Sinking shoulders", "Overarching neck", "Not engaging legs"]
            },
            "vertical_toe_touches": {
                "name": "Vertical Toe Touches",
                "type": "Core Flexibility",
                "equipment": ["Mat"],
                "level": "Beginner",
                "reps": "10-12 reps",
                "benefits": "Improves core strength & hamstring flexibility",
                "target_areas": ["Core", "Legs"],
                "rating": 4.0,
                "steps": [
                    "Lie on back with legs straight up",
                    "Reach hands toward toes",
                    "Lift shoulder blades off ground",
                    "Touch toes if possible",
                    "Lower slowly and repeat"
                ],
                "demo_video": "Vertical Toe Touch Bodyweight Training Exercise 1.mp4",
                "common_mistakes": ["Using neck to pull up", "Jerky movements", "Not engaging core"]
            },
            "v_ups": {
                "name": "V-Ups",
                "type": "Core Strength",
                "equipment": ["Mat"],
                "level": "Intermediate",
                "reps": "8-12 reps",
                "benefits": "Builds core strength & coordination",
                "target_areas": ["Core", "Stomach"],
                "rating": 4.3,
                "steps": [
                    "Lie flat with arms overhead",
                    "Simultaneously lift legs and torso",
                    "Try to touch toes at the top",
                    "Lower slowly with control",
                    "Keep core engaged throughout"
                ],
                "demo_video": "v_ups_demo.mp4",
                "common_mistakes": ["Using momentum", "Not controlling descent", "Straining neck"]
            },
            "dirty_dog": {
                "name": "Dirty Dog",
                "type": "Glute Strength",
                "equipment": ["Mat"],
                "level": "Beginner",
                "reps": "10-12 reps/side",
                "benefits": "Strengthens glutes & improves hip mobility",
                "target_areas": ["Glutes", "Legs"],
                "rating": 4.4,
                "steps": [
                    "Start on hands and knees",
                    "Keep knee bent and lift leg to side",
                    "Lift until thigh is parallel to ground",
                    "Lower slowly without touching ground",
                    "Complete all reps before switching"
                ],
                "demo_video": "dirty_dog_demo.mp4",
                "common_mistakes": ["Lifting too high", "Rotating hips", "Not keeping core stable"]
            }
        }
        
        # Add gym-specific exercises
        self.gym_exercises = {
            "barbell_squat": {
                "name": "Barbell Squat",
                "type": "Compound Strength",
                "equipment": ["Barbell", "Squat Rack"],
                "level": "Intermediate",
                "reps": "8-12 reps",
                "benefits": "Builds overall leg strength and power",
                "target_areas": ["Legs", "Glutes", "Core"],
                "rating": 4.8,
                "steps": [
                    "Position bar on upper traps",
                    "Stand with feet shoulder-width apart",
                    "Lower by pushing hips back and bending knees",
                    "Descend until thighs parallel to floor",
                    "Drive through heels to return to start"
                ],
                "demo_video": "barbell_squat_demo.mp4",
                "common_mistakes": ["Knee valgus", "Forward lean", "Partial range of motion"]
            },
            "bench_press": {
                "name": "Bench Press",
                "type": "Upper Body Strength",
                "equipment": ["Barbell", "Bench"],
                "level": "Intermediate",
                "reps": "6-10 reps",
                "benefits": "Develops chest, shoulders, and triceps strength",
                "target_areas": ["Chest", "Arms", "Shoulders"],
                "rating": 4.7,
                "steps": [
                    "Lie flat on bench with feet planted",
                    "Grip bar slightly wider than shoulders",
                    "Lower bar to chest with control",
                    "Press bar up in straight line",
                    "Lock out arms at the top"
                ],
                "demo_video": "bench_press_demo.mp4",
                "common_mistakes": ["Bouncing off chest", "Uneven grip", "Arched back"]
            }
        }
    
    def get_exercises_by_target_area(self, target_areas: List[str], workout_location: str = "Home") -> Dict:
        """Filter exercises by target body areas and location"""
        all_exercises = self.exercises.copy()
        if workout_location == "Gym":
            all_exercises.update(self.gym_exercises)
            
        filtered = {}
        for key, exercise in all_exercises.items():
            if any(area in exercise["target_areas"] for area in target_areas):
                filtered[key] = exercise
        return filtered
    
    def get_exercises_by_equipment(self, available_equipment: List[str], workout_location: str = "Home") -> Dict:
        """Filter exercises by available equipment and location"""
        all_exercises = self.exercises.copy()
        if workout_location == "Gym":
            all_exercises.update(self.gym_exercises)
            
        filtered = {}
        for key, exercise in all_exercises.items():
            if workout_location == "Home":
                # For home, only include if equipment is available (don't default to Mat)
                if all(equip in available_equipment for equip in exercise["equipment"]):
                    filtered[key] = exercise
            else:
                # For gym, assume most equipment is available
                filtered[key] = exercise
        return filtered

# ---------------- FITNESS ADVISOR CLASS ----------------
class FitnessAdvisor:
    def __init__(self, api_key: str, endpoint_url: str):
        self.api_key = api_key
        self.endpoint_url = endpoint_url
        self.exercise_db = ExerciseDatabase()
    
    def generate_personalized_response(self, user_profile: Dict) -> str:
        """Generate a highly personalized and casual response"""
        try:
            # Create a comprehensive prompt based on user profile
            casual_greeting = f"Hey {user_profile['name']}! 😊"
            
            # Analyze user's lifestyle
            lifestyle_analysis = self.analyze_lifestyle(user_profile)
            
            # Create detailed prompt
            prompt = f"""
            You are FriskaAI, a friendly and knowledgeable personal fitness coach. Start with a warm, casual greeting and create a highly personalized workout plan.

            Client Profile:
            - Name: {user_profile['name']}
            - Age: {user_profile['age']}, Gender: {user_profile['gender']}
            - Height: {user_profile['height']}cm, Weight: {user_profile['weight']}kg
            - Fitness Level: {user_profile['fitness_level']}
            - Goals: {', '.join(user_profile.get('goals', []))}
            - Target Areas: {', '.join(user_profile.get('target_areas', []))}
            - Workout Location: {user_profile.get('workout_location', 'Home')}
            - Preferred Duration: {user_profile.get('workout_duration', '20-30 minutes')}
            - Activity Level: {user_profile.get('detailed_activity_level', 'Moderately Active')}
            - Current Exercise: {user_profile.get('current_exercise', 'No')}
            - Exercise Frequency: {user_profile.get('exercise_frequency', '0')} times/week
            - Daily Steps: {user_profile.get('daily_steps', 'Not specified')}
            - Sitting Time: {user_profile.get('sitting_time', 'Not specified')} hours/day
            - Medical Conditions: {', '.join(user_profile.get('medical_conditions', ['None']))}
            - Specific Health Issues: {user_profile.get('physical_issues', 'None')}
            - Smoking: {user_profile.get('smoking', 'No')}
            - Alcohol: {user_profile.get('alcohol_consumption', 'No')}
            - Equipment Available: {', '.join(user_profile.get('equipment', []))}
            - Preferred Exercise Time: {user_profile.get('preferred_time', 'Not specified')}
            - Weight Change: {user_profile.get('weight_change', 'None')}

            Instructions:
            1. Start with a warm, casual greeting using their name
            2. Provide a BRIEF PERSONALIZED ASSESSMENT (2-3 sentences) addressing their specific situation
            3. Give CUSTOMIZED RECOMMENDATIONS based on their medical conditions, activity level, and goals
            4. For each recommended exercise, provide a full tutorial in this format:
                - Exercise Name
                - Brief Benefit (1-2 sentences)
                - How to do it: step-by-step guide, clearly numbered as Step 1, Step 2, Step 3, etc. (each step on a new line)
                - Sets/Reps or Duration
            5. Be specific about why certain exercises are chosen for THEIR situation
            6. Address any medical concerns or limitations mentioned
            7. Make it conversational and encouraging
            8. Include safety considerations if they have any medical conditions
            9. Suggest progression based on their current fitness level

            Make the response feel like it's written specifically for {user_profile['name']} based on all their inputs, not generic advice.
            """
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "mistral-small",
                "messages": [
                    {"role": "system", "content": "You are FriskaAI, a friendly, knowledgeable personal fitness coach who creates highly personalized, encouraging workout plans with a casual, supportive tone."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1500
            }
            
            response = requests.post(self.endpoint_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Error generating response: {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def analyze_lifestyle(self, profile: Dict) -> str:
        """Analyze user's lifestyle for better recommendations"""
        analysis = []
        
        sitting_time = profile.get('sitting_time', 0)
        if sitting_time and int(sitting_time) > 8:
            analysis.append("high_sedentary")
        
        if profile.get('smoking') == 'Yes':
            analysis.append("smoker")
        
        current_exercise = profile.get('current_exercise', 'No')
        if current_exercise == 'No':
            analysis.append("inactive")
        
        return analysis

# Initialize fitness advisor
fitness_advisor = FitnessAdvisor(API_KEY, ENDPOINT_URL)

# Helper: find a matching video file in the local video/ folder
def find_video_file(filename: str) -> Optional[str]:
    """Return a path to a matching file in ./video/ or None if not found."""
    if not filename:
        return None
    video_dir = os.path.join(os.path.dirname(__file__), "video") if '__file__' in globals() else os.path.join(".", "video")
    if not os.path.isdir(video_dir):
        return None

    target = filename.lower().replace("_", " ").strip()
    candidate = os.path.join(video_dir, filename)
    if os.path.exists(candidate):
        return candidate

    for f in os.listdir(video_dir):
        if target in f.lower() or f.lower() in target:
            return os.path.join(video_dir, f)

    return None

# ---------------- ENHANCED STREAMLIT FORM ----------------
st.markdown("### 📋 Let's Get To Know You Better!")
st.markdown("*Don't worry, this information helps me create the perfect workout plan just for you!*")

# Personal Information
st.markdown("#### 👤 Basic Information")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("What's your name?*", placeholder="Enter your full name")
    age = st.number_input("How old are you?*", 16, 80, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

with col2:
    height = st.number_input("Height (cm)", 140, 220, 170)
    weight = st.number_input("Weight (kg)", 40, 150, 70)
    fitness_level = st.selectbox("How would you describe your current fitness level?", ["Beginner", "Intermediate", "Advanced"])

# Activity Level and Exercise History
st.markdown("#### 🏃‍♂️ Activity Level & Exercise History")
col3, col4 = st.columns(2)
with col3:
    detailed_activity_level = st.selectbox("Activity Level", 
        ["Sedentary", "Lightly Active", "Moderately Active", "Active", "Super Active"])
    sitting_time = st.number_input("Average Sitting Time (hrs/day)", 0, 16, 8)
    
    # Weight change
    weight_change_type = st.selectbox("Recent Weight Change", ["No Change", "Gained Weight", "Lost Weight"])
    if weight_change_type != "No Change":
        weight_change_amount = st.number_input(f"How much weight? (kg)", 0.5, 50.0, 2.0)
        weight_change = f"{weight_change_type}: {weight_change_amount} kg"
    else:
        weight_change = "No Change"

with col4:
    current_exercise = st.selectbox("Do you currently exercise?", ["Yes", "No"])
    if current_exercise == "Yes":
        exercise_type = st.text_input("Type of Physical Activity", placeholder="e.g., walking, swimming, yoga")
        exercise_frequency = st.number_input("Exercise Frequency (times/week)", 0, 14, 3)
    else:
        exercise_type = "None"
        exercise_frequency = 0
    
    daily_steps = st.number_input("Daily Step Count (if known)", 0, 50000, 5000)
    preferred_time = st.selectbox("Preferred Exercise Time", ["Morning", "Afternoon", "Evening", "No Preference"])

# Lifestyle Habits
st.markdown("#### 🚬 Lifestyle Habits")
col5, col6 = st.columns(2)
with col5:
    smoking = st.selectbox("Do you smoke or vape?", ["No", "Yes"])
    if smoking == "Yes":
        smoking_frequency = st.selectbox("Frequency", ["1 pack/day", "½ pack/day", "5-10 singles/day", "Occasional"])
        smoking_type = st.selectbox("Type", ["Cigarettes", "Vape", "Cigars", "Pipe"])
        previous_smoker = st.selectbox("Previous smoker?", ["No", "Yes"])
        if previous_smoker == "Yes":
            quit_year = st.number_input("Quit Year", 1990, 2024, 2020)

with col6:
    alcohol_consumption = st.selectbox("Do you consume alcohol?", ["No", "Occasionally", "Regularly"])
    if alcohol_consumption != "No":
        alcohol_frequency = st.text_input("Frequency", placeholder="e.g., 2-3 times per week")

# Health & Wellness Goals
st.markdown("#### 🎯 Health & Wellness Goals")
goals = st.multiselect("Please select all that apply:", 
    ["Weight Management", "Disease Management", "Vital Monitoring", "Fitness Improvement", 
     "Nutritional Monitoring", "Improve Cardiovascular Fitness", "Build Muscular Strength", 
     "Injury Rehab", "Reduce Stress", "Improve Flexibility", "Reduce Back Pain", 
     "Lower Cholesterol/Blood Pressure", "Stop Smoking", "Feel Better / Look Better"])

# Target Areas
target_areas = st.multiselect("Which body parts do you want to focus on?", 
    ["Full Body", "Core", "Stomach", "Back", "Chest", "Arms", "Legs", "Glutes", "Shoulders"])

# Medical Conditions (only two prompts: medical and physical limitations)
st.markdown("#### 🏥 Medical Conditions")
has_medical_conditions = st.selectbox("Do you have any existing medical conditions?", ["No", "Yes"])

medical_conditions = []
if has_medical_conditions == "Yes":
    selected_conditions = st.multiselect("Select your medical conditions:", MEDICAL_CONDITIONS[1:])  # Exclude "None"
    if "Other" in selected_conditions:
        custom_condition = st.text_input("Please specify other condition:")
        if custom_condition:
            selected_conditions.remove("Other")
            selected_conditions.append(custom_condition)
    medical_conditions = selected_conditions

# Physical/Functional Limitations
physical_issues = st.text_area("Any physical limitations, injuries, or pain? (e.g., Lower back pain, knee problems, shoulder injury, etc.)")


# Equipment & Environment
st.markdown("#### 🏠 Workout Setup")
col7, col8 = st.columns(2)
with col7:
    workout_location = st.selectbox("Preferred Location", ["Home", "Gym", "Outdoor"])

    # Equipment based on location
    if workout_location == "Home":
        available_equipment_options = ["None", "Mat", "Dumbbells", "Resistance Bands", "Small Cushion", 
                                     "Towel Roll", "Chair", "Wall", "Kettlebell", "Pull-up Bar"]
    elif workout_location == "Gym":
        available_equipment_options = ["Mat", "Barbell", "Dumbbells", "Cable Machine", "Treadmill", 
                                     "Stationary Bike", "Squat Rack", "Bench", "Pull-up Bar", 
                                     "Leg Press", "Smith Machine", "Resistance Machines", "Towel Roll", "Chair", "Wall", "Small Cushion", "Kettlebell"]
    else:  # Outdoor
        available_equipment_options = ["None", "Resistance Bands", "Mat", "Jump Rope", 
                                     "Bodyweight Only"]
    equipment = st.multiselect("Available Equipment", available_equipment_options)

with col8:
    workout_duration = st.selectbox("Preferred Workout Duration", 
        ["15-20 minutes", "20-30 minutes", "30-45 minutes", "45-60 minutes"])

# Medications (Optional)
with st.expander("💊 Medications (Optional)"):
    on_medications = st.selectbox("Are you currently on any medications?", ["No", "Yes"])
    if on_medications == "Yes":
        medication_categories = st.multiselect("Select medication categories (if applicable):", [
            "Diuretics", "Cardiovascular", "Beta Blockers", "NSAIDs/Anti-inflammatories",
            "Vasodilators", "Cholesterol", "Diabetes/Insulin", "Calcium Channel Blockers", "Other"
        ])

# Generate Plan Button
if st.button("🚀 Generate My Personalized Workout Plan", type="primary"):
    if not name or not goals:
        st.error("Please fill in your name and select at least one fitness goal.")
    else:
        with st.spinner("Creating your personalized workout plan... This might take a moment! ⏳"):
            # Combine all medical information (now just medical_conditions)
            all_medical_conditions = medical_conditions if medical_conditions else ["None"]

            user_profile = {
                "name": name,
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight,
                "fitness_level": fitness_level,
                "detailed_activity_level": detailed_activity_level,
                "sitting_time": sitting_time,
                "weight_change": weight_change,
                "current_exercise": current_exercise,
                "exercise_type": exercise_type,
                "exercise_frequency": exercise_frequency,
                "daily_steps": daily_steps,
                "preferred_time": preferred_time,
                "smoking": smoking,
                "alcohol_consumption": alcohol_consumption,
                "goals": goals,
                "target_areas": target_areas,
                "medical_conditions": all_medical_conditions,
                "physical_issues": physical_issues,
                "equipment": equipment,
                "workout_location": workout_location,
                "workout_duration": workout_duration
            }
            
            # Store in session state
            st.session_state.user_profile = user_profile
            
            # Generate personalized response
            try:
                workout_plan = fitness_advisor.generate_personalized_response(user_profile)
                st.session_state['last_workout_plan'] = workout_plan

                st.success("✅ Your personalized workout plan is ready!")
                st.markdown("---")
                
                # Format the response nicely
                st.markdown("## 🏋️‍♂️ Your Personalized Fitness Plan")
                
                # Split response into sections for better formatting
                if "BRIEF PERSONALIZED ASSESSMENT" in workout_plan or "assessment" in workout_plan.lower():
                    sections = workout_plan.split('\n\n')
                    for i, section in enumerate(sections):
                        if i == 0:  # First section is usually greeting
                            st.markdown(f"### 👋 {section}")
                        elif "assessment" in section.lower():
                            st.markdown(f"### 📊 {section}")
                        elif "recommendation" in section.lower():
                            st.markdown(f"### 💡 {section}")
                        else:
                            st.markdown(section)
                else:
                    st.markdown(workout_plan)
                
                # Show recommended exercises from AI response only, formatted impressively
                st.markdown("---")

                st.markdown("<h2 style='color:#2e7d32;'>💪 Recommended Exercise Demo</h2>", unsafe_allow_html=True)

                # --- Inline Exercise GIF Demo Section ---

                import re
                # --- Local GIFs from Kaggle dataset ---
                kaggle_gif_dir = os.path.join("archive", "exercisedb_v1_sample", "gifs_360x360")
                kaggle_json_path = os.path.join("archive", "exercisedb_v1_sample", "exercises.json")
                kaggle_gif_map = {}
                try:
                    with open(kaggle_json_path, "r", encoding="utf-8") as f:
                        kaggle_exercises = json.load(f)
                    for ex in kaggle_exercises:
                        name = ex["name"].strip().lower()
                        gif_file = ex["gifUrl"]
                        kaggle_gif_map[name] = gif_file
                except Exception as e:
                    st.warning(f"Could not load local exercise GIFs: {e}")
                    kaggle_gif_map = {}

                # Improved: fuzzy match exercise names from AI response to Kaggle dataset

                from difflib import get_close_matches
                demo_exercise_names = []
                # (Debug output of AI response removed)
                ai_text = re.sub(r'[^a-zA-Z0-9\s]', '', workout_plan).lower()
                #st.write("Processed AI text for matching:", ai_text)
                ai_words = set(ai_text.split())
                kaggle_names = list(kaggle_gif_map.keys())
                match_debug = []
                for ex_name in kaggle_names:
                    if ex_name in ai_text:
                        demo_exercise_names.append(ex_name)
                        match_debug.append(f"Direct match: {ex_name}")
                    else:
                        ex_words = set(ex_name.split())
                        if len(ex_words & ai_words) / max(1, len(ex_words)) >= 0.6:
                            demo_exercise_names.append(ex_name)
                            match_debug.append(f"Fuzzy word match: {ex_name}")
                        else:
                            close = get_close_matches(ex_name, [ai_text], n=1, cutoff=0.8)
                            if close:
                                demo_exercise_names.append(ex_name)
                                match_debug.append(f"Difflib match: {ex_name}")
                demo_exercise_names = list(dict.fromkeys(demo_exercise_names))
                st.write("Matched exercise names for GIFs:", demo_exercise_names)
                st.write("Match debug info:", match_debug)

                if demo_exercise_names:
                    st.markdown("### 💡 Suggested Exercise Animations (Local)")
                    cols = st.columns(len(demo_exercise_names))
                    for i, ex_name in enumerate(demo_exercise_names):
                        gif_file = kaggle_gif_map.get(ex_name)
                        gif_path = os.path.join(kaggle_gif_dir, gif_file) if gif_file else None
                        # On Windows, Streamlit may need the absolute path
                        if gif_path and not os.path.isabs(gif_path):
                            gif_path = os.path.abspath(gif_path)
                        with cols[i]:
                            st.markdown(f"**{ex_name.title()}**")
                            if gif_path and os.path.exists(gif_path):
                                # Read GIF as bytes and display
                                with open(gif_path, "rb") as gif_file:
                                    gif_bytes = gif_file.read()
                                st.image(gif_bytes, use_container_width=True)
                            else:
                                st.info("No local GIF available.")

                
                exercise_names = []
                # Improved extraction: match exercise names even if AI adds extra whitespace, punctuation, or uses partial names
                ai_text = re.sub(r'[^a-zA-Z0-9\s]', '', workout_plan).lower()
                for ex in fitness_advisor.exercise_db.exercises.values():
                    ex_name = ex['name'].lower()
                    if ex_name in ai_text:
                        exercise_names.append(ex['name'])
                exercise_names = list(dict.fromkeys(exercise_names))

                exercise_details = []
                for ex_name in exercise_names:
                    for key, ex in fitness_advisor.exercise_db.exercises.items():
                        if ex['name'] == ex_name:
                            exercise_details.append((key, ex))

                if exercise_details:
                    for i, (key, exercise) in enumerate(exercise_details):
                        st.markdown(f"""
<div style='background:#e3f2fd;border-radius:10px;padding:18px;margin-bottom:18px;box-shadow:0 2px 8px #bdbdbd;'>
  <h3 style='color:#1565c0;margin-bottom:8px;'>⭐ {exercise['name']} <span style='font-size:0.8em;color:#888;'>(Rating: {exercise['rating']}/5)</span></h3>
  <b>Benefit:</b> {exercise['benefits']}<br>
  <b>Type:</b> {exercise['type']}<br>
  <b>Equipment:</b> {', '.join(exercise['equipment'])}<br>
  <b>Level:</b> {exercise['level']}<br>
  <b>Target Areas:</b> {', '.join(exercise['target_areas'])}<br>
  <b>Sets/Reps:</b> {exercise['reps']}<br>
  <div style='margin-top:10px;margin-bottom:10px;'><b>📝 Step-by-Step Guide:</b></div>
  <ol style='margin-left:20px;'>
    {''.join([f'<li>{step}</li>' for step in exercise['steps']])}
  </ol>
  <details style='margin-top:10px;'>
    <summary style='font-weight:bold;color:#1976d2;'>View More (Mistakes & Pro Tips)</summary>
    <div style='margin-top:8px;'><b>⚠️ Common Mistakes to Avoid:</b><ul>{''.join([f'<li>{mistake}</li>' for mistake in exercise['common_mistakes']])}</ul></div>
    <div style='margin-top:8px;'><b>🎯 Pro Tips:</b>
      <ul>
        <li>Start slowly and focus on proper form</li>
        <li>Breathe steadily throughout the movement</li>
        <li>Stop if you feel any pain or discomfort</li>
      </ul>
    </div>
  </details>
</div>
""", unsafe_allow_html=True)
                else:
                    st.info("No exercises found in the AI response. Try again or check the response format.")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


# Reset the flag
if 'plan_just_generated' in st.session_state:
    del st.session_state['plan_just_generated']

# Footer
st.markdown("---")
st.markdown("### 📱 FriskaAI - Your Smart Fitness Companion")
st.markdown("*Always consult with a healthcare provider before starting any new exercise program.*")
st.markdown("💪 **Remember:** Consistency is key! Start small, stay committed, and celebrate your progress!")