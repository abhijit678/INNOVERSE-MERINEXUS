import pandas as pd

class RecommendationEngine:
    def __init__(self):
        self.strategies = {
            "Visual Learner": [
                "Use mind maps for concept connection",
                "Color-code study materials",
                "Watch video tutorials before reading",
                "Draw diagrams for math problems"
            ],
            "Analytical Thinker": [
                "Break down problems into structured steps",
                "Focus on understanding the 'why' behind formulas",
                "Review systematic mistakes",
                "Use logic puzzles for warm-ups"
            ],
            "Kinesthetic Learner": [
                "Use interactive simulations",
                "Take frequent short breaks (Pomodoro)",
                "Pace while memorizing facts",
                "Use hands-on experiments"
            ],
            "Social Collaborator": [
                "Join a peer study group",
                "Teach concepts to a classmate",
                "Participate in group discussions",
                "Use flashcards with a partner"
            ],
            "Mixed Learner": [
                "Alternate between reading and interactive practice",
                "Set varied daily study formats",
                "Combine visual and auditory inputs",
                "Maintain a balanced study schedule"
            ]
        }
        
    def get_pattern_strategies(self):
        return self.strategies
        
    def get_priority(self, student):
        acc = student.get('accuracy', 0) * 100
        if acc < 60:
            return "🔴 Critical"
        elif acc < 72:
            return "🟡 Moderate"
        else:
            return "🟢 On Track"
            
    def get_recommendation(self, student):
        pattern = student.get('pattern', 'Mixed Learner')
        strats = self.strategies.get(pattern, self.strategies["Mixed Learner"])
        # Simple context aware: If accuracy is very low, pick the first strategy which is usually foundational
        if student.get('accuracy', 0) < 0.6:
            return strats[0]
        # If retry rate is high, pick second
        elif student.get('retry_rate', 0) > 0.5:
            return strats[1]
        else:
            return strats[2]
            
    def get_all_recommendations(self, students_df):
        recs = []
        for _, student in students_df.iterrows():
            priority = self.get_priority(student)
            recs.append({
                "Student": student['name'],
                "Pattern": student['pattern'],
                "Accuracy%": f"{student['accuracy']*100:.1f}%",
                "Retry Rate%": f"{student['retry_rate']*100:.1f}%",
                "Priority": priority,
                "Top Recommendation": self.get_recommendation(student)
            })
            
        df = pd.DataFrame(recs)
        
        # Sort by priority: Critical -> Moderate -> On Track
        priority_map = {"🔴 Critical": 0, "🟡 Moderate": 1, "🟢 On Track": 2}
        df['sort_key'] = df['Priority'].map(priority_map)
        df = df.sort_values('sort_key').drop('sort_key', axis=1)
        
        return df

if __name__ == "__main__":
    from analyzer import CognitiveAnalyzer
    from data_generator import generate_mock_data
    s, l = generate_mock_data()
    a = CognitiveAnalyzer()
    res = a.analyze_all(s, l)
    eng = RecommendationEngine()
    print(eng.get_all_recommendations(res).head())
