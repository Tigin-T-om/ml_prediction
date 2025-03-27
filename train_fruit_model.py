import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Load Dataset
dataset = pd.read_csv("fruit_dataset.csv")
X = dataset.iloc[:, :-1].values  # Features (Weight, Size, Color Score)
y = dataset.iloc[:, -1].values  # Labels (Fruit Type)

# Handle missing values
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
X = imputer.fit_transform(X)

# Create and fit scaler for features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split dataset into training (70%) and testing (30%)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Train KNN Model
k = 3  # Number of neighbors
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X_train, y_train)

# Save the trained model and scaler
joblib.dump(knn, "fruit_knn_model.pkl")
joblib.dump(scaler, "fruit_knn_scaler.pkl")
print("Model and scaler trained and saved")

# Predict Test Data
y_pred = knn.predict(X_test)

# Model Accuracy
accuracy = knn.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.4f}")

# Plot Training Set
plt.figure(figsize=(10, 6))
plt.scatter(X_train[:, 0], X_train[:, 1], c=[{'Apple': 0, 'Banana': 1, 'Orange': 2}[label] for label in y_train], cmap='viridis', label="Training Data")
plt.title("Fruit Classification (Training Set)")
plt.xlabel("Weight")
plt.ylabel("Size")
plt.legend()
plt.grid(True)
plt.show()

# Plot Test Set
plt.figure(figsize=(10, 6))
plt.scatter(X_test[:, 0], X_test[:, 1], c=[{'Apple': 0, 'Banana': 1, 'Orange': 2}[label] for label in y_test], cmap='viridis', label="Test Data")
plt.title("Fruit Classification (Test Set)")
plt.xlabel("Weight")
plt.ylabel("Size")
plt.legend()
plt.grid(True)
plt.show()

# Test predictions for a sample fruit
sample_fruit = [[150, 7, 0.8]]  # Example input
sample_fruit_scaled = scaler.transform(sample_fruit)
sample_pred = knn.predict(sample_fruit_scaled)[0]
print(f"Predicted fruit type for given input: {sample_pred}")