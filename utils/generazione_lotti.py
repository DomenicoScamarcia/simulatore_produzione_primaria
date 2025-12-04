import random
from typing import List
from data_model.lotto_produzione_model import LottoProduzione
from data_model.specie_ittica_model import SpecieIttica


def genera_lotti_casuali(specie_disponibili: List[SpecieIttica], min_larve: int, max_larve: int) -> List[LottoProduzione]:
    """
    Genera lotti di produzione con quantità casuali di larve

    Args:
        specie_disponibili: Lista di specie ittiche disponibili
        min_larve: Numero minimo di larve da seminare
        max_larve: Numero massimo di larve da seminare

    Returns:
        Lista di lotti di produzione con quantità casuali
    """
    lotti = []
    for specie in specie_disponibili:
        numero_larve = random.randint(min_larve, max_larve)
        lotti.append(LottoProduzione(specie, numero_larve))
    return lotti