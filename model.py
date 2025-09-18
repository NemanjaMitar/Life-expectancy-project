from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


class Model:
    def __init__(self,data):
        self.data = data.data 

    def random_forest(self):
        # Drop non-numeric or irrelevant columns
        exclude_cols = ['Life expectancy', 'Year']  # exclude target and categorical columns for now
        X = self.data.drop(columns=exclude_cols)
        y = self.data['Life expectancy']

        # Split into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize the model
        model = RandomForestRegressor(n_estimators=1000, random_state=0)

        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)

        # Evaluate
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"Test MSE: {mse}")
        print(f"Test R2: {r2}")

        return mse, r2