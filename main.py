from data_load import DataLoad
from eda import EDA
from model import Model
import warnings
import pandas as pd

# https://drive.google.com/drive/folders/1nE4-ZytyNWDtDTjSC1YEmZZi4TpvH2ac

warnings.filterwarnings('ignore', category=FutureWarning)

if __name__ == "__main__":
    # Ucitavanje
    loader = DataLoad("data.csv")
    # df = loader.get_data()
    print(loader.columns())
    # loader.detect_anomalies()
    # loader.eda()
"""
    # EDA
    eda = EDA(df)
    eda.check_missing_values()
    eda.impute_numeric()
    eda.print_duplicate_info()
    eda.one_hot_encoding()
    eda.handle_anomalies()
    eda.weight_pondering(['Hepatitis B', 'Polio', 'Diphtheria'], 1.5)
    
    # Drop nepotrebnih kolona
    df = eda.data.drop(columns=["Country"], errors="ignore")

    # Export
    loader.data = df   # update da DataLoad ima najnoviju verziju
    loader.export_data("output.csv")

    # Model
    model = Model(df)

    # Model 1 - los DecisionTree
    model.train_bad_model()

    # Model 2 - Random Forest
    model.train_random_forest()

    # Model 3 Gradient Boosting
    #
    model.train_gradient_boosting()
"""