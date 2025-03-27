import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

# Load Dataset
dataset = pd.read_csv("diabetes_balanced_data.csv")

# Prepare features and target
X = dataset[['Age', 'BMI', 'Glucose', 'BloodPressure']].values
y = dataset['Diabetes'].values  # Binary classification (0 or 1)

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split dataset into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train Logistic Regression Model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the trained model and scaler
joblib.dump(model, "diabetes_model.pkl")
joblib.dump(scaler, "diabetes_scaler.pkl")

print("Model trained and saved as diabetes_model.pkl")
print("Scaler saved as diabetes_scaler.pkl")

# Predict Test Data
y_pred = model.predict(X_test)

# Model Accuracy
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.4f}")

# Feature Importance (Coefficients)
feature_names = ['Age', 'BMI', 'Glucose', 'Blood Pressure']
for name, coef in zip(feature_names, model.coef_[0]):
    print(f"{name}: {coef:.4f}")

# Visualizing Actual vs Predicted
plt.figure(figsize=(8, 6))
plt.scatter(range(len(y_test)), y_test, color="red", label="Actual")
plt.scatter(range(len(y_pred)), y_pred, color="blue", marker="x", label="Predicted")
plt.xlabel("Samples")
plt.ylabel("Diabetes (0 = No, 1 = Yes)")
plt.title("Actual vs Predicted Diabetes Cases")
plt.legend()
plt.show()
