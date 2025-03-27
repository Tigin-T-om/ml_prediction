import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib

# Load Dataset
dataset = pd.read_csv("house_prediction_slr.csv")
X = dataset.iloc[:, 0:1].values  # Square Footage
y = dataset.iloc[:, 1:2].values  # Price

# Handle missing values
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
X = imputer.fit_transform(X)
y = imputer.fit_transform(y)

# Create and fit scaler for features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split dataset into training (70%) and testing (30%)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Train Linear Regression Model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Save the trained model and scaler
joblib.dump(regressor, "house_price_model.pkl")
joblib.dump(scaler, "house_price_scaler.pkl")
print("Model and scaler trained and saved")

# Predict Test Data
y_pred = regressor.predict(X_test)

# Model Accuracy (R² Score)
r2_score = regressor.score(X_test, y_test)
print(f"Model Accuracy (R² Score): {r2_score:.4f}")

# Plot Training Set
plt.figure(figsize=(10, 6))
plt.scatter(X_train, y_train, color="red", label="Training Data")
plt.plot(X_train, regressor.predict(X_train), color="blue", label="Regression Line")
plt.title("Square Footage vs House Price (Training Set)")
plt.xlabel("Square Footage")
plt.ylabel("House Price ($)")
plt.legend()
plt.grid(True)
plt.show()

# Plot Test Set
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color="red", label="Test Data")
plt.plot(X_train, regressor.predict(X_train), color="blue", label="Regression Line")
plt.title("Square Footage vs House Price (Test Set)")
plt.xlabel("Square Footage")
plt.ylabel("House Price ($)")
plt.legend()
plt.grid(True)
plt.show()

# Test predictions for minimum values
min_sqft = 100
min_sqft_scaled = scaler.transform([[min_sqft]])
min_pred = regressor.predict(min_sqft_scaled)[0][0]
print(f"Prediction for minimum square footage ({min_sqft}): ${min_pred:,.2f}")