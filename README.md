# Dokumentacija projekta – Predikcija životnog veka

## 1. Uvod

Cilj ovog projekta je izrada modela koji, na osnovu socio-ekonomskih i zdravstvenih pokazatelja, predviđa očekivani životni vek (*Life expectancy*) u različitim državama. Projekat spada u kategoriju regresionih problema, jer je ciljna promenljiva numeričkog tipa.  

Podaci obuhvataju demografske, ekonomske, socijalne i zdravstvene indikatore, pri čemu je poseban akcenat stavljen na stope imunizacije protiv **Hepatitisa B, Polia i Difterije**, kao i na **Indeks ljudskog razvoja (HDI)**. Odabrani su faktori koji najbolje oslikavaju stanje javnog zdravlja i kvalitet života populacije.  

Korišćeni skup podataka preuzet je iz **Global Health Observatory (GHO)** baze Svetske zdravstvene organizacije (WHO), kao i podataka Ujedinjenih nacija. Dataset obuhvata period od **2000. do 2015. godine** i sadrži informacije za ukupno **193 zemlje**.

---

## 2. Struktura dataset-a i njegova interpretacija

Ulazni skup podataka dostavljen je u `.csv` formatu i sadrži ukupno **22 kolone** i više od **2000 redova**.  
Radi lakšeg upoznavanja sa podacima, njihovog pregleda, kao i detekcije anomalija i nedostajućih vrednosti, u okviru projekta je implementirana pomoćna klasa (*data_load.py*). Ova klasa omogućava:

- vizuelizaciju osnovnih karakteristika skupa  
- pregled i proveru tipova podataka 
- detekciju nedostajućih vrednosti i anomalija  

### Kolone dataseta

Dataset obuhvata sledeće atribute:  

- **Country** – naziv zemlje  
- **Year** – godina posmatranja  
- **Status** – razvojni status zemlje (razvijena / u razvoju)  
- **Life expectancy** – očekivani životni vek (ciljna promenljiva)  
- **Adult Mortality** – smrtnost odraslih  
- **Infant deaths** – smrtnost odojčadi  
- **Alcohol** – prosečna potrošnja alkohola  
- **Percentage expenditure** – procentualna potrošnja na zdravstvo  
- **Hepatitis B** – stopa imunizacije protiv hepatitisa B  
- **Measles** – broj slučajeva malih boginja  
- **BMI** – prosečan indeks telesne mase  
- **Under-five deaths** – smrtnost dece mlađe od pet godina  
- **Polio** – stopa imunizacije protiv polia  
- **Total Expenditure** – ukupna izdvajanja za zdravstvo  
- **Diphtheria** – stopa imunizacije protiv difterije  
- **HIV/AIDS** – stopa obolelih od HIV/AIDS-a  
- **GDP** – bruto domaći proizvod po glavi stanovnika  
- **Population** – broj stanovnika  
- **Thinness 1–19 years** – učestalost pothranjenosti kod mladih od 1 do 19 godina  
- **Thinness 5–9 years** – učestalost pothranjenosti kod dece od 5 do 9 godina  
- **Income composition of resources** – indeks raspodele prihoda (komponenta HDI)  
- **Schooling** – prosečan broj godina školovanja  

Ove kolone je moguće uočiti pozivom funkicije: `print(loader.columns())`