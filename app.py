from flask import Flask, render_template, request, jsonify
import pickle
import os
import numpy as np
from cv_parser import extract_features
import tempfile

app = Flask(__name__)

# Load Model Artifacts
def load_artifacts():
    model_path = os.path.join(os.path.dirname(__file__), 'salary_model.pkl')
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    return None

artifacts = load_artifacts()

if not artifacts:
    print("WARNING: Model not found! Please run 'model_training.py' first.")

model = artifacts.get('model') if artifacts else None
le_role = artifacts.get('le_role') if artifacts else None
le_edu = artifacts.get('le_edu') if artifacts else None

@app.route('/')
def index():
    try:
        roles = sorted(list(le_role.classes_)) if le_role else []
        educations = sorted(list(le_edu.classes_)) if le_edu else []
        return render_template('index.html', roles=roles, educations=educations)
    except Exception as e:
        print(f"Error in index route: {e}")
        return render_template('index.html', roles=[], educations=[])

@app.route('/parse_cv', methods=['POST'])
def parse_cv():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})

    if file:
        # Create a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        try:
            features = extract_features(tmp_path)
            # Clean up temp file
            os.remove(tmp_path)
            
            if features:
                return jsonify({'success': True, 'features': features})
            else:
                return jsonify({'success': False, 'error': 'Failed to extract features'})
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            return jsonify({'success': False, 'error': str(e)})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    role = data.get('role')
    education = data.get('education')
    experience = data.get('experience', 0)

    if not model or not le_role or not le_edu:
        return jsonify({'success': False, 'error': 'Model not initialized'})

    try:
        role_enc = le_role.transform([role])[0]
        edu_enc = le_edu.transform([education])[0]
        input_data = np.array([[role_enc, edu_enc, experience]])
        
        prediction = model.predict(input_data)[0]
        
        if prediction >= 100000:
            salary_display = f"₹{prediction/100000:,.2f} Lakhs"
        else:
            salary_display = f"₹{prediction:,.0f}"
            
        return jsonify({
            'success': True, 
            'salary': float(prediction), 
            'salary_display': salary_display
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
