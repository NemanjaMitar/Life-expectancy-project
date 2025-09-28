import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataLoad:
    def __init__(self, file_path=None):
        self.data = pd.read_csv(file_path) if file_path else None
        print(f"Uspesno ucitan dataset iz {file_path}")

    def get_data(self):
        return self.data

    def columns(self, quantity=None):
        return self.data.columns[:quantity] if quantity else self.data.columns

    def eda(self):
        print(self.data.describe(include="all"))

    def detect_anomalies(self, col=None):
        # Eventualno ako je nesto poslo po zlu
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

    def export_data(self, file_path="output.csv"):
        self.data.to_csv(file_path, index=False)

    def histogram(self):
        self.data.hist(bins = 30, color = 'g', figsize=(20,20))
        plt.show()
    
    def heatmap(self):
        plt.figure(figsize = (20,20))
        corr_matrix = self.data.select_dtypes(include='number').corr()
        sns.heatmap(corr_matrix, annot = True)
        plt.show()