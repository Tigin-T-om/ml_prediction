# Machine Learning Predictions Web Application

A Flask-based web application that provides various machine learning prediction services including house prices, employee salaries, diabetes risk assessment, fruit classification, and temperature predictions.

## Features

- **House Price Prediction**: Predicts house prices based on square footage
- **Salary Prediction**: Estimates employee salaries based on experience, education, and certifications
- **Diabetes Risk Assessment**: Evaluates diabetes risk based on health metrics
- **Fruit Classification**: Classifies fruits based on physical characteristics
- **Temperature Prediction**: Forecasts temperature based on weather conditions

## Models and Accuracies

1. **House Price Model**
   - Features: Square footage
   - Model Type: Linear Regression
   - Accuracy: R² = 0.9993
   - Dataset Size: 120 samples

2. **Salary Prediction Model**
   - Features: Years of experience, Education level, Certifications
   - Model Type: Multiple Linear Regression
   - Accuracy: R² = 0.95
   - Dataset Size: 202 samples

3. **Diabetes Risk Model**
   - Features: Age, BMI, Glucose, Blood Pressure
   - Model Type: Logistic Regression
   - Accuracy: R² = 0.95
   - Dataset Size: 502 samples

4. **Fruit Classification Model**
   - Features: Weight, Size, Color Score
   - Model Type: K-Nearest Neighbors
   - Accuracy: 0.95
   - Dataset Size: 152 samples

5. **Temperature Prediction Model**
   - Features: Day, Humidity, Wind Speed, Pressure
   - Model Type: Polynomial Regression
   - Accuracy: R² = 0.95
   - Dataset Size: 367 samples

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Prediction
```

2. Create and activate a virtual environment:
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Use the web interface to make predictions:
   - Enter the required input values
   - Click "Predict" to get results
   - View the prediction and model accuracy

## Project Structure

```
Prediction/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
├── static/              # CSS, JS, and other static files
├── *.pkl                # Trained model files
└── *.csv                # Training datasets
```

## Dependencies

- Flask
- scikit-learn
- pandas
- numpy
- joblib

## Model Training

Each model can be retrained using its respective training script:
- `train_model.py` - House price model
- `train_mlr_model.py` - Salary prediction model
- `train_diabetes_model.py` - Diabetes risk model
- `train_fruit_model.py` - Fruit classification model
- `train_temp_poly.py` - Temperature prediction model

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 