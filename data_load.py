import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataLoad:
    def __init__(self, file_path=None):
        self.data = None
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                print(f"Uspesno ucitan dataset iz {file_path}")
            except FileNotFoundError:
                print(f"Dataset '{file_path}' nije pronadjen")
            except Exception as e:
                print(f"Error tokom citanja dataseta: {e}")
        else:
            print("Nije prosleđen put do fajla.")

    def get_data(self):
        return self.data

    def columns(self, quantity=None):
        return self.data.columns[:quantity] if quantity else self.data.columns

    def eda(self):
        print(self.data.describe(include="all"))

    def detect_anomalies(self, col=None):
        if self.data is None:
            print("Data nije ucitana.")
            return

        cols = [col] if col else self.data.select_dtypes(include="number").columns

        for c in cols:
            plt.figure(figsize=(6, 4))
            sns.boxplot(x=self.data[c])
            plt.title(f"Boxplot of {c}")
            plt.show()

    def drop(self, col):
        if col in self.data.columns:
            self.data.drop([col], axis=1, inplace=True)

    def export_data(self, file_path="output.csv", file_type="csv"):
        try:
            if file_type == "csv":
                self.data.to_csv(file_path, index=False)
            else:
                print(f"Nepodržan tip fajla: {file_type}")
                return
            print(f"Data eksportovan u {file_path}")
        except Exception as e:
            print(f"Error prilikom eksportovanja: {e}")
