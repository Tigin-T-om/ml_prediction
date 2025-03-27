from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, accuracy_score
import joblib

app = Flask(__name__)

# Load available models and scalers
try:
    house_model = joblib.load('house_price_model.pkl')
    house_scaler = joblib.load('house_price_scaler.pkl')
    salary_model = joblib.load('employee_salary_model.pkl')
    salary_scaler = joblib.load('salary_scaler.pkl')
    diabetes_model = joblib.load('diabetes_model.pkl')
    diabetes_scaler = joblib.load('diabetes_scaler.pkl')
    fruit_model = joblib.load('fruit_knn_model.pkl')
    fruit_scaler = joblib.load('fruit_knn_scaler.pkl')
    temp_model = joblib.load('temperature_prediction_model.pkl')
    temp_scaler = joblib.load('temperature_prediction_scaler.pkl')
    temp_poly = joblib.load('temperature_prediction_poly.pkl')
except FileNotFoundError as e:
    print(f"Error loading model files: {str(e)}")
    print("Please ensure all model files are present in the Prediction directory")
    exit(1)

# Calculate accuracies for available models
try:
    house_data = pd.read_csv('house_prediction_slr.csv')
    X_house = house_data.iloc[:, 0:1].values.astype(np.float64)  # Square Footage
    y_house = house_data.iloc[:, 1:2].values.astype(np.float64)  # Price
    X_house_scaled = house_scaler.transform(X_house)
    house_accuracy = r2_score(y_house, house_model.predict(X_house_scaled))

    salary_data = pd.read_csv('employee_salaries.csv')
    X_salary = salary_data[['YearsExperience', 'EducationLevel', 'Certifications']].values.astype(np.float64)
    y_salary = salary_data['Salary'].values.astype(np.float64)
    X_salary_scaled = salary_scaler.transform(X_salary)
    salary_accuracy = r2_score(y_salary, salary_model.predict(X_salary_scaled))

    diabetes_data = pd.read_csv('diabetes_balanced_data.csv')
    X_diabetes = diabetes_data[['Age', 'BMI', 'Glucose', 'BloodPressure']].values.astype(np.float64)
    y_diabetes = diabetes_data['Diabetes'].values.astype(np.float64)
    X_diabetes_scaled = diabetes_scaler.transform(X_diabetes)
    diabetes_accuracy = r2_score(y_diabetes, diabetes_model.predict(X_diabetes_scaled))

    fruit_data = pd.read_csv('fruit_dataset.csv')
    X_fruit = fruit_data[['Weight', 'Size', 'Color_Score']].values.astype(np.float64)
    y_fruit = fruit_data['Label']
    X_fruit_scaled = fruit_scaler.transform(X_fruit)
    fruit_accuracy = accuracy_score(y_fruit, fruit_model.predict(X_fruit_scaled))

    # Calculate temperature model accuracy
    temp_data = pd.read_csv('temperature_prediction_data.csv')
    X_temp = temp_data[['Day', 'Humidity', 'Wind_Speed', 'Pressure']].values.astype(np.float64)
    y_temp = temp_data['Temperature'].values.astype(np.float64)
    X_temp_scaled = temp_scaler.transform(X_temp)
    X_temp_poly = temp_poly.transform(X_temp_scaled)
    temp_accuracy = r2_score(y_temp, temp_model.predict(X_temp_poly))
except FileNotFoundError as e:
    print(f"Error loading dataset files: {str(e)}")
    print("Please ensure all dataset files are present in the Prediction directory")
    exit(1)

@app.route('/')
def home():
    return render_template('index.html',
                         house_accuracy="{:.4f}".format(house_accuracy),
                         salary_accuracy="{:.4f}".format(salary_accuracy),
                         diabetes_accuracy="{:.4f}".format(diabetes_accuracy),
                         fruit_accuracy="{:.4f}".format(fruit_accuracy),
                         temp_accuracy="{:.4f}".format(temp_accuracy))

