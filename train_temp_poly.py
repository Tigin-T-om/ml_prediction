import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
import joblib

# Load Dataset
dataset = pd.read_csv("temperature_prediction_data.csv")
X = dataset.iloc[:, :-1].values  # Features (Day, Humidity, Wind Speed, Pressure)
y = dataset.iloc[:, -1:].values  # Temperature

# Handle missing values
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
X = imputer.fit_transform(X)
y = imputer.fit_transform(y)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Polynomial Feature Transformation
degree = 3  # You can adjust the polynomial degree
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(X_scaled)

# Split dataset into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

# Train Polynomial Regression Model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Save the trained model and scalers
joblib.dump(regressor, "temperature_prediction_model.pkl")
joblib.dump(scaler, "temperature_prediction_scaler.pkl")
joblib.dump(poly, "temperature_prediction_poly.pkl")
print("Model and scaler trained and saved")

# Predict Test Data
y_pred = regressor.predict(X_test)

# Model Accuracy (R² Score)
r2_score = regressor.score(X_test, y_test)
print(f"Model Accuracy (R² Score): {r2_score:.4f}")

# Visualization (Actual vs Predicted)
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color='blue', label='Predicted vs Actual')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r', lw=2, label='Ideal Fit')
plt.xlabel("Actual Temperature (°C)")
plt.ylabel("Predicted Temperature (°C)")
plt.title("Actual vs Predicted Temperature")
plt.legend()
plt.grid(True)
plt.show()
