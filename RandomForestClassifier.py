import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv(r"C:\Users\schal\Downloads\combined_model_ready_all.csv")
df['sleep_quality_encoded'] = df['sleep_quality'].map({'Bad': 0, 'Average': 1, 'Good': 2})
df['took_nap'] = df['took_nap'].astype(int)

# Feature selection
features = [
    'total_steps', 'steps_2h_before_sleep', 'total_screen_time', 'unlock_count',
    'Instagram', 'YouTube', 'TikTok', 'Snapchat', '8 Ball Pool', 'Brawl Stars',
    'Clash of Clans', 'social_media_ratio', 'game_ratio'
]
X_raw = df[features].replace(0, np.nan).dropna(axis=1, how='all')
y_raw = df['sleep_quality_encoded']

# Impute and scale
imputer = SimpleImputer(strategy='constant', fill_value=0)
X_imputed = imputer.fit_transform(X_raw)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Combine features and labels
X_scaled_df = pd.DataFrame(X_scaled, columns=X_raw.columns)
X_scaled_df['label'] = y_raw.values

# Manual cluster-aware interpolation
X_augmented = []
y_augmented = []
rng = np.random.default_rng(42)
target_class_size = X_scaled_df['label'].value_counts().max()

for cls in sorted(X_scaled_df['label'].unique()):
    df_cls = X_scaled_df[X_scaled_df['label'] == cls].copy()
    X_cls = df_cls.drop(columns='label').values
    n_existing = len(X_cls)
    n_to_generate = target_class_size - n_existing

    # Cluster samples within the class
    n_clusters = min(3, n_existing)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(X_cls)

    # Generate synthetic samples within clusters
    synthetic_samples = []
    for _ in range(n_to_generate):
        # Randomly choose a cluster
        cluster_id = rng.choice(np.unique(cluster_labels))
        cluster_indices = np.where(cluster_labels == cluster_id)[0]
        if len(cluster_indices) < 2:
            continue  # can't interpolate
        i1, i2 = rng.choice(cluster_indices, size=2, replace=False)
        alpha = rng.random()
        synthetic = X_cls[i1] + alpha * (X_cls[i2] - X_cls[i1])
        synthetic_samples.append(synthetic)

    if synthetic_samples:
        X_combined = np.vstack([X_cls, np.array(synthetic_samples)])
    else:
        X_combined = X_cls  # no new samples, just keep original

    y_combined = np.full(X_combined.shape[0], cls)
    X_augmented.append(X_combined)
    y_augmented.append(y_combined)

# Final dataset
X_final = np.vstack(X_augmented)
y_final = np.concatenate(y_augmented)

print("\nBalanced class counts:")
print(pd.Series(y_final).value_counts().sort_index())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_final, y_final, test_size=0.2, stratify=y_final, random_state=42)

# Train model
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=4,
    min_samples_split=3,
    class_weight='balanced',
    random_state=42
)
model.fit(X_train, y_train)

# Evaluation
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

print(f"\nTraining Accuracy: {accuracy_score(y_train, y_train_pred):.2f}")
print(f"Test Accuracy: {accuracy_score(y_test, y_test_pred):.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_test_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_test_pred))
cm = confusion_matrix(y_test, y_test_pred)
print(cm)

# Confusion matrix plot
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
            xticklabels=['Bad', 'Average', 'Good'], 
            yticklabels=['Bad', 'Average', 'Good'])
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.tight_layout()
plt.show()

# Feature importance visualization
importances = model.feature_importances_
feature_names = X_raw.columns

# Sort importances
indices = np.argsort(importances)[::-1]
sorted_features = feature_names[indices]
sorted_importances = importances[indices]

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x=sorted_importances, y=sorted_features)
plt.title("Feature Importances from Random Forest")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()


