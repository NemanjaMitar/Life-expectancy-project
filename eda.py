from sklearn.linear_model import LinearRegression
import numpy as np

class EDA:
    def __init__(self, data=None):
        self.data = data.data
        self.data.columns = self.data.columns.str.strip()
    def check_missing_values(self):
        print(self.data.isnull().sum())

    def impute_numeric(self, country_col='Country'):
    # Iterate through all numeric columns
        for col in self.data.select_dtypes(include='number').columns:
            # Compute global mean for fallback
            global_mean = self.data[col].mean()

            # Define a function to fill NaNs for a group (country)
            def fill_country(group):
                if group[col].notnull().any():  # If there is at least one value
                    filled = group[col].fillna(group[col].mean())
                else:  # All values are null
                    filled = group[col].fillna(global_mean)
                return filled.round(2)  # Round to 2 decimals

            # Apply group-wise fill
            self.data[col] = self.data.groupby(country_col, group_keys=False).apply(fill_country)

        print("Numeric columns imputed with country-specific means (global fallback), rounded to 2 decimals.")

    def one_hot_encoding(self, status_col='Status'):
        self.data[status_col] = self.data[status_col].apply( lambda x: 1 if str(x).strip().lower() == 'developed' else 0)




    def handle_anomalies(self, x_col='Life expectancy', z_thresh=3, exclude_cols=None):
        if exclude_cols is None:
            exclude_cols = []
        exclude_cols = set(exclude_cols) | {x_col}

        numeric_cols = self.data.select_dtypes(include=np.number).columns
        y_cols = [col for col in numeric_cols if col not in exclude_cols]

        for country, group in self.data.groupby('Country'):
            group = group.copy()
            X = group[[x_col]].values
            if X.shape[0] < 2:
                continue  # not enough data to fit

            for y_col in y_cols:
                Y = group[y_col].values
                # skip columns with insufficient valid data
                if np.sum(~np.isnan(Y)) < 2:
                    continue

                model = LinearRegression()
                # Only use valid rows
                mask = ~np.isnan(X.flatten()) & ~np.isnan(Y)
                if np.sum(mask) < 2:
                    continue
                model.fit(X[mask], Y[mask])
                preds = model.predict(X)
                residuals = Y - preds
                z_scores = (residuals - np.nanmean(residuals)) / (np.nanstd(residuals) + 1e-8)
                anomalies = np.abs(z_scores) > z_thresh
                if anomalies.any():
                    print(f"{country} - {y_col}: corrected {anomalies.sum()} anomalies using LR")
                    self.data.loc[group.index[anomalies], y_col] = preds[anomalies]