import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataLoad:
    def __init__(self, filePath=None):
        try:
            if not filePath:  # empty or None
                raise ValueError("No file path provided.")

            # Try reading the CSV
            self.data = pd.read_csv(filePath)
            print(f"Uspesno ucitan dataset iz {filePath}")

        except FileNotFoundError:
            print(f"Dataset '{filePath}' nije pronadjen")
            self.data = None

        except ValueError as ve:
            print(f"{ve}")
            self.data = None

        except Exception as e:
            # Svi ostali errori
            print(f"Error tokom citanja dataseta: {e}")
            self.data = None
    
    def columns(self,quantity = None):
        if quantity:
            return self.data.columns[:quantity]
        return self.data.columns

    def eda(self):
        print(self.data.describe(include="all"))


    def detect_anomalies(self, col=None):
        if col:
            cols = [col]
        else:
            # Detect for all numeric columns
            cols = self.data.select_dtypes(include='number').columns

        for col in cols:
            plt.figure(figsize=(6, 4))
            sns.boxplot(x=self.data[col])
            plt.title(f"Boxplot of {col}")
            plt.show()
            
    def drop(self, col):
        if col in self.data.columns:
            self.data.drop([col], axis=1, inplace=True)
        else:
            print(f"Column '{col}' does not exist.")

    def export_data(self, file_path='output.csv', file_type='csv'):
        if file_type == 'csv':
            self.data.to_csv(file_path, index=False)
        elif file_type == 'excel':
            self.data.to_excel(file_path, index=False)
        elif file_type == 'json':
            self.data.to_json(file_path)
        else:
            print(f"Unsupported file type: {file_type}")
        print(f"Data exported to {file_path}")