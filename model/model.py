from sklearn.datasets import load_iris
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib

# Load data
data = pd.read_csv('smart_farm_zoning_dataset.csv')
X = data[['temperature', 'pressure', 'altitude']]  
y = data['zone_class']

# StandardScaler + SMOTE + KNN
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('smote', SMOTE(random_state=42)),
    ('knn', KNeighborsClassifier(n_neighbors=3))  # Ganti k jika mau eksperimen
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Accuracy on entire dataset:", acc)

joblib.dump(pipeline, 'knn_model_smart_farm.pkl')

# Load model
model_loaded = joblib.load('knn_model_smart_farm.pkl')

# Data baru
data_baru = [[30.5, 1013.25, 10.0]]  # contoh: suhu, tekanan, ketinggian

# Prediksi
prediksi = model_loaded.predict(data_baru)
print("Hasil Prediksi:", prediksi[0])