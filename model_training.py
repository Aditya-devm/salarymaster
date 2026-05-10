import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# Set seed for reproducibility
np.random.seed(42)

def generate_data(n=1000):
    roles = ['Software Engineer', 'Data Scientist', 'Manager', 'Analyst', 'HR']
    education_levels = ['Bachelor\'s', 'Master\'s', 'PhD']
    
    data = []
    for _ in range(n):
        role = np.random.choice(roles)
        edu = np.random.choice(education_levels)
        exp = np.random.randint(0, 30)
        
        # Base salary based on role (in INR)
        base = {
            'Software Engineer': 800000,
            'Data Scientist': 1000000,
            'Manager': 1500000,
            'Analyst': 600000,
            'HR': 500000
        }[role]
        
        # Multipliers
        edu_mult = {'Bachelor\'s': 1.0, 'Master\'s': 1.3, 'PhD': 1.6}[edu]
        exp_mult = (1.12 ** exp) # 12% compound growth per year
        
        salary = base * edu_mult * exp_mult
        # Add some noise
        salary += np.random.normal(0, 5000)
        
        data.append([role, edu, exp, round(salary, -2)])
        
    return pd.DataFrame(data, columns=['Role', 'Education', 'Experience', 'Salary'])

def train_model():
    print("Loading dataset from 'salary_data.csv'...")
    if not os.path.exists('salary_data.csv'):
        print("Error: 'salary_data.csv' not found. Generating default data...")
        df = generate_data(2000)
    else:
        df = pd.read_csv('salary_data.csv')
    
    # Preprocessing
    le_role = LabelEncoder()
    le_edu = LabelEncoder()
    
    df['Role_Encoded'] = le_role.fit_transform(df['Role'])
    df['Education_Encoded'] = le_edu.fit_transform(df['Education'])
    
    X = df[['Role_Encoded', 'Education_Encoded', 'Experience']]
    y = df['Salary']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluation
    score = model.score(X_test, y_test)
    print(f"Model R^2 Score: {score:.4f}")
    
    # Save model and encoders
    artifacts = {
        'model': model,
        'le_role': le_role,
        'le_edu': le_edu
    }
    
    with open('salary_model.pkl', 'wb') as f:
        pickle.dump(artifacts, f)
    
    print("Model and artifacts saved to 'salary_model.pkl'")
    df.to_csv('salary_data.csv', index=False)
    print("Dataset saved to 'salary_data.csv'")

if __name__ == "__main__":
    train_model()
