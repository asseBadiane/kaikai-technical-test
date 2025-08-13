# PARTIE A : Python & Analyse de Données

# Section A1 : Import et Nettoyage (15 points)
# Tâche A1.1 : Chargement et exploration (5 points)

from prometheus_client import Counter, start_http_server
import time

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


def load_sensor_data(filepath):
    try:
        # Chargement avec gestion d'encodage et erreurs
        df = pd.read_csv(filepath, encoding='utf-8', encoding_errors='replace', low_memory=False)
        
        # Affichage de la structure
        print("Structure du dataset :")
        print(df.info())
        
        print("\nPremières lignes :")
        print(df.head())
        
        print("\nValeurs manquantes par colonne :")
        print(df.isnull().sum())
        
        print("\nStatistiques descriptives :")
        print(df.describe())
        
        # Identification des colonnes importantes
        important_columns = [
            'Location Name', 'Local Date/Time', 'PM2.5 (μg/m³) corrected',
            'Temperature (°C) corrected', 'Humidity (%) corrected',
            'Location Type', 'TVOC index', 'NOX index'
        ]
        print("\nColonnes importantes pour l'analyse :", important_columns)
        
        # Problèmes potentiels
        problems = []
        if df['Location Group'].isnull().all():
            problems.append("Colonne 'Location Group' est entièrement vide.")
        if df.isnull().sum().sum() > 0:
            problems.append("Valeurs manquantes détectées (ex. : CO2).")
        print("\nProblèmes potentiels :", problems if problems else "Aucun détecté dans l'échantillon.")
        
        return df
    except FileNotFoundError:
        print("Erreur : Fichier non trouvé.")
        return None
    except pd.errors.ParserError:
        print("Error : Issue with file format.")
        return None
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return None

# Load filepath 
df = load_sensor_data('data/capteur_temp.csv')


# # Tâche A1.2 : Nettoyage des données (10 points)

def clean_sensor_data(df):
    # Conversion des dates
    df['Local Date/Time'] = pd.to_datetime(df['Local Date/Time'], errors='coerce')
    df['UTC Date/Time'] = pd.to_datetime(df['UTC Date/Time'], errors='coerce')
    
    # Gestion des manquants (PM2.5, Temp, Humidité) - impute médiane par location
    for col in ['PM2.5 (μg/m³) corrected', 'Temperature (°C) corrected', 'Humidity (%) corrected']:
        df[col] = df.groupby('Location Name')[col].transform(lambda x: x.fillna(x.median()))
    
    # Outliers : Cap PM2.5 >500 à 500
    outliers = df['PM2.5 (μg/m³) corrected'] > 500
    df.loc[outliers, 'PM2.5 (μg/m³) corrected'] = 500
    print(f"Nombre d'outliers traités : {outliers.sum()}")  # 0 dans l'échantillon
    
    # Drop colonnes inutiles (ex. entièrement vides)
    df = df.drop(columns=['Location Group'], errors='ignore')
    
    return df

# Appliquer après chargement
if df is not None:
    df = clean_sensor_data(df)
# Questions à répondre :

# Justification stratégie manquants : 
# 1: J'utilise l'imputation par médiane groupée par Location Name car les capteurs sont site-spécifiques ; 
# ça préserve les patterns locaux (ex. : humidité plus haute en indoor). Médiane vs moyenne : 
# Plus résistante aux outliers dans des données IoT bruitées. Si <5% manquants, suppression possible, mais imputation maximise les données.
# 2: Identification et traitement outliers : Identifie via seuil fixe (>500, comme tâche). Alternative : 
# Z-score (>3 std) ou IQR. Traitement : Capping à 500 pour atténuer l'impact sans perte (utile pour moyennes). Dans l'échantillon : 
# 0 outliers.



# # Section A2 : Analyse et Visualisation (20 points)
# # Tâche A2.1 : Analyse temporelle (10 points)

# Extraction date et heure
df['Date'] = df['Local Date/Time'].dt.date
df['Hour'] = df['Local Date/Time'].dt.hour

# Moyennes journalières par location
daily_avg = df.groupby(['Location Name', 'Date'])[['PM2.5 (μg/m³) corrected', 'Temperature (°C) corrected', 'Humidity (%) corrected']].mean()
print("Moyennes journalières :\n", daily_avg)

