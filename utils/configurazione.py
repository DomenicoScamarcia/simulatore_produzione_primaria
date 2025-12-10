from config import settings


class ConfigurazioneGruppoDelPesce:

    def __init__(self):
        # ===== AVANNOTTERIA (Riproduzione) =====
        # Vasche larvali
        self.vasche_larvali_piccole = settings.VASCHE_LARVALI_PICCOLE
        self.vasche_larvali_medie = settings.VASCHE_LARVALI_MEDIE
        self.vasche_larvali_grandi = settings.VASCHE_LARVALI_GRANDI

        # Vasche preingrasso (fino a 2g)
        self.vasche_preingrasso = settings.VASCHE_PREINGRASSO

        # ===== IMPIANTI DI INGRASSO (6 siti produttivi) =====
        self.numero_impianti = settings.NUMERO_IMPIANTI

        # Gabbie in mare (per la maggior parte degli impianti)
        self.gabbie_per_impianto = settings.GABBIE_PER_IMPIANTO
        self.volume_gabbia = settings.VOLUME_GABBIA

        # Impianto a terra Orbetello (capacità maggiore)
        self.vasche_terra_orbetello = settings.VASCHE_TERRA_ORBETELLO
        self.volume_vasca_terra = settings.VOLUME_VASCA_TERRA

        # ===== PARAMETRI PRODUTTIVI =====
        self.tasso_sopravvivenza_larvale = settings.TASSO_SOPRAVVIVENZA_LARVALE
        self.tasso_sopravvivenza_preingrasso = settings.TASSO_SOPRAVVIVENZA_PREINGRASSO
        self.tasso_sopravvivenza_ingrasso = settings.TASSO_SOPRAVVIVENZA_INGRASSO
        self.efficienza_operativa = settings.EFFICIENZA_OPERATIVA

        # Capacità produttiva annua (tonnellate)
        self.capacita_produttiva_annua = settings.CAPACITA_PRODUTTIVA_ANNUA