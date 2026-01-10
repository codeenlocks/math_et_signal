"""
@DESCRIPTION
"""



import matplotlib.pyplot as plt
import numpy as np
from fft import signal_utile, FFT
from data import df, get_full_signal, N, view


debut, fin = 0, 27393
start_year = 1950
end_year = start_year + 9

def limitation(duration : int, start = 1950) -> None :
    global debut, fin, start_year, end_year
    start_year = start
    end_year = start_year + 9
    debut = int ((start - 1950) * 365.25)
    fin = debut + int (duration * 365.25)

def BRUIT(s) :
    s_centre = s - np.mean(s)
    
    BRUIT = s_centre - signal_utile(s)
    return BRUIT
    
    
def RSB(s) :
    """

    Parameters
    ----------
    s : signal 
        signal prélevé tel que dans le .csv

    Returns
    -------
    Rapport signal sur bruit en décibel

    """
    s_centre = s - np.mean(s)
    puissance_s = np.mean(s_centre**2)
    
    Bruit = BRUIT(s)
    puissance_B = np.mean(Bruit**2)
    
    rsb = 10 * np.log10(puissance_s/puissance_B)
    return rsb

def main() -> None:
    """
    Script principal pour l’étude du bruit
    par calcul du rapport signal/bruit (RSB)
    """
    global start_year, end_year, debut, fin
    
    LABELS = [
            [("Bruit (°C)", 
                f"Modélisation du bruit de température à Strasbourg ({start_year}-{end_year})"),
               ("Bruit (mm)",
                f"Modélisation du bruit de précipitations à Strasbourg ({start_year}-{end_year})"),
               ("Bruit (mm)", 
                f"Modélisation du bruit de neige à Strasbourg ({start_year}-{end_year})")],
            
              [("Bruit (km/h)",
               f"Modélisation du bruit de vent à Strasbourg ({start_year}-{end_year})"),
               ("Bruit (mn)",
                f"Modélisation du bruit l'ensoleillement à Strasbourg ({start_year}-{end_year})"),
               ("Bruit (hpa)",
                f"Modélisation du bruit de pression à Strasbourg ({start_year}-{end_year})")]
              ]
    
    # 1. Aperçu et préparation des données
    view()
    
    # On récupère les signaux complets (75 ans) liés à la température
    T_avg = get_full_signal('tavg')
    T_min = get_full_signal('tmin')
    T_max = get_full_signal('tmax')

    # 2. Calcul du signal utile (Modélisation périodique)
    # signal_utile(s) renvoie la sinusoïde reconstruite à partir de la FFT
    B_avg_modele, rsb_avg = BRUIT(T_avg), RSB(T_avg)
    B_min_modele, rsb_min = BRUIT(T_min), RSB (T_min)
    B_max_modele, rsb_max = BRUIT(T_max), RSB(T_max)

    # 3. Calcul des caractéristiques du modèle
    # On récupère les paramètres de la température moyenne
    f_dom, A_dom, phi_dom = FFT(T_avg)
    

    # 4. Affichage graphique
    fig, axs = plt.subplots(2, 3, figsize=(30, 20))

    

    # On trace les modèles périodiques (signaux utiles)
    axs[0,0].plot(B_avg_modele, color='red', linewidth=2, label=f'Modèle Moyenne : RSB={rsb_avg:.2f}')
    axs[0,0].plot(B_min_modele, color='blue', linewidth=1, linestyle='--', label=f'Modèle Min : RSB={rsb_min:.2f}')
    axs[0,0].plot(B_max_modele, color='orange', linewidth=1, linestyle='--', label=f'Modèle Max : RSB={rsb_max:.2f}')

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
    B_spd_modele, rsb_spd = BRUIT(W_spd), RSB(W_spd)
    B_pgt_modele, rsb_pgt = BRUIT(W_pgt), RSB(W_pgt)


    # 3. Calcul des caractéristiques du modèle
    # On récupère les paramètres de la vitesse du vent
    f_dom, A_dom, phi_dom = FFT(W_spd)
    #periode_jours = 1 / f_dom 
    
    


    # On trace les modèles périodiques (signaux utiles)
    axs[1,0].plot(B_spd_modele, color='red', linewidth=2, label=f'Modèle vitesse : RSB = {rsb_spd:.2f}')
    axs[1,0].plot(B_pgt_modele, color='blue', linewidth=1, linestyle='--', label=f'Modèle pic de rafale : RSB = {rsb_pgt:.2f}')
    
    
    
    
    # On récupère les signaux complets (75 ans) du reste des données
    
    # 1. Dnnées prélevées
    PRCP = get_full_signal('prcp')
    t_sun = get_full_signal('tsun')
    SNOW = get_full_signal('snow')
    PRES = get_full_signal('pres')
    
    # 2. Calcul du signal utile (Modélisation périodique)
    # signal_utile(s) renvoie la sinusoïde reconstruite à partir de la FFT
    B_prcp_modele, rsb_prcp = BRUIT(PRCP), RSB(PRCP)
    B_tsun_modele, rsb_tsun = BRUIT(t_sun), RSB(t_sun)
    B_snow_modele, rsb_snow = BRUIT(SNOW), RSB(SNOW)
    B_pres_modele, rsb_pres = BRUIT(PRES), RSB(PRES)


    # 3. Calcul des caractéristiques du modèle
    # On récupère les paramètres de la vitesse du vent
    #f_dom, A_dom, phi_dom = FFT(W_spd)
    #periode_jours = 1 / f_dom 
    
    


    # On trace les modèles périodiques (signaux utiles)
    axs[0,1].plot(B_prcp_modele, color='red', linewidth=2, label=f'Modèle pluies : RSB = {rsb_prcp:.2f}')
    axs[1,1].plot(B_tsun_modele, color='red', linewidth=2, label=f'Modèle ensolleiment : RSB = {rsb_tsun:.2f}')
    axs[0,2].plot(B_snow_modele, color='red', linewidth=2, label=f'Modèle neige : RSB = {rsb_snow:.2f}')
    axs[1,2].plot(B_pres_modele, color='red', linewidth=2, label=f'Modèle pression : RSB = {rsb_pres:.2f}')
    
    

    
    #====#Définitions des paramètres génériques à tous les graphiques#====#
    for i in range(2) :
        for j in range(3) :
            axs[i,j].legend(loc='upper right')
            axs[i,j].grid(True, which='both', linestyle='--', alpha=0.5)
            axs[i,j].set_xticks(indices)
            axs[i,j].set_xticklabels(labels_ans, rotation=45)
            axs[i,j].set_xlim(debut, fin)
            axs[i,j].set_xlabel("Années de prélèvement")
            axs[i,j].set_ylabel(LABELS[i][j][0])
            axs[i,j].set_title(LABELS[i][j][1])
            
    
    plt.tight_layout()
    plt.savefig(f"../images/bruits/bruit_strasbourg_{start_year}_{end_year}.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    
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