# Heures de pic
peaks = df[df['PM2.5 (μg/m³) corrected'] > 35].groupby('Hour').size()
print("Heures de pic (PM2.5 >35) :", peaks if not peaks.empty else "Aucun dans l'échantillon")

# Visualisation évolution 24h (moyen par heure)
hourly_pm = df.groupby('Hour')['PM2.5 (μg/m³) corrected'].mean()
plt.figure(figsize=(10, 5))
hourly_pm.plot(kind='line', marker='o')
plt.title('Évolution PM2.5 sur 24h (moyen par heure)')
plt.xlabel('Heure')
plt.ylabel('PM2.5 (μg/m³)')
plt.grid(True)
plt.savefig('evolution_24h.png')  # Sauvegarde pour livrable
plt.show()  # Ou close() si non interactif


# Tâche A2.2 : Corrélations et insights (10 points)


# Corrélations
corr = df[['PM2.5 (μg/m³) corrected', 'Temperature (°C) corrected', 'Humidity (%) corrected']].corr()
print("Matrice de corrélations :\n", corr)
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Corrélations')
plt.savefig('correlations.png')

# Localisation la plus polluée
most_polluted = df.groupby('Location Name')['PM2.5 (μg/m³) corrected'].mean().idxmax()
print("Localisation la plus polluée :", most_polluted)  # Lycée Technique André Peytavin dans échantillon

# Dashboard avec 4 visualisations
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# 1: Bar moyennes PM par location
df.groupby('Location Name')['PM2.5 (μg/m³) corrected'].mean().plot(kind='bar', ax=axs[0,0])
axs[0,0].set_title('PM2.5 moyen par location')

# 2: Scatter PM vs Temp
axs[0,1].scatter(df['Temperature (°C) corrected'], df['PM2.5 (μg/m³) corrected'])
axs[0,1].set_title('PM2.5 vs Temp')

# 3: Boxplot PM par type (Indoor/Outdoor)
sns.boxplot(x='Location Type', y='PM2.5 (μg/m³) corrected', data=df, ax=axs[1,0])
axs[1,0].set_title('PM2.5 par type')

# 4: Line humidité vs heure
df.groupby('Hour')['Humidity (%) corrected'].mean().plot(kind='line', ax=axs[1,1])
axs[1,1].set_title('Humidité sur 24h')

plt.tight_layout()
plt.savefig('dashboard.png')


# Section A3 : Préparation pour la production (10 points)
# Tâche A3.1 : Fonctions réutilisables

def process_sensor_data(filepath):
    """
    Fonction qui automatise le traitement des données
    - Charge le fichier
    - Nettoie les données
    - Calcule les métriques clés
    - Retourne un dictionnaire de résultats
    """
    df = load_sensor_data(filepath)  # De A1.1
    if df is None:
        return {"error": "Échec du chargement"}
    
    df = clean_sensor_data(df)  # De A1.2
    
    # Métriques clés
    daily_avg = df.groupby(['Location Name', df['Local Date/Time'].dt.date])['PM2.5 (μg/m³) corrected'].mean()
    correlations = df[['PM2.5 (μg/m³) corrected', 'Temperature (°C) corrected', 'Humidity (%) corrected']].corr()
    most_polluted = df.groupby('Location Name')['PM2.5 (μg/m³) corrected'].mean().idxmax()
    peaks_count = (df['PM2.5 (μg/m³) corrected'] > 35).sum()
    
    results = {
        "daily_averages": daily_avg.to_dict(),
        "correlations": correlations.to_dict(),
        "most_polluted_location": most_polluted,
        "peak_hours_count": peaks_count,
        "cleaned_rows": len(df)
    }
    
    # Sauvegarde plots (optionnel)
    # ... (ajoute code viz ici si besoin)
    
    return results

# Exemple
results = process_sensor_data("data/capteur_temp.csv")
print(results)



# Start HTTP server for metrics
start_http_server(8000)
PROCESS_COUNT = Counter('processed_rows_total', 'Total rows processed')

def process_sensor_data(filepath):
    # Existing code...
    df = load_sensor_data(filepath)
    if df is not None:
        PROCESS_COUNT.inc(len(df))  # Increment counter
        # Rest of your processing...
    return results