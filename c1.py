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
                "intensity": "RPE 3-4",
                "rest": "30-45 sec",
                "benefits": "Improves core control & lumbar stability",
                "target_areas": ["Core", "Stomach"],
                "rating": 4.5,
                "safety": "Keep a neutral spine and avoid excessive lumbar extension. Stop if you feel sharp back pain.",
                "contraindications": ["acute lower back pain", "recent spinal surgery", "severe disc herniation"],
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
                "intensity": "RPE 3-4",
                "rest": "30-45 sec",
                "benefits": "Strengthens rotator cuff & improves posture",
                "target_areas": ["Arms", "Back"],
                "rating": 4.2,
                "safety": "Move slowly and keep range small if you have shoulder pain. Stop if you experience pinching or sharp pain.",
                "contraindications": ["acute rotator cuff tear", "recent shoulder surgery", "severe shoulder impingement"],
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
                "reps": "6-8 reps / 15-30 sec holds",
                "intensity": "RPE 4-6",
                "rest": "30-60 sec",
                "benefits": "Opens chest & improves spinal flexibility",
                "target_areas": ["Back", "Chest"],
                "rating": 4.7,
                "safety": "Avoid if you have acute low back pain or recent spinal injury; perform a gentler cobra or supported bridge instead.",
                "contraindications": ["acute lower back pain", "recent spinal surgery"],
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
            "v_ups": {
                "name": "V-Ups",
                "type": "Core Strength",
                "equipment": ["Mat"],
                "level": "Intermediate",
                "reps": "AMRAP or 8-12 reps",
                "intensity": "RPE 6-7",
                "rest": "60-90 sec",
                "benefits": "Builds core strength & coordination",
                "target_areas": ["Core", "Stomach"],
                "rating": 4.3,
                "safety": "Keep neck neutral and avoid jerking; reduce ROM or do dead-bugs if you have low back issues.",
                "contraindications": ["acute lower back pain", "hernia"],
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
                "intensity": "RPE 4-5",
                "rest": "45-60 sec",
                "benefits": "Strengthens glutes & improves hip mobility",
                "target_areas": ["Glutes", "Legs"],
                "rating": 4.4,
                "safety": "Keep core braced and avoid excessive lumbar rotation. Reduce range if you feel back strain.",
                "contraindications": ["acute lower back pain"],
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
                "intensity": "70-75% 1RM",
                "rest": "90-120 sec",
                "benefits": "Builds overall leg strength and power",
                "target_areas": ["Legs", "Glutes", "Core"],
                "rating": 4.8,
                "safety": "Use proper set-up and avoid deep squats if you have knee pain; consider goblet squats as an alternative.",
                "contraindications": ["acute knee injury", "recent knee surgery", "severe lower back pain"],
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
                "intensity": "70-80% 1RM",
                "rest": "90-180 sec",
                "benefits": "Develops chest, shoulders, and triceps strength",
                "target_areas": ["Chest", "Arms", "Shoulders"],
                "rating": 4.7,
                "safety": "Use a spotter for heavy loads; avoid if you have uncontrolled shoulder pain—use dumbbell presses or push-ups as alternatives.",
                "contraindications": ["acute shoulder injury", "recent shoulder surgery"],
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

    def is_contraindicated(self, exercise: Dict, medical_conditions: List[str]) -> bool:
        """Return True if any of the user's medical conditions match the exercise contraindications"""
        if not medical_conditions or medical_conditions == ["None"]:
            return False
        ex_contras = [c.lower() for c in exercise.get("contraindications", [])]
        user_conds = [c.lower() for c in medical_conditions]
        # Simple substring match
        for uc in user_conds:
            for ec in ex_contras:
                if ec in uc or uc in ec:
                    return True
        return False
# ---------------- FITNESS ADVISOR CLASS ----------------
class FitnessAdvisor:
    def __init__(self, api_key: str, endpoint_url: str):
        self.api_key = api_key
        self.endpoint_url = endpoint_url
        self.exercise_db = ExerciseDatabase()
    
    def generate_personalized_response(self, user_profile: Dict) -> str:
        """Generate a highly personalized and casual response (robust parsing + debug on failure)"""
        try:
            # Create a comprehensive prompt based on user profile
            casual_greeting = f"Hey {user_profile['name']}! 😊"
            lifestyle_analysis = self.analyze_lifestyle(user_profile)
            prompt = f"""
            You are FriskaAI, a friendly and knowledgeable personal fitness coach. Start with a warm, casual greeting and create a highly personalized workout plan.

            Client Profile:
            - Name: {user_profile['name']}
            - Age: {user_profile['age']}, Gender: {user_profile['gender']}
            - Height: {user_profile.get('height_cm', user_profile.get('height','N/A'))}cm, Weight: {user_profile.get('weight_kg', user_profile.get('weight','N/A'))}kg
            - Fitness Level: {user_profile['fitness_level']}
            - Goals: {', '.join(user_profile.get('goals', []))}
            - Target Areas: {', '.join(user_profile.get('target_areas', []))}
            - Workout Location: {user_profile.get('workout_location', 'Home')}
            - Preferred Duration: {user_profile.get('workout_duration', '20-30 minutes')}
            - Activity Level: {user_profile.get('detailed_activity_level', 'Moderately Active')}
            - Current Exercise: {user_profile.get('current_exercise', 'No')}
            - Exercise Frequency: {user_profile.get('exercise_frequency', '0')} times/week
            - Preferred Weekly Frequency: {user_profile.get('preferred_weekly_frequency', '3')} days/week
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
            1. Start with a warm, casual greeting using their name.
            2. Provide a BRIEF PERSONALIZED ASSESSMENT (2-3 sentences) addressing their specific situation and goals.
            3. Prioritize content toward the user's selected health goals; explicitly include cardio if cardiovascular health is a goal.
            4. Give CUSTOMIZED RECOMMENDATIONS based on medical conditions, activity level, and goals.
            5. For each recommended exercise, provide a full tutorial in this format:
                - Exercise Name
                - Brief Benefit (1-2 sentences)
                - How to do it: step-by-step guide, clearly numbered as Step 1, Step 2, Step 3, etc.
                - Sets/Reps or Duration
                - Intensity (use RPE 1–10 for bodyweight/mobility exercises; use %1RM or a % range for weighted exercises when appropriate)
                - Rest between sets (give recommended rest in seconds/minutes and link to training goal)
                - Safety Cue: 1-2 sentences (explicit safety advice and what to watch for)
                - Contraindications: list medical conditions that would make this exercise inappropriate (if any)
            6. If an exercise would be contraindicated for the user's listed medical conditions, do NOT recommend it; instead suggest a safer alternative and explain why.
            7. Specify whether the plan is for a single session or a weekly routine, and provide a short weekly frequency schedule when applicable.
            8. For bodyweight strength exercises where the user's exact strength is unknown, recommend AMRAP or scaled alternatives rather than a fixed rep target.
            9. Use ACE-style rest guidance and tailor rest to each exercise and the user's level.
            10. Avoid overclaiming clinical benefits; when in doubt recommend referral to a clinician/physiotherapist.
            11. Be specific about progression and include short notes on when/how to progress intensity or load.
            12. Keep tone conversational, encouraging, and safety-first. Include safety cues and when to stop or seek medical advice.

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

            # call the API with a timeout
            resp = requests.post(self.endpoint_url, headers=headers, json=payload, timeout=30)

            # on success try multiple extraction patterns
            if resp.status_code == 200:
                try:
                    result = resp.json()
                except Exception:
                    # Not JSON - return raw text for debugging
                    return resp.text or "Empty response from model (non-JSON)."

                # Common patterns: choices[].message.content, choices[].text, output, result['choices'][0]['message']['content']
                content = None
                if isinstance(result, dict):
                    choices = result.get("choices")
                    if choices and len(choices) > 0:
                        first = choices[0]
                        if isinstance(first, dict):
                            # OpenAI-style chat completion
                            msg = first.get("message")
                            if msg and isinstance(msg, dict) and msg.get("content"):
                                content = msg["content"]
                            # older/other variants
                            elif first.get("text"):
                                content = first.get("text")
                            elif first.get("message") and isinstance(first.get("message"), str):
                                content = first.get("message")
                    # other vendor keys
                    if not content:
                        if "output" in result:
                            content = result["output"]
                        elif "data" in result:
                            content = json.dumps(result["data"])
                # fallback to stringified JSON
                if not content:
                    try:
                        content = json.dumps(result, indent=2)
                    except Exception:
                        content = str(result)
                return content
            else:
                # return status and body to make debugging visible in UI
                text = resp.text
                return f"Error generating response: status={resp.status_code} body={text}"

        except requests.exceptions.Timeout:
            return "Error: The API request timed out."
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

    # New: units selection for height & weight
    height_unit = st.selectbox("Height unit", ["cm", "ft + in"], index=0)
    if height_unit == "cm":
        height_cm_input = st.number_input("Height (cm)", 140, 220, 170)
    else:
        col_h1, col_h2 = st.columns([1,1])
        with col_h1:
            height_ft = st.number_input("Height (ft)", 4, 7, 5)
        with col_h2:
            height_in = st.number_input("Height (in)", 0, 11, 7)
        height_cm_input = int(height_ft * 30.48 + height_in * 2.54)

with col2:
    weight_unit = st.selectbox("Weight unit", ["kg", "lbs"], index=0)
    if weight_unit == "kg":
        weight_kg_input = st.number_input("Weight (kg)", 40, 150, 70)
    else:
        weight_lbs = st.number_input("Weight (lbs)", 88, 330, 154)
        weight_kg_input = round(weight_lbs * 0.453592, 1)

    fitness_level = st.selectbox("How would you describe your current fitness level?", ["Beginner", "Intermediate", "Advanced"])

# Calculate BMI (displayed when inputs available)
try:
    bmi = round(weight_kg_input / ((height_cm_input/100)**2), 1)
    st.info(f"Calculated BMI: {bmi} kg/m²")
except Exception:
    bmi = None

# Activity Level and Exercise History
st.markdown("#### 🏃‍♂️ Activity Level & Exercise History")
col3, col4 = st.columns(2)
with col3:
    detailed_activity_level = st.selectbox("Activity Level", 
        ["Sedentary", "Lightly Active", "Moderately Active", "Active"])
    sitting_time = st.number_input("Average Sitting Time (hrs/day)", 0, 16, 8)
    
    # Weight change (amount + timeframe)
    weight_change_type = st.selectbox("Recent Weight Change", ["No Change", "Gained Weight", "Lost Weight"])
    if weight_change_type != "No Change":
        weight_change_amount = st.number_input(f"How much weight? (kg)", 0.5, 50.0, 2.0)
        weight_change_timeframe = st.selectbox("Timeframe for weight change", ["Within 3 months", "Within 6 months", "Within 9 months", "Over 1 year"])
        weight_change = f"{weight_change_type}: {weight_change_amount} kg ({weight_change_timeframe})"
    else:
        weight_change = "No Change"

with col4:
    current_exercise = st.selectbox("Do you currently exercise?", ["Yes", "No"])
    if current_exercise == "Yes":
        exercise_type = st.text_input("Type of Physical Activity", placeholder="e.g., walking, swimming, yoga")
        # Clarified label: past/existing frequency
        exercise_frequency = st.number_input("Past exercise frequency (times/week)", 0, 14, 3)
        # New: total workout experience duration
        workout_experience_years = st.selectbox("Total workout experience", ["<1 year", "1-2 years", "2-4 years", "4+ years"])
    else:
        exercise_type = "None"
        exercise_frequency = 0
        workout_experience_years = "<1 year"
    
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
    ["Weight Management", "Health Condition Management", "Vital Monitoring", "Fitness Improvement", 
     "Nutritional Monitoring", "Improve Cardiovascular Fitness", "Build Muscular Strength", 
     "Rehabilitation & Corrective Exercise", "Reduce Stress", "Improve Flexibility & Mobility", "Improve Posture & Balance",
     "Increase Energy & Sleep Quality", "Manage/Prevent Lifestyle Disorders", "Improve Hormonal Balance", 
     "Reduce Back Pain", "Feel Better / Look Better", "Stop Smoking"])
# Barriers to goals (recommended addition)
st.markdown("**Any barriers that make it difficult to achieve your fitness goals?**")
barriers = st.multiselect("Select barriers (if any):", [
    "Difficulty maintaining consistency", "Limited access to reliable information", "Lack of structure or guidance",
    "Time constraints", "Challenges tracking progress", "Limited accountability/motivation", "Other"
])
if "Other" in barriers:
    barriers_other = st.text_input("If other, please specify:")

# Target Areas
target_areas = st.multiselect("Which body parts or training focus do you want?", 
    ["Full Body", "Upper Body", "Lower Body", "Anterior (front)", "Posterior (back)", "Core & Abs", "Back", 
     "Chest", "Arms", "Legs", "Glutes", "Shoulders"])

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
    workout_location = st.selectbox("Preferred Location / Gym Type", ["Home", "Garage gym", "Small gym", "Large gym", "Outdoor"])

    # Equipment based on location (expanded categories)
    if workout_location == "Home":
        available_equipment_options = ["None", "Mat", "Dumbbells", "Resistance Bands", "Kettlebell", "Chair", "Wall", "Pull-up Bar", "Towel Roll", "Small Cushion"]
    elif workout_location == "Garage gym":
        available_equipment_options = ["Mat", "Barbell", "Dumbbells", "Squat Rack", "Bench", "Pull-up Bar", "Kettlebell", "Resistance Bands"]
    elif workout_location == "Small gym":
        available_equipment_options = ["Mat", "Dumbbells", "Cable Machine", "Treadmill", "Stationary Bike", "Bench", "Pull-up Bar", "Leg Press"]
    else:  # Large gym or Outdoor
        available_equipment_options = ["Mat", "Barbell", "Dumbbells", "Cable Machine", "Treadmill", "Stationary Bike", "Squat Rack", "Bench", "Pull-up Bar", "Leg Press", "Smith Machine", "Resistance Machines", "Jump Rope", "Bodyweight Only"]
    equipment = st.multiselect("Available Equipment", available_equipment_options)

    workout_frequency = st.selectbox("Preferred workout days per week (desired)", [1,2,3,4,5,6,7], index=2)
    
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
                "height_cm": height_cm_input,
                "weight_kg": weight_kg_input,
                "bmi": bmi,
                "fitness_level": fitness_level,
                "detailed_activity_level": detailed_activity_level,
                "sitting_time": sitting_time,
                "weight_change": weight_change,
                "current_exercise": current_exercise,
                "exercise_type": exercise_type,
                "exercise_frequency": exercise_frequency,  # past frequency
                "workout_experience_years": workout_experience_years,
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
                "workout_duration": workout_duration,
                "preferred_weekly_frequency": workout_frequency,  # desired frequency
                "barriers": barriers
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
                excluded_exercises = []
                user_medical_conditions = user_profile.get("medical_conditions", ["None"])
                for ex_name in exercise_names:
                    for key, ex in fitness_advisor.exercise_db.exercises.items():
                        if ex['name'] == ex_name:
                            # filter out contraindicated exercises
                            if fitness_advisor.exercise_db.is_contraindicated(ex, user_medical_conditions):
                                excluded_exercises.append(ex['name'])
                                continue
                            exercise_details.append((key, ex))

                if excluded_exercises:
                    st.warning("Some exercises were excluded because they may be unsuitable for your medical conditions: " + ", ".join(excluded_exercises))
                    st.info("Where possible, the plan includes safer alternatives. If unsure, consult your clinician or physiotherapist.")

                if exercise_details:
                    for i, (key, exercise) in enumerate(exercise_details):
                        st.markdown(f"""
<div style='background:#e3f2fd;border-radius:10px;padding:18px;margin-bottom:18px;box-shadow:0 2px 8px #bdbdbd;'>
  <h3 style='color:#1565c0;margin-bottom:8px;'>⭐ {exercise['name']} <span style='font-size:0.8em;color:#888;'>(Rating: {exercise.get('rating','N/A')}/5)</span></h3>
  <b>Benefit:</b> {exercise['benefits']}<br>
  <b>Type:</b> {exercise['type']}<br>
  <b>Equipment:</b> {', '.join(exercise.get('equipment', []))}<br>
  <b>Level:</b> {exercise.get('level', 'N/A')}<br>
  <b>Target Areas:</b> {', '.join(exercise.get('target_areas', []))}<br>
  <b>Sets/Reps:</b> {exercise.get('reps', 'N/A')}<br>
  <b>Intensity:</b> {exercise.get('intensity', 'RPE guidance will be provided in plan')}<br>
  <b>Rest between sets:</b> {exercise.get('rest', 'See plan guidelines')}<br>
  <b>Safety:</b> {exercise.get('safety', 'Follow general safety guidelines: move slowly, breathe, stop on sharp pain, seek medical advice if unsure.')}<br>
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
