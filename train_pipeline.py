# train_pipeline.py
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules
from joblib import dump

# === STEP 1: Load & Clean Dataset ===
df = pd.read_csv("data/cars_delhi.csv")

# Clean km_driven
df["km_driven"] = df["km_driven"].astype(str).str.replace(",", "").str.replace(" km", "").str.replace("KM","").str.strip()
df["km_driven"] = pd.to_numeric(df["km_driven"], errors="coerce")

# Clean price
df["price"] = df["price"].astype(str).str.replace("₹", "").str.replace(",", "").str.strip()
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Extract region
df["region"] = df["registeration"].astype(str).str.split("-").str[0]

df = df.dropna(subset=["km_driven","price"])

# === STEP 2: Fair Price Estimation (KNN) ===
X = df[["car_name","variant","transmission","km_driven","owner_type","fuel_type","region"]]
y = df["price"]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["car_name","variant","transmission","owner_type","fuel_type","region"]),
    ("num", StandardScaler(), ["km_driven"])
])

knn = Pipeline([("pre", preprocessor), ("model", KNeighborsRegressor(n_neighbors=10))])
knn.fit(X, y)

df["fair_price"] = knn.predict(X)
df["deviation_pct"] = (df["price"] - df["fair_price"]) / df["fair_price"]

dump(knn, "models/knn_price.pkl")

# === STEP 3: Clustering ===
features = df[["deviation_pct","km_driven"]].fillna(0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)
df["cluster"] = labels

# Label clusters by median deviation
med = df.groupby("cluster")["deviation_pct"].median().sort_values()
mapping = {med.index[0]:"underpriced", med.index[1]:"normal", med.index[2]:"overpriced"}
df["cluster_name"] = df["cluster"].map(mapping)

dump({"scaler":scaler,"kmeans":kmeans,"mapping":mapping}, "models/price_clusters.pkl")

# === STEP 4: Manipulation Classification (Decision Tree) ===
df["manipulated"] = ((df["deviation_pct"] > 0.3) | (df["deviation_pct"] < -0.3)).astype(int)

X_cls = df[["km_driven","fair_price","deviation_pct"]]
y_cls = df["manipulated"]

tree = DecisionTreeClassifier(max_depth=5, random_state=42)
tree.fit(X_cls, y_cls)
df["manipulation_prob"] = tree.predict_proba(X_cls)[:,1]

dump(tree, "models/tree_manipulation.pkl")

# === STEP 5: Association Rules ===
bins_dev = [-np.inf,-0.2,-0.05,0.05,0.2,np.inf]
labels_dev = ["deep_under","under","fair","over","deep_over"]
df["dev_bucket"] = pd.cut(df["deviation_pct"], bins=bins_dev, labels=labels_dev)

basket_cols = ["region","fuel_type","transmission","owner_type","dev_bucket","cluster_name"]
dummies = pd.get_dummies(df[basket_cols], drop_first=False)
freq = apriori(dummies.astype(bool), min_support=0.05, use_colnames=True)
rules = association_rules(freq, metric="lift", min_threshold=1.2).sort_values("lift", ascending=False)
rules_small = rules[["antecedents","consequents","support","confidence","lift"]].head(30)
rules_small = rules_small.applymap(lambda x:", ".join(list(x)) if isinstance(x,frozenset) else x)
rules_small.to_csv("data/assoc_rules.csv", index=False)

# === STEP 6: Save Cleaned Data ===
df.to_csv("data/cars_cleaned.csv", index=False)
print("Pipeline complete. Outputs saved in data/ and models/")
