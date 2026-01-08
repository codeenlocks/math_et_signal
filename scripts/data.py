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


def get_years_range():
    """Retourne la liste des années disponibles dans le fichier."""
    return sorted(df['time'].dt.year.unique())