import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np

class Model:
    def __init__(self, df):
        self.df = df
        self.X = None
        self.y = None

    def prepare_data(self, target='Life expectancy', test_size=0.3, random_state=42):
        # Odabir svih numeričkih kolona osim target
        self.X = self.df.select_dtypes(include=np.number).drop(columns=[target], errors='ignore')
        self.y = self.df[target]
        return train_test_split(self.X, self.y, test_size=test_size, random_state=random_state)

    # Grid search - vraca najbolju kombinaciju parametara prosledjenu prilikom obucavanja
    def grid_search(self, model, param_grid, X_train, y_train):
        grid = GridSearchCV(model, param_grid)
        grid.fit(X_train, y_train)
        print("Najbolji parametri:", grid.best_params_)
        return grid.best_estimator_

    # Cross validation -  poredi R2 score na osnovu podele test skupa, delimo na 5 foldova sa razlicitim podacima
    def cross_validation(self, model, X=None, y=None, cv=5, scoring='r2'):
        if X is None or y is None:
            X, y = self.X, self.y
        scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
        print(f"R2 po fold-ovima: {scores}")
        print(f"Prosek R2: {np.mean(scores):.3f}")
        return scores

    # Racuna MSE, MAE, R2 za svaki model koji cemo proslediti i plotuje predikciju u odnosu na stvarne vrednosti
    def evaluate_model(self, model, X_test, y_test):
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"MSE: {mse:.3f}, MAE: {mae:.3f}, R2: {r2:.3f}")

        plt.figure(figsize=(6,4))
        sns.scatterplot(x=y_test, y=y_pred)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        plt.xlabel("True Values")
        plt.ylabel("Predictions")
        plt.title("Predictions vs True Values")
        plt.show()
        return mse, mae, r2


    def train_LR(self): 
        X_train, X_test, y_train, y_test = self.prepare_data()
        model = LinearRegression()
        model.fit(X_train, y_train)
        self.evaluate_model(model, X_test, y_test)
        return model
    # LASSO REGRESIJA
    def train_lasso(self):
        X_train, X_test, y_train, y_test = self.prepare_data()
        param_grid = {"alpha": [0.1, 1, 10, 100]}
        lasso = Lasso(random_state=0, max_iter=10000)
        najbolji_model = self.grid_search(lasso, param_grid, X_train, y_train)
        self.evaluate_model(najbolji_model, X_test, y_test)
        self.cross_validation(najbolji_model)
        return najbolji_model


    # RIDGE REGRESIJA
    def train_ridge(self):
        X_train, X_test, y_train, y_test = self.prepare_data()
        param_grid = {"alpha": [0.001, 0.01, 0.1, 1, 10, 100]}
        ridge = Ridge(random_state=0, max_iter=10000)
        najbolji_model = self.grid_search(ridge, param_grid, X_train, y_train)
        self.evaluate_model(najbolji_model, X_test, y_test)
        self.cross_validation(najbolji_model)
        return najbolji_model

    # Random Forest regresija
    # Kod regresije - koristi se srednja vrednost svih predikcija
    def train_random_forest(self):
        X_train, X_test, y_train, y_test = self.prepare_data()
        param_grid = {
            "n_estimators": [100, 200],
            "max_depth": [None, 5, 10, 20]
            #"min_samples_split": [2, 5, 10],
            #"min_samples_leaf": [1, 2, 4]
        }
        rf = RandomForestRegressor(random_state=0)
        najbolji_model = self.grid_search(rf, param_grid, X_train, y_train)
        self.evaluate_model(najbolji_model, X_test, y_test)
        self.cross_validation(najbolji_model, X_train, y_train)

        # Bonus - plottujemo najbitnije feature za RF
        importances = pd.Series(najbolji_model.feature_importances_, index=self.X.columns)
        importances = importances.sort_values(ascending=False)
        plt.figure(figsize=(8,6))
        sns.barplot(x=importances.values[:10], y=importances.index[:10])
        plt.title("Top 10 Feature Importances")
        plt.show()

        return najbolji_model
