import random
from typing import List
from data_model.lotto_produzione_model import LottoProduzione
from data_model.specie_ittica_model import SpecieIttica


def genera_lotti_casuali(specie_disponibili: List[SpecieIttica], min_larve: int, max_larve: int) -> List[LottoProduzione]:
    """
    Genera lotti di produzione con quantità casuali di larve
    """

    lotti = []
    for specie in specie_disponibili:
        numero_larve = random.randint(min_larve, max_larve)
        lotti.append(LottoProduzione(specie, numero_larve))
    return lotti