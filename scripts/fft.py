from data import N, freqs
import numpy as np


def FFT(s) :
    """
    Parameters
    ----------
    s : tab[float]
        Signal échantilloné (données du csv).

    Returns
    [f_dom, A_dom, phi_dom] 
    
    Applique FFT à un signal échantilloné pour déterminer
    la fréquence fondamentale et les autres caractéritiques
    dans le domaine spectrale.
    
    """
    retour_fft = np.fft.fft(s)
    amplitudes = (2/N)*np.abs(retour_fft)
    phases = np.angle(retour_fft)
    
    
    idx_max = np.argmax(amplitudes[1:N//2]) + 1 
    f_dom = freqs[idx_max]
    A_dom = amplitudes[idx_max]
    phi_dom = phases[idx_max]
    
    return [f_dom, A_dom, phi_dom]



def signal_utile(s) :
    """

    Parameters
    ----------
    s : tab[float]
        Signal échantilloné (données du csv).

    Returns
    -------
    A * np.cos(2 * np.pi * f * t + phi)
        array[s_clean(i)] où s_clean est le signal utile de caractéristiques :
            Amplitude A
            Frequence f
            phase phi
        Déterminées par FFT.

    """
    # On gère les éventuels NaN (valeurs manquantes) fréquents dans les CSV météo
    s_clean = np.nan_to_num(s, nan=np.nanmean(s)) 
    
    f, A, phi = FFT(s_clean)
    t = np.arange(len(s_clean))
    
    # Reconstruction utilisant le cosinus pour être raccord avec la phase de la FFT
    return A * np.cos(2 * np.pi * f * t + phi)