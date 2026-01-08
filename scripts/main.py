import matplotlib.pyplot as plt
import numpy as np
from fft import signal_utile, FFT
from data import df, get_full_signal, N, view

def main() -> None:
    """
    Script principal pour l'analyse des températures de Strasbourg.
    Modélisation par FFT et extraction du signal périodique.
    """
    
    # 1. Aperçu et préparation des données
    view()
    
    # On récupère les signaux complets (75 ans) directement via la nouvelle fonction
    # C'est beaucoup plus rapide que de boucler année par année
    T_avg = get_full_signal('tavg')
    T_min = get_full_signal('tmin')
    T_max = get_full_signal('tmax')

    # 2. Calcul du signal utile (Modélisation périodique)
    # signal_utile(s) renvoie la sinusoïde reconstruite à partir de la FFT
    S_avg_modele = signal_utile(T_avg)
    S_min_modele = signal_utile(T_min)
    S_max_modele = signal_utile(T_max)

    # 3. Calcul des caractéristiques du modèle (pour ton rapport)
    # On récupère les paramètres de la température moyenne
    f_dom, A_dom, phi_dom = FFT(T_avg)
    periode_jours = 1 / f_dom
    
    print("\n--- Caractéristiques du modèle (T_avg) ---")
    print(f"Fréquence dominante : {f_dom:.6f} cycles/jour")
    print(f"Période détectée    : {periode_jours:.2f} jours (Cycle annuel)")
    print(f"Amplitude du cycle  : {A_dom:.2f} °C")
    print(f"Phase à l'origine   : {phi_dom:.2f} rad")

    # 4. Affichage graphique
    plt.figure(figsize=(12, 6))

    # On trace le signal réel (en arrière-plan, plus clair)
    plt.plot(T_avg, color='lightgray', alpha=0.5, label='Données réelles (T_avg)')

    # On trace les modèles périodiques (signaux utiles)
    plt.plot(S_avg_modele, color='red', linewidth=2, label='Modèle Moyenne')
    plt.plot(S_min_modele, color='blue', linewidth=1, linestyle='--', label='Modèle Min')
    plt.plot(S_max_modele, color='orange', linewidth=1, linestyle='--', label='Modèle Max')

    # 5. Gestion de l'axe X (Dates)
    # On place une étiquette tous les 10 ans pour la lisibilité
    step = 365 * 10
    indices = np.arange(0, N, step)
    # On extrait les années correspondantes depuis le DataFrame de data.py
    labels_ans = df['time'].dt.year.iloc[indices].values

    plt.xticks(ticks=indices, labels=labels_ans, rotation=45)
    
    plt.xlabel("Années de prélèvement")
    plt.ylabel("Températures (°C)")
    plt.title("Modélisation du cycle saisonnier à Strasbourg (1950-2024)")
    plt.legend(loc='upper right')
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.show()

    # 6. Analyse du bruit blanc (résidus)
    bruit = T_avg - S_avg_modele
    sigma_bruit = np.std(bruit)
    print(f"Écart-type du bruit blanc : {sigma_bruit:.2f} °C")

if __name__ == "__main__":
    main()