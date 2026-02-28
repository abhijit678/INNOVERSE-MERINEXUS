import pandas as pd
import numpy as np
import random

def generate_mock_data():
    np.random.seed(42)
    random.seed(42)

    subjects = ["Algebra", "Geometry", "Statistics", "Logic", "Calculus"]
    archetypes = ["Visual Learner", "Analytical Thinker", "Kinesthetic Learner", "Social Collaborator", "Mixed Learner"]
    
    first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Oliver", "Isabella", "Elijah", "Sophia", "William",
                   "Mia", "James", "Charlotte", "Benjamin", "Amelia", "Lucas", "Harper", "Henry", "Evelyn", "Alexander",
                   "Abigail", "Mason", "Emily", "Michael", "Elizabeth", "Ethan", "Mila", "Daniel", "Ella", "Jacob",
                   "Avery", "Logan", "Sofia", "Jackson", "Camila", "Levi", "Aria", "Sebastian", "Scarlett", "Mateo",
                   "Victoria", "Jack", "Madison", "Owen", "Luna", "Theodore", "Grace", "Aiden", "Chloe", "Samuel"]

    # 1. Generate Students
    students = []
    for i in range(50):
        student_id = f"STU{i+1:03d}"
        name = first_names[i]
        grade = np.random.randint(6, 13)
        base_archetype = np.random.choice(archetypes)
        students.append({
            "student_id": student_id,
            "name": name,
            "grade": grade,
            "base_archetype": base_archetype
        })
    students_df = pd.DataFrame(students)

    # 2. Generate Logs
    logs = []
    for student in students:
        student_id = student['student_id']
        base_arch = student['base_archetype']
        
        for session in range(1, 21):
            num_questions = np.random.randint(8, 16)
            
            for q_idx in range(num_questions):
                subject = np.random.choice(subjects)
                
                # Learning curve logic base
                # Session 1..20 maps to increasing accuracy and decreasing time
                progress_factor = session / 20.0
                
                # Base probability of being correct increases over sessions
                base_accuracy_prob = 0.5 + (0.35 * progress_factor)
                
                # Modify by archetype slightly
                if base_arch == "Analytical Thinker":
                    base_accuracy_prob += 0.05
                elif base_arch == "Kinesthetic Learner" and session > 10:
                    base_accuracy_prob += 0.1  # Fast improvement later
                    
                base_accuracy_prob = min(0.98, max(0.1, base_accuracy_prob))
                
                correct = 1 if np.random.rand() < base_accuracy_prob else 0
                
                # Base response time decreases over sessions
                base_time = 45.0 - (15.0 * progress_factor) # seconds
                
                if base_arch == "Analytical Thinker":
                    base_time += 10.0 # Methodical
                elif base_arch == "Kinesthetic Learner":
                    base_time -= 5.0 # Fast
                    
                response_time = max(5.0, np.random.normal(base_time, 5.0))
                
                # Retry mapping
                retry_prob = 0.1
                if correct == 0:
                    retry_prob = 0.6
                if base_arch == "Kinesthetic Learner":
                    retry_prob += 0.2
                    
                retried = 1 if np.random.rand() < retry_prob else 0
                
                # Calculate score for the question
                score = 10 if correct else (5 if retried else 0)
                
                logs.append({
                    "student_id": student_id,
                    "session": session,
                    "subject": subject,
                    "response_time": response_time,
                    "correct": correct,
                    "retried": retried,
                    "score": score
                })
                
    logs_df = pd.DataFrame(logs)
    
    return students_df, logs_df

if __name__ == "__main__":
    st, lg = generate_mock_data()
    print(f"Generated {len(st)} students and {len(lg)} logs.")
