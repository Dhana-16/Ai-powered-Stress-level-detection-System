import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
df = pd.read_csv("../dataset/Mental Health Dataset.csv")
df.drop("Timestamp", axis=1, inplace=True)
label_encoders = {}
for col in df.columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le
X = df.drop("Growing_Stress", axis=1)
y = df["Growing_Stress"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_split=5,
    random_state=42
)

model.fit(X_train, y_train)
joblib.dump(model, "stress_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")
print("✅ Stress Detection Model Trained Successfully")
