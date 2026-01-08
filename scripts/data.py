import numpy as np
import pandas as pd
#from datetime import datetime

"""
Script  pour la manipulation des données météo de Strasbourg-Entzheim.
"""

# --- 1. Chargement et Nettoyage Initial ---
chemin_fichier = 'strasbourg_entzheim.csv'
df = pd.read_csv(chemin_fichier)

# Conversion automatique de la colonne temps
df['time'] = pd.to_datetime(df['time'])

# Paramètres globaux pour la FFT
N = len(df)
Te = 1.0  # Période d'échantillonnage (1 jour)
fs = 1/Te
freqs = np.fft.fftfreq(N, d=1/fs)

# --- 2. Fonctions de base et Utilitaires ---

def view() -> None:
    """Affiche un aperçu des données et détecte les valeurs manquantes."""
    print("Aperçu des données :")
    print(df.head())
    print("\nStatistiques sur les données manquantes (NaN) :")
    print(df.isnull().sum())
    print(f"\nNombre total de points : {N}")

def get_full_signal(colonne: str) -> np.ndarray:
    """
    Récupère une colonne complète et gère les valeurs manquantes (NaN).
    C'est la fonction la plus sûre pour la FFT.
    """
    # On remplace les trous (NaN) par la moyenne de la colonne pour ne pas fausser la FFT
    return df[colonne].fillna(df[colonne].mean()).values

# --- 3. Fonctions compatibles avec main.py actuel ---
# Note : Ces fonctions extraient les données année par année.

def temp(annee: int, arg: str) -> list:
    """Retourne les températures ('min', 'max', 'avg') pour une année précise."""
    mask = df['time'].dt.year == annee
    col = 't' + arg
    # On extrait, on bouche les trous par la moyenne locale, et on convertit en liste
    return df.loc[mask, col].fillna(df[col].mean()).tolist()

def wind(annee: int, arg: str) -> list:
    """Retourne les données de vent ('dir', 'spd', 'pgt') pour une année précise."""
    mask = df['time'].dt.year == annee
    col = 'w' + arg
    return df.loc[mask, col].fillna(df[col].mean()).tolist()

def prcp(annee: int) -> list:
    mask = df['time'].dt.year == annee
    return df.loc[mask, 'prcp'].fillna(0).tolist() # Précipitations : on met 0 si manquant

def snow(annee: int) -> list:
    mask = df['time'].dt.year == annee
    return df.loc[mask, 'snow'].fillna(0).tolist()

def pres(annee: int) -> list:
    mask = df['time'].dt.year == annee
    return df.loc[mask, 'pres'].fillna(df['pres'].mean()).tolist()

def tsun(annee: int) -> list:
    mask = df['time'].dt.year == annee
    return df.loc[mask, 'tsun'].fillna(0).tolist()

# --- 4. Fonctions de gestion de dates (optionnelles avec Pandas mais conservées) ---

def duree(date_debut: str, date_fin: str) -> int:
    """Calcule la durée en jours entre deux chaînes 'AAAA-MM-JJ'."""
    d1 = pd.to_datetime(date_debut)
    d2 = pd.to_datetime(date_fin)
    return abs((d2 - d1).days)

def get_years_range():
    """Retourne la liste des années disponibles dans le fichier."""
    return sorted(df['time'].dt.year.unique())