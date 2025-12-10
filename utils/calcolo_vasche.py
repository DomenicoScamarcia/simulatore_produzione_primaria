"""
MODULO CALCOLO VASCHE - GRUPPO DEL PESCE
Funzioni per calcolare le risorse necessarie per ogni fase produttiva
"""

from data_model.lotto_produzione_model import LottoProduzione
from data_model.specie_ittica_model import SpecieIttica
from utils.configurazione import ConfigurazioneGruppoDelPesce


def calcola_vasche_larvali(lotto: LottoProduzione, config: ConfigurazioneGruppoDelPesce) -> int:
    """
    Determina quante vasche larvali sono necessarie per un lotto specifico
    basandosi sul numero di larve da seminare e sulla densità di semina della specie.
    Utilizza una capacità media di 8000 litri per vasca (mix di vasche piccole,
    medie e grandi) e calcola quante larve possono essere contenute per vasca
    moltiplicando la capacità per la densità specifica della specie (larve/litro).
    Arrotonda per eccesso (+1) per garantire spazio sufficiente e limita il risultato
    al numero totale di vasche larvali disponibili nell'impianto.
    """

    densita = lotto.specie.densita_semina_larvale

    # Usa le vasche piccole, medie, grandi
    capacita_media = 8000  # litri (media tra i vari tipi)
    vasche_totali = config.vasche_larvali_piccole + config.vasche_larvali_medie + config.vasche_larvali_grandi

    larve_per_vasca = capacita_media * densita
    vasche_necessarie = int(lotto.numero_larve / larve_per_vasca) + 1

    return min(vasche_necessarie, vasche_totali)

def calcola_vasche_preingrasso(post_larve: int, config: ConfigurazioneGruppoDelPesce) -> int:
    """
    Calcola il numero di vasche da 40mc (40.000 litri) necessarie per la fase
    di preingrasso, dove le post-larve crescono fino a raggiungere 2 grammi.
    Utilizza una densità fissa di 400 avannotti per metro cubo (ridotta rispetto
    alla fase larvale per garantire il benessere dei pesci). Converte la capacità
    della vasca da litri a metri cubi, calcola quante post-larve può contenere
    ciascuna vasca, determina il numero necessario arrotondando per eccesso (+1),
    e limita il risultato alle vasche di preingrasso effettivamente disponibili.
    """

    capacita_vasca = 40000  # litri
    densita = 400  # avannotti per mc (ridotta per benessere)

    post_larve_per_vasca = (capacita_vasca / 1000) * densita
    vasche_necessarie = int(post_larve / post_larve_per_vasca) + 1

    return min(vasche_necessarie, config.vasche_preingrasso)

def calcola_gabbie_ingrasso(avannotti: int, specie: SpecieIttica, config: ConfigurazioneGruppoDelPesce) -> int:
    """
    Determina il numero di gabbie in mare necessarie per la fase finale di ingrasso,
    dove gli avannotti crescono fino a raggiungere la taglia commerciale (350-900g
    a seconda della specie). Utilizza la densità di ingrasso specifica per ogni specie
    (pesci per metro cubo, più bassa rispetto alle fasi precedenti per garantire
    crescita ottimale) e il volume standard delle gabbie. Calcola la capienza di
    ogni gabbia moltiplicando volume per densità, determina quante gabbie servono
    arrotondando per eccesso (+1), e limita al totale di gabbie disponibili
    distribuito sui 6 impianti produttivi del Gruppo Del Pesce.
    """

    densita = specie.densita_ingrasso
    volume_gabbia = config.volume_gabbia

    pesci_per_gabbia = volume_gabbia * densita
    gabbie_necessarie = int(avannotti / pesci_per_gabbia) + 1

    gabbie_totali_disponibili = config.gabbie_per_impianto * config.numero_impianti
    return min(gabbie_necessarie, gabbie_totali_disponibili)