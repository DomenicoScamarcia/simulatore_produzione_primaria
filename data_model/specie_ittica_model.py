from dataclasses import dataclass


@dataclass
class SpecieIttica:
    """Rappresenta una specie ittica allevata"""
    nome: str
    densita_semina_larvale: int  # larve per litro
    densita_preingrasso: int  # avannotti per mc in fase preingrasso
    densita_ingrasso: int  # pesci per mc in fase ingrasso finale
    giorni_fase_larvale: int  # giorni in fase larvale
    giorni_preingrasso: int  # giorni in fase preingrasso (fino a 2g)
    giorni_ingrasso: int  # giorni fino a taglia commerciale
    taglia_vendita_avannotto: float  # grammi
    taglia_commerciale: float  # grammi
    temperatura_ottimale: float  # °C