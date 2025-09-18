from data_load import DataLoad
from eda import EDA
from model import Model
import warnings
# https://drive.google.com/drive/folders/1nE4-ZytyNWDtDTjSC1YEmZZi4TpvH2ac

warnings.filterwarnings('ignore', category=FutureWarning)

if __name__ == "__main__":   
    # Ucitavanja podataka iz dataseta
    data = DataLoad('data.csv')

    # Kolone 
    # print(data.columns())

    # Vizuelno detektovanje anomalija i outliera
    # data.detect_anomalies('Year')
    # Obratiti posebnu paznju na one iz pod iz teksta

    # EDA
    eda = EDA(data)
    eda.check_missing_values()
    eda.impute_numeric()
    eda.check_missing_values()
    
    # Onehot encoding 
    eda.one_hot_encoding()
    eda.handle_anomalies()


    # Kolona Country nam sigurno nece biti ni od kakvog znacaja tako da mozemo da je izostavimo iz razmatranja
    # Zakomplikovace nam zivot jer ima 193 zemlje u razmatranju 💀

    data.drop('Country')
    data.export_data('output.csv')


    # Treniranje Modela 
    model = Model(data)
    model.train_random_forest()


