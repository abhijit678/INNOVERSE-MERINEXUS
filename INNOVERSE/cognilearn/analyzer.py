import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class CognitiveAnalyzer:
    def __init__(self):
        # 5 patterns using normalized metrics [0-1]
        # Metrics: [accuracy, avg_response_time, retry_rate, mistake_freq, retention_score]
        # To make it simpler, we just use the 4 extracted + retention
        # Note: we want to match profiles. We define ideal normalized profiles (ranges 0-1)
        # Visual: high retention (0.8), medium accuracy(0.6), medium speed(0.5 obj -> time is inverted or just raw time normalized? we'll use raw normalized)
        # However, let's explicitly define profiles for these 5 metrics: 
        # ['accuracy', 'avg_response_time', 'retry_rate', 'mistake_freq', 'retention']
        
        self.profiles = {
            "Visual Learner": np.array([0.6, 0.5, 0.4, 0.4, 0.9]),     # high retention, med acc/speed
            "Analytical Thinker": np.array([0.9, 0.8, 0.2, 0.1, 0.8]), # high acc, slow (high resp time), low retry
            "Kinesthetic Learner": np.array([0.5, 0.2, 0.9, 0.5, 0.6]),# med acc, fast, high retry
            "Social Collaborator": np.array([0.7, 0.6, 0.6, 0.3, 0.8]),# consistent, high retention
            "Mixed Learner": np.array([0.5, 0.5, 0.5, 0.5, 0.5])       # balanced
        }

    def _estimate_retention(self, student_logs):
        # late-session accuracy (e.g. sessions 15-20)
        late_sessions = student_logs[student_logs['session'] >= 15]
        if len(late_sessions) == 0:
            return 0.5
        return late_sessions['correct'].mean()

    def analyze_all(self, students_df, logs_df):
        metrics = []
        
        for idx, student in students_df.iterrows():
            sid = student['student_id']
            s_logs = logs_df[logs_df['student_id'] == sid]
            
            if len(s_logs) == 0:
                continue
                
            accuracy = s_logs['correct'].mean()
            avg_response_time = s_logs['response_time'].mean()
            retry_rate = s_logs['retried'].mean()
            mistake_freq = 1.0 - accuracy  # complementary to accuracy
            sessions_completed = s_logs['session'].nunique()
            retention_score = self._estimate_retention(s_logs)
            
            metrics.append({
                'student_id': sid,
                'name': student['name'],
                'grade': student['grade'],
                'accuracy': accuracy,
                'avg_response_time': avg_response_time,
                'retry_rate': retry_rate,
                'mistake_freq': mistake_freq,
                'sessions_completed': sessions_completed,
                'retention': retention_score
            })
            
        metrics_df = pd.DataFrame(metrics)
        
        # Normalize metrics for classification using Euclidean distance
        features = ['accuracy', 'avg_response_time', 'retry_rate', 'mistake_freq', 'retention']
        scaler = MinMaxScaler()
        normalized_data = scaler.fit_transform(metrics_df[features])
        
        # Classification
        patterns = []
        for row in normalized_data:
            distances = {
                pattern: np.linalg.norm(row - profile)
                for pattern, profile in self.profiles.items()
            }
            best_pattern = min(distances, key=distances.get)
            patterns.append(best_pattern)
            
        metrics_df['pattern'] = patterns
        
        # We also want to keep the normalized data around if helpful, 
        # but let's just return metrics_df with everything.
        # Add the normalized columns for easy radar plotting
        for i, f in enumerate(features):
            metrics_df[f"{f}_norm"] = normalized_data[:, i]
            
        return metrics_df

if __name__ == "__main__":
    from data_generator import generate_mock_data
    s, l = generate_mock_data()
    analyzer = CognitiveAnalyzer()
    res = analyzer.analyze_all(s, l)
    print(res.head())
