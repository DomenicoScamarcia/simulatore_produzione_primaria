from dataclasses import dataclass
from data_model.specie_ittica_model import SpecieIttica


@dataclass
class LottoProduzione:
    """Rappresenta un lotto di produzione completo"""
    specie: SpecieIttica
    numero_larve: int  # numero totale di larve da produrre
    fase_corrente: str = "larvale"  # larvale, preingrasso, ingrasso
    larve_sopravvissute: int = 0
    avannotti_prodotti: int = 0
    pesci_commerciali: int = 0
    giorni_totali: int = 0