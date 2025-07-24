import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import joblib
import os

# Define base directory relative to current file
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct dataset path relative to this file
illness_data_path = os.path.join(base_dir, "..", "datasets", "illness_dataset.csv")

# Load data
df = pd.read_csv(illness_data_path)

# Features and label
X = df.drop('Disease', axis=1)
y = df['Disease']

# Encode target labels
le = LabelEncoder()
Y = le.fit_transform(y)

# Train-test split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

# Train SVC model
mdl = SVC(kernel='linear', probability=True, class_weight='balanced', random_state=42)
mdl.fit(X_train, Y_train)

# Save the model and label encoder
joblib.dump(mdl, 'mental_health_model.joblib')
joblib.dump(le, 'label_encoder.joblib')
joblib.dump(list(X.columns), 'symptoms_list.joblib')

print("SVC model and encoder saved successfully.")
