import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib

# Load Dataset
dataset = pd.read_csv("employee_salaries.csv")

# Prepare features and target
X = dataset[['YearsExperience', 'EducationLevel', 'Certifications']].values
y = dataset['Salary'].values.reshape(-1, 1)

# Handle missing values
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)
y = imputer.fit_transform(y)

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split dataset into training (70%) and testing (30%)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Train Multiple Linear Regression Model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Save the trained model and scaler
joblib.dump(regressor, "employee_salary_model.pkl")
joblib.dump(scaler, "salary_scaler.pkl")

print("Model trained and saved as employee_salary_model.pkl")
print("Scaler saved as salary_scaler.pkl")

# Predict Test Data
y_pred = regressor.predict(X_test)

# Calculate R² Score
r2_score = regressor.score(X_test, y_test)
print(f"Model Accuracy (R² Score): {r2_score:.4f}")

# Print feature importance
feature_names = ['Years Experience', 'Education Level', 'Certifications']
for name, coef in zip(feature_names, regressor.coef_[0]):
    print(f"{name}: {coef:.2f}")

# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Salary')
plt.ylabel('Predicted Salary')
plt.title('Actual vs Predicted Salaries')
plt.show()