@app.route('/predict_house', methods=['POST'])
def predict_house():
    try:
        data = request.get_json()
        sqft = float(data['sqft'])
        
        # Input validation
        if sqft <= 0:
            return jsonify({'error': 'Square footage must be positive'}), 400
            
        # Scale input
        X = np.array([[sqft]], dtype=np.float64)
        X_scaled = house_scaler.transform(X)
        
        # Make prediction
        prediction = house_model.predict(X_scaled)[0][0]
        
        return jsonify({
            'prediction': float(prediction),
            'accuracy': float(house_accuracy)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict_salary', methods=['POST'])
def predict_salary():
    try:
        data = request.get_json()
        years_experience = float(data['years_experience'])
        education_level = int(data['education_level'])
        certifications = int(data['certifications'])
        
        # Input validation with more reasonable limits
        if years_experience < 0 or years_experience > 40:
            return jsonify({'error': 'Years of experience must be between 0 and 40'}), 400
        if education_level < 1 or education_level > 5:
            return jsonify({'error': 'Education level must be between 1 and 5'}), 400
        if certifications < 0 or certifications > 10:
            return jsonify({'error': 'Number of certifications must be between 0 and 10'}), 400
            
        # Scale inputs using reshape to avoid deprecation warning
        X = np.array([[years_experience, education_level, certifications]], dtype=np.float64)
        X_scaled = salary_scaler.transform(X)
        
        # Make prediction
        prediction = salary_model.predict(X_scaled)[0]
        
        # Apply experience multiplier for senior levels
        if years_experience > 10:
            prediction *= (1 + (years_experience - 10) * 0.03)  # 3% increase per year after 10 years
            
        # Apply education multiplier
        education_multiplier = {
            1: 1.0,    # High School
            2: 1.1,    # Bachelor's
            3: 1.2,    # Master's
            4: 1.3,    # PhD
            5: 1.4     # Post-doc
        }
        prediction *= education_multiplier.get(education_level, 1.0)
        
        # Ensure minimum salary of $40,000
        prediction = max(prediction, 40000)
        
        return jsonify({
            'prediction': float(prediction),
            'accuracy': float(salary_accuracy)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict_diabetes', methods=['POST'])
def predict_diabetes():
    try:
        data = request.get_json()
        age = float(data['age'])
        bmi = float(data['bmi'])
        glucose = float(data['glucose'])
        blood_pressure = float(data['blood_pressure'])
        
        # Validate input ranges
        if age < 0 or age > 120 or bmi < 10 or bmi > 50 or glucose < 50 or glucose > 400 or blood_pressure < 60 or blood_pressure > 200:
            return jsonify({'error': 'Invalid input values'}), 400
        
        features = np.array([[age, bmi, glucose, blood_pressure]], dtype=np.float64)
        features_scaled = diabetes_scaler.transform(features)
        prediction = diabetes_model.predict(features_scaled)[0]
        raw_probability = diabetes_model.predict_proba(features_scaled)[0][1] * 100
        
        # Adjust probability based on medical guidelines
        base_probability = raw_probability
        
        # Adjust based on glucose level
        if glucose >= 140 and glucose < 200:  # Pre-diabetic range
            base_probability = min(base_probability, 75)  # Cap at 75% for pre-diabetic
        elif glucose >= 200:  # Diabetic range
            base_probability = min(base_probability, 95)  # Cap at 95% for diabetic
            
        # Adjust based on BMI
        if bmi >= 30:  # Obese
            base_probability = min(base_probability + 10, 95)
        elif bmi >= 25:  # Overweight
            base_probability = min(base_probability + 5, 95)
            
        # Determine risk level based on adjusted probability and glucose level
        if glucose >= 200:  # Diabetic range
            risk_level = "High Risk"
        elif glucose >= 140:  # Pre-diabetic range
            if base_probability >= 65:
                risk_level = "High Risk"
            else:
                risk_level = "Moderate Risk"
        else:
            if base_probability < 40:
                risk_level = "Low Risk"
            elif base_probability < 65:
                risk_level = "Moderate Risk"
            else:
                risk_level = "High Risk"

        return jsonify({
            'age': age,
            'bmi': bmi,
            'glucose_level': glucose,
            'blood_pressure': blood_pressure,
            'diabetes_risk': risk_level,
            'probability': round(base_probability, 2),
            'model_accuracy': round(diabetes_accuracy * 100, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict_fruit', methods=['POST'])
def predict_fruit():
    try:
        data = request.get_json()
        weight = float(data['weight'])
        size = float(data['size'])
        color_score = float(data['color_score'])
        
        # Input validation
        if weight <= 0 or size <= 0:
            return jsonify({'error': 'Weight and size must be positive'}), 400
        if color_score < 0 or color_score > 1:
            return jsonify({'error': 'Color score must be between 0 and 1'}), 400
            
        # Scale inputs
        X = [[weight, size, color_score]]
        X_scaled = fruit_scaler.transform(X)
        
        # Get prediction probabilities
        probabilities = fruit_model.predict_proba(X_scaled)[0]
        prediction_idx = np.argmax(probabilities)
        
        # Get fruit classes
        fruit_classes = ['Apple', 'Banana', 'Orange']
        predicted_fruit = fruit_classes[prediction_idx]
        
        # Define typical ranges for each fruit
        typical_ranges = {
            'Apple': {
                'weight': (120, 200),
                'size': (6, 8),
                'color': (0.7, 0.9)
            },
            'Banana': {
                'weight': (100, 150),
                'size': (12, 18),
                'color': (0.5, 0.7)
            },
            'Orange': {
                'weight': (150, 250),
                'size': (7, 10),
                'color': (0.6, 0.8)
            }
        }
        
        # Calculate feature scores for each fruit
        def calculate_range_score(value, range_tuple):
            min_val, max_val = range_tuple
            if min_val <= value <= max_val:
                return 1.0
            if value < min_val:
                return max(0.3, 1 - (min_val - value) / min_val)
            return max(0.3, 1 - (value - max_val) / max_val)
        
        # Calculate scores for each fruit
        fruit_scores = {}
        for fruit, ranges in typical_ranges.items():
            weight_score = calculate_range_score(weight, ranges['weight'])
            size_score = calculate_range_score(size, ranges['size'])
            color_score = calculate_range_score(color_score, ranges['color'])
            
            # Weight the scores (size is most important for fruit classification)
            total_score = (weight_score * 0.3 + size_score * 0.5 + color_score * 0.2)
            
            # Special handling for orange-like features
            if fruit == 'Orange' and 150 <= weight <= 250 and 7 <= size <= 10:
                total_score *= 1.2  # Boost score for orange-like features
                
            fruit_scores[fruit] = total_score
        
        # Adjust prediction based on feature scores
        best_fruit = max(fruit_scores.items(), key=lambda x: x[1])[0]
        if fruit_scores[best_fruit] > fruit_scores[predicted_fruit] * 1.1:  # Reduced threshold
            predicted_fruit = best_fruit
            prediction_idx = fruit_classes.index(predicted_fruit)
        
        # Calculate final confidence
        base_confidence = probabilities[prediction_idx]
        feature_confidence = fruit_scores[predicted_fruit]
        confidence = (base_confidence * 0.6 + feature_confidence * 0.4) ** 0.5
        
        # Prepare top predictions with adjusted probabilities
        top_predictions = []
        for i, (fruit, prob) in enumerate(zip(fruit_classes, probabilities)):
            if prob > 0.01:  # Only include significant probabilities
                adjusted_prob = prob * fruit_scores[fruit]
                top_predictions.append({
                    'fruit': fruit,
                    'probability': round(adjusted_prob, 2)
                })
        
        # Sort by probability
        top_predictions.sort(key=lambda x: x['probability'], reverse=True)
        
        return jsonify({
            'prediction': predicted_fruit,
            'confidence': round(confidence, 2),
            'top_predictions': top_predictions,
            'model_accuracy': round(fruit_accuracy * 100, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict_temperature', methods=['POST'])
def predict_temperature():
    try:
        data = request.get_json()
        day = float(data['day'])
        humidity = float(data['humidity'])
        wind_speed = float(data['wind_speed'])
        pressure = float(data['pressure'])
        
        # Validate input ranges
        if day < 1 or day > 31 or humidity < 0 or humidity > 100 or wind_speed < 0 or wind_speed > 100 or pressure < 900 or pressure > 1100:
            return jsonify({
                'error': 'Invalid input values. Day must be between 1-31, humidity between 0-100%, wind speed between 0-100 km/h, and pressure between 900-1100 hPa.'
            }), 400
        
        # Prepare features using reshape to avoid deprecation warning
        features = np.array([[day, humidity, wind_speed, pressure]], dtype=np.float64)
        features_scaled = temp_scaler.transform(features)
        features_poly = temp_poly.transform(features_scaled)
        
        # Make prediction and ensure it's a scalar
        prediction = float(temp_model.predict(features_poly)[0])
        
        # Ensure reasonable temperature range (-50°C to 60°C)
        prediction = max(min(prediction, 60), -50)
        
        return jsonify({
            'prediction': prediction,
            'day': day,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'pressure': pressure,
            'model_accuracy': round(temp_accuracy * 100, 2)
        })
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': 'Invalid input values. Please provide valid numbers.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
