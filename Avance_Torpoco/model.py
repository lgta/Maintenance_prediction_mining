"""Training utilities."""
from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

# -------------------------------------------------------------------------
def train_failure_classifier(X: pd.DataFrame,
                             y: pd.Series,
                             test_size: float = 0.2,
                             random_state: int = 42) -> Tuple[Pipeline, float]:
    """Train a baseline logistic model and return it with ROC‑AUC on hold‑out."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state)

    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('clf',    LogisticRegression(max_iter=200,
                                      class_weight='balanced',
                                      random_state=random_state))
    ])
    pipe.fit(X_train, y_train)
    preds = pipe.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, preds)
    return pipe, auc

# -------------------------------------------------------------------------
def cv_auc(pipe: Pipeline,
           X: pd.DataFrame,
           y: pd.Series,
           n_splits: int = 5,
           random_state: int = 42) -> float:
    """Cross‑validated ROC‑AUC mean."""
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    scores = cross_val_score(pipe, X, y, cv=cv, scoring='roc_auc', n_jobs=-1)
    return scores.mean()




def benchmark_models(X, y, test_size=0.2, random_state=42):
    """Entrena Logistic, RandomForest y GradientBoost; devuelve dict ordenado por AUC."""
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=test_size,
                                          stratify=y, random_state=random_state)

    models = {
        "LogReg": LogisticRegression(max_iter=200, class_weight="balanced"),
        "RandomForest": RandomForestClassifier(n_estimators=300, n_jobs=-1,
                                               class_weight="balanced",
                                               random_state=random_state),
        "GradientBoost": GradientBoostingClassifier(random_state=random_state),
    }

    results = {}
    for name, est in models.items():
        est.fit(Xtr, ytr)
        auc = roc_auc_score(yte, est.predict_proba(Xte)[:, 1])
        results[name] = (est, auc)
        print(f"{name:12s} AUC = {auc:.3f}")

    return dict(sorted(results.items(), key=lambda kv: kv[1][1], reverse=True))