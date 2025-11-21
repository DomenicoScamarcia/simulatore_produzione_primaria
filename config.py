from pydantic_settings import BaseSettings

class Configuration(BaseSettings):
    # ===== AVANNOTTERIA (Riproduzione) =====
    # Vasche larvali
    VASCHE_LARVALI_PICCOLE: int = 30
    VASCHE_LARVALI_MEDIE: int = 25
    VASCHE_LARVALI_GRANDI: int = 10

    # Vasche preingrasso (fino a 2g)
    VASCHE_PREINGRASSO: int = 40

    # ===== IMPIANTI DI INGRASSO (6 siti produttivi) =====
    NUMERO_IMPIANTI: int = 6

    # Gabbie in mare (per la maggior parte degli impianti)
    GABBIE_PER_IMPIANTO: int = 20
    VOLUME_GABBIA: int = 1000  # mc per gabbia

    # Impianto a terra Orbetello (capacità maggiore)
    VASCHE_TERRA_ORBETELLO: int = 50
    VOLUME_VASCA_TERRA: int = 200  # mc per vasca

    # ===== PARAMETRI PRODUTTIVI =====
    TASSO_SOPRAVVIVENZA_LARVALE: float = 0.70  # 70%
    TASSO_SOPRAVVIVENZA_PREINGRASSO: float = 0.90  # 90%
    TASSO_SOPRAVVIVENZA_INGRASSO: float = 0.95  # 95%
    EFFICIENZA_OPERATIVA: float = 0.85  # 85%

    # Capacità produttiva annua (tonnellate)
    CAPACITA_PRODUTTIVA_ANNUA: int = 4500  # tonnellate/anno

    # ===== CERTIFICAZIONI =====
    CERTIFICAZIONI: list[str] = ["Global GAP", "Antibiotic Free", "IFS Food"]

settings = Configuration()