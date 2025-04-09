import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

# === Load the steps-sleep dataset ===
df = pd.read_csv("merged_steps_sleep_clean.csv")

# === Define features and target ===
features = ["total_steps", "steps_2h_before_sleep", "took_nap"]

X = df[features].copy()
X["took_nap"] = X["took_nap"].astype(int)  # convert bool to int

y = df["sleep_quality"]

# === Split the data with stratification ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.4,
    stratify=y,
    random_state=42
)

# === Train decision tree ===
clf = DecisionTreeClassifier(max_depth=4, random_state=42)
clf.fit(X_train, y_train)

# === Evaluate ===
y_pred = clf.predict(X_test)

print("📊 Classification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\n🧮 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\n🔍 Predictions vs Actual:")
print(pd.DataFrame({"Actual": y_test.values, "Predicted": y_pred}))

# === Visualize the tree ===
plt.figure(figsize=(12, 6))
plot_tree(clf, feature_names=features, class_names=clf.classes_, filled=True)
plt.title("Decision Tree for Sleep Quality (Steps-Only)")
plt.show()
