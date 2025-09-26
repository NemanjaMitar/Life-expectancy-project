import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np

class Model:
    def __init__(self, df):
        self.df = df
        self.X = None
        self.y = None

    # -----------------------------
    # PRIPREMA PODATAKA
    # -----------------------------
    def prepare_data(self, target='Life expectancy', features=None, exclude_cols=None, test_size=0.2, random_state=42):
        if exclude_cols is None:
            exclude_cols = []
        exclude_cols = set(exclude_cols) | {target}

        if features is None:
            # sve numeričke osim targeta i exclude_cols
            self.X = self.df.select_dtypes(include=np.number).drop(columns=exclude_cols, errors='ignore')
        else:
            self.X = self.df[features]

        self.y = self.df[target]
        return train_test_split(self.X, self.y, test_size=test_size, random_state=random_state)

    # -----------------------------
    # GRID SEARCH
    # -----------------------------
    def grid_search(self, model, param_grid, X_train, y_train, scoring='r2', cv=5):
        grid = GridSearchCV(model, param_grid, cv=cv, scoring=scoring, n_jobs=-1, verbose=2)
        grid.fit(X_train, y_train)
        print("Najbolji parametri:", grid.best_params_)
        return grid.best_estimator_

    # -----------------------------
    # CROSS VALIDATION
    # -----------------------------
    def cross_validation(self, model, X=None, y=None, cv=5, scoring='r2'):
        if X is None or y is None:
            X, y = self.X, self.y
        scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
        print(f"R2 po fold-ovima: {scores}")
        print(f"Prosek R2: {np.mean(scores):.3f}")
        return scores

    # -----------------------------
    # FEATURE IMPORTANCE
    # -----------------------------
    def plot_feature_importance(self, model, top_n=10):
        if hasattr(model, 'feature_importances_'):
            importances = pd.Series(model.feature_importances_, index=self.X.columns)
            importances = importances.sort_values(ascending=False).head(top_n)
            plt.figure(figsize=(8,6))
            sns.barplot(x=importances.values, y=importances.index)
            plt.title(f"Top {top_n} feature importance")
            plt.show()
            return importances
        else:
            print("Model nema attribute 'feature_importances_'")
            return None

    # -----------------------------
    # EVALUACIJA MODELA
    # -----------------------------
    def evaluate_model(self, model, X_test, y_test):
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"MSE: {mse:.3f}, MAE: {mae:.3f}, R2: {r2:.3f}")

        # plot reziduala
        plt.figure(figsize=(6,4))
        sns.scatterplot(x=y_test, y=y_pred)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        plt.xlabel("True Values")
        plt.ylabel("Predictions")
        plt.title("Predictions vs True Values")
        plt.show()

        return mse, mae, r2

    # -----------------------------
    # TRENING RANDOM FOREST
    # -----------------------------
    def train_random_forest(self, features=None):
        X_train, X_test, y_train, y_test = self.prepare_data(features=features, exclude_cols=['Year'])
        param_grid = {
            "n_estimators": [500, 1000, 2000],
            "max_depth": [None, 10, 20, 30],
            "max_features": ["sqrt", "log2"]
        }
        rf = RandomForestRegressor(random_state=0)
        best_model = self.grid_search(rf, param_grid, X_train, y_train)
        self.evaluate_model(best_model, X_test, y_test)
        self.cross_validation(best_model)
        self.plot_feature_importance(best_model)
        return best_model

    # -----------------------------
    # TRENING GRADIENT BOOSTING
    # -----------------------------
    def train_gradient_boosting(self, features=None):
        X_train, X_test, y_train, y_test = self.prepare_data(features=features, exclude_cols=['Year'])
        param_grid = {
            "n_estimators": [100, 300, 500],
            "learning_rate": [0.01, 0.05, 0.1],
            "max_depth": [3, 5, 7]
        }
        gb = GradientBoostingRegressor(random_state=0)
        best_model = self.grid_search(gb, param_grid, X_train, y_train)
        self.evaluate_model(best_model, X_test, y_test)
        self.cross_validation(best_model)
        self.plot_feature_importance(best_model)
        return best_model

    # -----------------------------
    # NAMERNO LOŠ MODEL
    # -----------------------------
    def train_bad_model(self, features=None):
        X_train, X_test, y_train, y_test = self.prepare_data(features=features, exclude_cols=['Year'])
        bad_tree = DecisionTreeRegressor(max_depth=1, min_samples_split=2000, random_state=0)
        bad_tree.fit(X_train, y_train)
        self.evaluate_model(bad_tree, X_test, y_test)
        self.cross_validation(bad_tree)
        return bad_tree
