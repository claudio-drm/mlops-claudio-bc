import json
from pathlib import Path
import pickle
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

ART = Path("artifacts")
ART.mkdir(parents=True, exist_ok=True)

data = load_breast_cancer(as_frame=True)
df = data.frame.copy()
y = df["target"]
X = df.drop(columns=["target"])

X.columns = (
    X.columns.str.replace(" ", "_")
             .str.replace("(", "", regex=False)
             .str.replace(")", "", regex=False)
             .str.replace("/", "_", regex=False)
             .str.replace("__", "_", regex=False)
             .str.lower()
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

clf = LogisticRegression(class_weight="balanced", max_iter=2000, random_state=42)
clf.fit(X_train_s, y_train)

proba = clf.predict_proba(X_test_s)[:, 1]
auc = roc_auc_score(y_test, proba)
print(f"AUC: {auc:.4f}")

with open(ART / "claudio_bc_model.pkl", "wb") as f:
    pickle.dump(clf, f)
with open(ART / "claudio_bc_scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
(ART / "claudio_bc_feature_order.json").write_text(json.dumps(X.columns.tolist(), ensure_ascii=False))
