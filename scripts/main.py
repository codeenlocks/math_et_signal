import matplotlib.pyplot as plt
import numpy as np
from fft import signal_utile, FFT
from data import df, get_full_signal, N, view

debut, fin = 0, 27393
start_year = 1950
end_year = start_year + 10

def limitation(duration : int, start = 1950) -> None :
    global debut, fin, start_year, end_year
    start_year = start
    end_year = start_year + 9
    debut = int ((start - 1950) * 365.25)
    fin = debut + int (duration * 365.25)

def main() -> None:
    """
    Script principal pour l'analyse des températures de Strasbourg.
    Modélisation par FFT et extraction du signal périodique.
    """
    global debut, fin, start_year, end_year
    
    LABELS = [
            [("Températures (°C)", 
                f"Modélisation de la température à Strasbourg ({start_year}-{end_year})"),
               ("Précipitaions (mm)",
                f"Modélisation des précipitations à Strasbourg ({start_year}-{end_year})"),
               ("Épaisseur de neige (mm)", 
                f"Modélisation de la neige à Strasbourg ({start_year}-{end_year})")],
            
              [("Vitesse (km/h)",
               f"Modélisation du vent à Strasbourg ({start_year}-{end_year})"),
               ("Durée d'ensoleillement (mn)",
                f"Modélisation de l'ensoleillement à Strasbourg ({start_year}-{end_year})"),
               ("Pression (hPa)",
                f"Modélisation de la pression à Strasbourg ({start_year}-{end_year})")]
              ]
    
    # 1. Aperçu et préparation des données
    view()
    
    # On récupère les signaux complets (75 ans) liés à la température
    T_avg = get_full_signal('tavg')
    T_min = get_full_signal('tmin')
    T_max = get_full_signal('tmax')

    # 2. Calcul du signal utile (Modélisation périodique)
    # signal_utile(s) renvoie la sinusoïde reconstruite à partir de la FFT
    S_avg_modele = signal_utile(T_avg)
    S_min_modele = signal_utile(T_min)
    S_max_modele = signal_utile(T_max)

    # 3. Calcul des caractéristiques du modèle
    # On récupère les paramètres de la température moyenne
    f_dom, A_dom, phi_dom = FFT(T_avg)
    #periode_jours = 1 / f_dom
    """
    Bloc à reproduire (éventuellement dans la boucle) 
    pour chacune des données pour dégager les cycles
    
    print("\n--- Caractéristiques du modèle (T_avg) ---")
    print(f"Fréquence dominante : {f_dom:.6f} cycles/jour")
    print(f"Période détectée    : {periode_jours:.2f} jours (Cycle annuel)")
    print(f"Amplitude du cycle  : {A_dom:.2f} °C")
    print(f"Phase à l'origine   : {phi_dom:.2f} rad")
    """
    

    # 4. Affichage graphique
    fig, axs = plt.subplots(2, 3, figsize=(30, 20))

    # On trace le signal réel (en arrière-plan, plus clair)
    axs[0,0].plot(T_avg, color='lightgray', alpha=0.5, label='Données réelles (T_avg)')

    # On trace les modèles périodiques (signaux utiles)
    axs[0,0].plot(S_avg_modele, color='red', linewidth=2, label='Modèle Moyenne')
    axs[0,0].plot(S_min_modele, color='blue', linewidth=1, linestyle='--', label='Modèle Min')
    axs[0,0].plot(S_max_modele, color='orange', linewidth=1, linestyle='--', label='Modèle Max')

    # 5. Gestion de l'axe X (Dates)
    # On place une étiquette tous les 10 ans pour la lisibilité
    step = 365.25*10
    indices = np.arange(0, N, step)
    # On extrait les années correspondantes depuis le DataFrame de data.py
    labels_ans = df['time'].dt.year.iloc[indices].values
    

    # On récupère les signaux complets (75 ans) liés au vent
    W_spd = get_full_signal('wspd')
    W_pgt = get_full_signal('wpgt')
    
    # 2. Calcul du signal utile (Modélisation périodique)
    # signal_utile(s) renvoie la sinusoïde reconstruite à partir de la FFT
    S_spd_modele = signal_utile(W_spd)
    S_pgt_modele = signal_utile(W_pgt)


    # 3. Calcul des caractéristiques du modèle
    # On récupère les paramètres de la vitesse du vent
    f_dom, A_dom, phi_dom = FFT(W_spd)
    #periode_jours = 1 / f_dom 
    
    


    # On trace les modèles périodiques (signaux utiles)
    axs[1,0].plot(S_spd_modele, color='red', linewidth=2, label='Modèle vitesse')
    axs[1,0].plot(S_pgt_modele, color='blue', linewidth=1, linestyle='--', label='Modèle pic de rafale')
    
    
    
    
    # On récupère les signaux complets (75 ans) du reste des données
    
    # 1. Dnnées prélevées
    PRCP = get_full_signal('prcp')
    t_sun = get_full_signal('tsun')
    SNOW = get_full_signal('snow')
    PRES = get_full_signal('pres')
    
    # 2. Calcul du signal utile (Modélisation périodique)
    # signal_utile(s) renvoie la sinusoïde reconstruite à partir de la FFT
    S_prcp_modele = signal_utile(PRCP)
    S_tsun_modele = signal_utile(t_sun)
    S_snow_modele = signal_utile(SNOW)
    S_pres_modele = signal_utile(PRES)


    # 3. Calcul des caractéristiques du modèle
    # On récupère les paramètres de la vitesse du vent
    #f_dom, A_dom, phi_dom = FFT(W_spd)
    #periode_jours = 1 / f_dom 
    
    


    # On trace les modèles périodiques (signaux utiles)
    axs[0,1].plot(S_prcp_modele, color='red', linewidth=2, label='Modèle pluies')
    axs[1,1].plot(S_tsun_modele, color='red', linewidth=2, label='Modèle ensolleiment')
    axs[0,2].plot(S_snow_modele, color='red', linewidth=2, label='Modèle neige')
    axs[1,2].plot(S_pres_modele, color='red', linewidth=2, label='Modèle pression')
    
    

    
    #====#Définitions des paramètres génériques à tous les graphiques#====#
    for i in range(2) :
        for j in range(3) :
            axs[i,j].legend(loc='upper right')
            axs[i,j].grid(True, which='both', linestyle='--', alpha=0.5)
            axs[i,j].set_xticks(indices)
            axs[i,j].set_xticklabels(labels_ans, rotation=45)
            axs[i,j].set_xlim(debut,fin)
            axs[i,j].set_xlabel("Années de prélèvement")
            axs[i,j].set_ylabel(LABELS[i][j][0])
            axs[i,j].set_title(LABELS[i][j][1])
            
    
    plt.tight_layout()
    plt.savefig(f"../images/analyse_strasbourg_{start_year}_{end_year}.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    """
    # 6. Analyse du bruit blanc (résidus)
    bruit = T_avg - S_avg_modele
    sigma_bruit = np.std(bruit)
    print(f"Écart-type du bruit blanc : {sigma_bruit:.2f} °C")
    """

"""
Pour une meilleure vue, on affichera les données que sur des intervalles 
de 10 ans
Retirer le "#" selon la période 10 ans désirée.
"""

if __name__ == "__main__":
    limitation(10), main()
    limitation(10,1960), main()
    limitation(10,1970), main()
    limitation(10,1980), main()
    limitation(10,1990), main()
    limitation(10,2000), main()
    limitation(10,2010), main()
    limitation(10,2015), main()
    
    