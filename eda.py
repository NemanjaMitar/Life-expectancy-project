from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib as plt

'''
    Eksplorativna analiza skupa
    Klasa koju koristimo za preuredjivanje skupa podataka, uklananje anomalija, skaliranje podataka, kodiranje podataka...

'''
class EDA:
    def __init__(self, data=None):
        # self.data predstavlja dataframe iz pandas-a
        self.data = data
        self.data.columns = self.data.columns.str.strip()

    def check_missing_values(self):
        print(self.data.isnull().sum())

    """
        Otkrivanje i obrada nedostajućih vrednosti - identifikacija praznih
        ili nepotpunih zapisa i njihovo popunjavanje, uklanjanje ili interpolacija
        na osnovu statističkih metoda.
    """
    
    def impute_numeric(self, country_col='Country'):
        def fill_country(group):
            # Ovo je pomocna funkcija koja na osnovu pozatih podataka popunjava prazne redove u okviru neke kolone
            # Nama ce koristiti ako za drzavu fali odredjen red, na osnovu podataka za tu drzavu ce racunati prosek kojim ce popuniti
            # Ako nema nikakvih podataka za tu drzavu za taj red, onda ce popuniti globalnim prosekom

            # Mozda bi isto bila dobra a ne preterano zahtevna metoda ako imamo podatke za kolonu da koristimo Linearnu regresiju ali
            # dobro pokusacu ovako
            if group[col].notnull().any(): 
                filled = group[col].fillna(group[col].mean())
            else:  
                filled = group[col].fillna(global_mean)

            return filled.round(2) 
        
        # Uzima samo numericke kolone odnosno one koje imaju u sebi brojeve
        for col in self.data.select_dtypes(include='number').columns:
            global_mean = self.data[col].mean()
           
            # GroupBy deli tabelu na manje tabele i primenjuje funkciju fill_country(), 
            # Za svaku drzavu
            self.data[col] = self.data.groupby(country_col, group_keys=False).apply(fill_country)

    # Spoiler : Nema duplih podataka, Spoiler 2 : ne moramo nikakve duplikate da brinemo
    def print_duplicate_info(self):
        # Da li postoje duplikati po svim kolonama (bukvalno isti red):
        print("Duplikati po svim kolonama:")
        print(self.data[self.data.duplicated()])

    # Ako je drzava u razvoju -> Status = 1
    # Else status -> 0
    def one_hot_encoding(self, status_col='Status'):
        def encode_status(x):
            if str(x).strip().lower() == 'developed':
                return 1
            else:
                return 0

        self.data[status_col] = self.data[status_col].apply(encode_status)

    # Skaliranje odredjenih kolona podataka
    def weight_pondering(self, cols, factor):
        for col in cols:
            self.data[col] = self.data[col] * factor


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
