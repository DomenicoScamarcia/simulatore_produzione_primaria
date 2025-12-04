
from data_model.lotto_produzione_model import LottoProduzione
from data_model.specie_ittica_model import SpecieIttica
from utils.configurazione import ConfigurazioneGruppoDelPesce


def calcola_vasche_larvali(lotto: LottoProduzione, config: ConfigurazioneGruppoDelPesce) -> int:
    """Calcola il numero di vasche larvali necessarie"""
    densita = lotto.specie.densita_semina_larvale

    # Usa le vasche piccole, medie, grandi
    capacita_media = 8000  # litri (media tra i vari tipi)
    vasche_totali = config.vasche_larvali_piccole + config.vasche_larvali_medie + config.vasche_larvali_grandi

    larve_per_vasca = capacita_media * densita
    vasche_necessarie = int(lotto.numero_larve / larve_per_vasca) + 1

    return min(vasche_necessarie, vasche_totali)

def calcola_vasche_preingrasso(post_larve: int, config: ConfigurazioneGruppoDelPesce) -> int:
    """Calcola vasche necessarie per il preingrasso"""
    capacita_vasca = 40000  # litri
    densita = 400  # avannotti per mc (ridotta per benessere)

    post_larve_per_vasca = (capacita_vasca / 1000) * densita
    vasche_necessarie = int(post_larve / post_larve_per_vasca) + 1

    return min(vasche_necessarie, config.vasche_preingrasso)

def calcola_gabbie_ingrasso(avannotti: int, specie: SpecieIttica, config: ConfigurazioneGruppoDelPesce) -> int:
    """Calcola gabbie necessarie per fase di ingrasso fino a taglia commerciale"""
    densita = specie.densita_ingrasso
    volume_gabbia = config.volume_gabbia

    pesci_per_gabbia = volume_gabbia * densita
    gabbie_necessarie = int(avannotti / pesci_per_gabbia) + 1

    gabbie_totali_disponibili = config.gabbie_per_impianto * config.numero_impianti
    return min(gabbie_necessarie, gabbie_totali_disponibili)