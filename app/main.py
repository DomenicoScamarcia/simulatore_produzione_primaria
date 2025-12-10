"""
SIMULAZIONE PROCESSO PRODUTTIVO - GRUPPO DEL PESCE
Avannotteria integrata: produzione di avannotti di spigola, orata e ombrina
Sistema completo dalla nascita alla taglia commerciale
"""
from typing import List, Dict
from app.report_generator import ReportGeneratorGruppoDelPesce
from data_model.lotto_produzione_model import LottoProduzione
from data_model.specie_ittica_model import SpecieIttica
from utils.calcolo_vasche import calcola_vasche_larvali, calcola_gabbie_ingrasso, calcola_vasche_preingrasso
from utils.configurazione import ConfigurazioneGruppoDelPesce
from utils.generazione_lotti import genera_lotti_casuali

# ============================================================================
# SEQUENZE PRODUTTIVE
# ============================================================================

def sequenza_produzione_completa_sequenziale(lotti: List[LottoProduzione], config: ConfigurazioneGruppoDelPesce) -> Dict:
    """
    Simula il processo produttivo completando interamente un lotto alla volta.
    Ogni specie attraversa tutte le fasi (larvale, preingrasso, ingrasso) prima
    che inizi la lavorazione della specie successiva. Calcola vasche necessarie,
    sopravvivenza in ogni fase, tempo totale e tonnellate prodotte per lotto.
    Restituisce un dizionario con metodo, dettagli per specie e tempo totale accumulato.
    """
    risultati = {
        'metodo': 'Sequenziale (dalla nascita alla taglia commerciale)',
        'dettagli': [],
        'tempo_totale': 0
    }

    tempo_accumulato = 0

    for lotto in lotti:
        # FASE 1: LARVALE (Avannotteria)
        vasche_larvali = calcola_vasche_larvali(lotto, config)
        giorni_larvali = lotto.specie.giorni_fase_larvale

        larve_sopravvissute = int(lotto.numero_larve * config.tasso_sopravvivenza_larvale * config.efficienza_operativa)

        # FASE 2: PREINGRASSO (Avannotteria - fino a 2g)
        vasche_preingrasso = calcola_vasche_preingrasso(larve_sopravvissute, config)
        giorni_preingrasso = lotto.specie.giorni_preingrasso

        avannotti_prodotti = int(larve_sopravvissute * config.tasso_sopravvivenza_preingrasso)

        # FASE 3: INGRASSO (Impianti produttivi - fino a taglia commerciale)
        gabbie_ingrasso = calcola_gabbie_ingrasso(avannotti_prodotti, lotto.specie, config)
        giorni_ingrasso = lotto.specie.giorni_ingrasso

        pesci_commerciali = int(avannotti_prodotti * config.tasso_sopravvivenza_ingrasso)

        # Calcola tonnellate prodotte
        peso_totale_kg = (pesci_commerciali * lotto.specie.taglia_commerciale) / 1000
        tonnellate = peso_totale_kg / 1000

        # Tempo totale
        tempo_lotto = giorni_larvali + giorni_preingrasso + giorni_ingrasso
        tempo_accumulato += tempo_lotto

        risultati['dettagli'].append({
            'specie': lotto.specie.nome,
            'larve_seminate': lotto.numero_larve,
            'vasche_larvali': vasche_larvali,
            'vasche_preingrasso': vasche_preingrasso,
            'gabbie_ingrasso': gabbie_ingrasso,
            'giorni_larvali': giorni_larvali,
            'giorni_preingrasso': giorni_preingrasso,
            'giorni_ingrasso': giorni_ingrasso,
            'giorni_totali': tempo_lotto,
            'larve_sopravvissute': larve_sopravvissute,
            'avannotti_2g': avannotti_prodotti,
            'pesci_commerciali': pesci_commerciali,
            'tonnellate_prodotte': round(tonnellate, 2),
            'tasso_sopravvivenza_totale': round((pesci_commerciali/lotto.numero_larve)*100, 1)
        })

    risultati['tempo_totale'] = tempo_accumulato
    return risultati

def sequenza_produzione_integrata_sovrapposta(lotti: List[LottoProduzione], config: ConfigurazioneGruppoDelPesce) -> Dict:
    """
    Simula una produzione sovrapposta dove più lotti vengono gestiti contemporaneamente.
    Un nuovo lotto può iniziare quando il precedente libera le vasche larvali, permettendo
    un uso più efficiente delle risorse. Traccia inizio/fine di ogni fase per ogni lotto
    e calcola il tempo massimo complessivo invece della somma dei tempi. Ottimizza throughput
    sfruttando la parallelizzazione delle fasi produttive tra i diversi lotti.
    """
    risultati = {
        'metodo': 'Integrata Sovrapposta (gestione multi-lotto simultanea)',
        'dettagli': [],
        'tempo_totale': 0
    }

    tempo_massimo = 0
    offset_inizio = 0

    for idx, lotto in enumerate(lotti):
        # FASE 1: LARVALE
        vasche_larvali = calcola_vasche_larvali(lotto, config)
        giorni_larvali = lotto.specie.giorni_fase_larvale

        larve_sopravvissute = int(lotto.numero_larve * config.tasso_sopravvivenza_larvale * config.efficienza_operativa)

        # FASE 2: PREINGRASSO
        vasche_preingrasso = calcola_vasche_preingrasso(larve_sopravvissute, config)
        giorni_preingrasso = lotto.specie.giorni_preingrasso

        avannotti_prodotti = int(larve_sopravvissute * config.tasso_sopravvivenza_preingrasso)

        # FASE 3: INGRASSO
        gabbie_ingrasso = calcola_gabbie_ingrasso(avannotti_prodotti, lotto.specie, config)
        giorni_ingrasso = lotto.specie.giorni_ingrasso

        pesci_commerciali = int(avannotti_prodotti * config.tasso_sopravvivenza_ingrasso)

        # Calcola tonnellate
        peso_totale_kg = (pesci_commerciali * lotto.specie.taglia_commerciale) / 1000
        tonnellate = peso_totale_kg / 1000

        # Con sovrapposizione: ogni lotto inizia quando il precedente
        # ha liberato le vasche larvali
        inizio_lotto = offset_inizio
        fine_larvale = inizio_lotto + giorni_larvali
        fine_preingrasso = fine_larvale + giorni_preingrasso
        fine_ingrasso = fine_preingrasso + giorni_ingrasso

        # Il prossimo lotto può iniziare quando questo libera le vasche larvali
        offset_inizio = fine_larvale

        tempo_massimo = max(tempo_massimo, fine_ingrasso)

        risultati['dettagli'].append({
            'specie': lotto.specie.nome,
            'larve_seminate': lotto.numero_larve,
            'vasche_larvali': vasche_larvali,
            'vasche_preingrasso': vasche_preingrasso,
            'gabbie_ingrasso': gabbie_ingrasso,
            'inizio_giorno': inizio_lotto,
            'fine_larvale_giorno': fine_larvale,
            'fine_preingrasso_giorno': fine_preingrasso,
            'fine_ingrasso_giorno': fine_ingrasso,
            'giorni_larvali': giorni_larvali,
            'giorni_preingrasso': giorni_preingrasso,
            'giorni_ingrasso': giorni_ingrasso,
            'larve_sopravvissute': larve_sopravvissute,
            'avannotti_2g': avannotti_prodotti,
            'pesci_commerciali': pesci_commerciali,
            'tonnellate_prodotte': round(tonnellate, 2),
            'tasso_sopravvivenza_totale': round((pesci_commerciali/lotto.numero_larve)*100, 1)
        })

    risultati['tempo_totale'] = tempo_massimo
    return risultati

# ============================================================================
# 6. OUTPUT E REPORTING
# ============================================================================

def stampa_risultati(risultati: Dict):
    """
    Formatta e stampa su console i risultati della simulazione in modo strutturato.
    # Visualizza per ogni specie: numeri (larve, avannotti, pesci, tonnellate),
    # risorse utilizzate (vasche e gabbie), tempi di ogni fase e performance complessive.
    # Include anche totali aggregati di produzione e tempo complessivo del ciclo.
    """
    print(f"\n{'='*80}")
    print(f"RISULTATI SIMULAZIONE - {risultati['metodo']}")
    print(f"{'='*80}")

    for dettaglio in risultati['dettagli']:
        print(f"\n Specie: {dettaglio['specie']}")
        print(f"    NUMERI:")
        print(f"      Larve seminate: {dettaglio['larve_seminate']:,} larve")
        print(f"      Avannotti prodotti (2g): {dettaglio['avannotti_2g']:,}")
        print(f"      Pesci commerciali: {dettaglio['pesci_commerciali']:,}")
        print(f"      Tonnellate prodotte: {dettaglio['tonnellate_prodotte']} t")

        print(f"\n    RISORSE UTILIZZATE:")
        print(f"      Vasche larvali: {dettaglio['vasche_larvali']}")
        print(f"      Vasche preingrasso: {dettaglio['vasche_preingrasso']}")
        print(f"      Gabbie ingrasso: {dettaglio['gabbie_ingrasso']}")

        print(f"\n     TEMPI:")
        if 'inizio_giorno' in dettaglio:
            print(f"      Inizio ciclo: giorno {dettaglio['inizio_giorno']}")
            print(f"      Fine larvale: giorno {dettaglio['fine_larvale_giorno']} ({dettaglio['giorni_larvali']}gg)")
            print(f"      Fine preingrasso: giorno {dettaglio['fine_preingrasso_giorno']} ({dettaglio['giorni_preingrasso']}gg)")
            print(f"      Fine ingrasso: giorno {dettaglio['fine_ingrasso_giorno']} ({dettaglio['giorni_ingrasso']}gg)")
        else:
            print(f"      Fase larvale: {dettaglio['giorni_larvali']} giorni")
            print(f"      Fase preingrasso: {dettaglio['giorni_preingrasso']} giorni")
            print(f"      Fase ingrasso: {dettaglio['giorni_ingrasso']} giorni")
            print(f"      Tempo totale: {dettaglio['giorni_totali']} giorni")

        print(f"\n    PERFORMANCE:")
        print(f"      Tasso sopravvivenza totale: {dettaglio['tasso_sopravvivenza_totale']}%")

    print(f"\n{'='*80}")
    print(f"️  TEMPO TOTALE CICLO PRODUTTIVO: {risultati['tempo_totale']} giorni")

    # Calcola produzione totale
    tot_tonnellate = sum(d['tonnellate_prodotte'] for d in risultati['dettagli'])
    tot_pesci = sum(d['pesci_commerciali'] for d in risultati['dettagli'])
    print(f" PRODUZIONE TOTALE: {tot_tonnellate:.2f} tonnellate ({tot_pesci:,} pesci)")
    print(f"{'='*80}\n")

# ============================================================================
# 7. FUNZIONE PRINCIPALE
# ============================================================================

def main():
    """
    Punto di ingresso principale del programma. Configura l'ambiente di simulazione,
    # definisce le tre specie ittiche (Spigola, Orata, Ombrina) con i loro parametri
    # specifici, inizializza la configurazione dell'impianto del Gruppo Del Pesce,
    # genera lotti casuali, esegue entrambe le simulazioni (sequenziale e sovrapposta),
    # genera il report grafico PNG, e stampa il confronto dettagliato tra i metodi
    # includendo analisi della produzione annuale e raggiungimento del target aziendale.
    """

    print("\n" + "="*80)
    print(" SIMULAZIONE PRODUZIONE - GRUPPO DEL PESCE")
    print("   Filiera integrata: dalla nascita alla taglia commerciale")
    print("   Sede: Guidonia (RM) - 6 impianti produttivi in Italia")
    print("="*80)

    # Definisci le tre specie principali del Gruppo Del Pesce
    specie_ittiche = [
        SpecieIttica(
            nome="Spigola/Branzino (Dicentrarchus labrax)",
            densita_semina_larvale=100,  # larve/litro
            densita_preingrasso=400,  # avannotti/mc
            densita_ingrasso=15,  # pesci/mc
            giorni_fase_larvale=40,
            giorni_preingrasso=70,  # fino a 2g
            giorni_ingrasso=450,  # fino a 350-400g
            taglia_vendita_avannotto=2.0,  # grammi
            taglia_commerciale=380.0,  # grammi
            temperatura_ottimale=18.0
        ),
        SpecieIttica(
            nome="Orata (Sparus aurata)",
            densita_semina_larvale=120,  # larve/litro
            densita_preingrasso=450,  # avannotti/mc
            densita_ingrasso=18,  # pesci/mc
            giorni_fase_larvale=45,
            giorni_preingrasso=65,  # fino a 2g
            giorni_ingrasso=420,  # fino a 300-350g
            taglia_vendita_avannotto=2.0,  # grammi
            taglia_commerciale=330.0,  # grammi
            temperatura_ottimale=20.0
        ),
        SpecieIttica(
            nome="Ombrina/Meagre (Argyrosomus regius)",
            densita_semina_larvale=80,  # larve/litro
            densita_preingrasso=350,  # avannotti/mc
            densita_ingrasso=12,  # pesci/mc (più grandi)
            giorni_fase_larvale=35,
            giorni_preingrasso=80,  # fino a 2g
            giorni_ingrasso=480,  # fino a 800g-1kg
            taglia_vendita_avannotto=2.0,  # grammi
            taglia_commerciale=900.0,  # grammi
            temperatura_ottimale=19.0
        )
    ]

    # Configura il gruppo produttivo
    config = ConfigurazioneGruppoDelPesce()

    print(f"\n CONFIGURAZIONE GRUPPO DEL PESCE:")
    print(f"\n    AVANNOTTERIA (Riproduzione):")
    print(f"      - Vasche larvali piccole (2-5mc): {config.vasche_larvali_piccole}")
    print(f"      - Vasche larvali medie (10mc): {config.vasche_larvali_medie}")
    print(f"      - Vasche larvali grandi (20mc): {config.vasche_larvali_grandi}")
    print(f"      - Vasche preingrasso (40mc): {config.vasche_preingrasso}")

    print(f"\n    IMPIANTI PRODUTTIVI:")
    print(f"      - Numero impianti: {config.numero_impianti}")
    print(f"      - Gabbie per impianto: {config.gabbie_per_impianto}")
    print(f"      - Volume gabbia: {config.volume_gabbia} mc")
    print(f"      - Impianto terra Orbetello: {config.vasche_terra_orbetello} vasche da {config.volume_vasca_terra} mc")

    print(f"\n    CAPACITÀ E PARAMETRI:")
    print(f"      - Capacità produttiva annua: {config.capacita_produttiva_annua:,} tonnellate/anno")
    print(f"      - Sopravvivenza larvale: {config.tasso_sopravvivenza_larvale*100}%")
    print(f"      - Sopravvivenza preingrasso: {config.tasso_sopravvivenza_preingrasso*100}%")
    print(f"      - Sopravvivenza ingrasso: {config.tasso_sopravvivenza_ingrasso*100}%")
    print(f"      - Efficienza operativa: {config.efficienza_operativa*100}%")


    # Genera lotti casuali
    print("\n Generazione lotti di produzione...")
    lotti = genera_lotti_casuali(specie_ittiche, min_larve=1000000, max_larve=2500000)

    print("\n Lotti generati:")
    for lotto in lotti:
        print(f"   - {lotto.specie.nome}")
        print(f"     Larve da seminare: {lotto.numero_larve:,} larve")
        print(f"     Densità larvale: {lotto.specie.densita_semina_larvale} larve/litro")
        print(f"     Taglia commerciale target: {lotto.specie.taglia_commerciale}g")

    # SIMULAZIONE 1: Sequenziale
    risultati_seq = sequenza_produzione_completa_sequenziale(lotti, config)
    # SIMULAZIONE 2: Sovrapposta (più efficiente)
    risultati_sov = sequenza_produzione_integrata_sovrapposta(lotti, config)

    # GENERA REPORT GRAFICO
    report_generator = ReportGeneratorGruppoDelPesce(config)
    file_png = report_generator.genera_report_completo(
        risultati_seq,
        risultati_sov,
        lotti,
        nome_file="report_produzione.png"
    )

    print(f" Report generato: {file_png}")

    # Confronto finale
    print("\n" + "="*80)
    print(" CONFRONTO TRA METODI DI GESTIONE PRODUTTIVA")
    print("="*80)
    print(f"Metodo Sequenziale: {risultati_seq['tempo_totale']} giorni")
    print(f"Metodo Integrato Sovrapposto: {risultati_sov['tempo_totale']} giorni")

    differenza = risultati_seq['tempo_totale'] - risultati_sov['tempo_totale']
    if differenza > 0:
        percentuale = (differenza / risultati_seq['tempo_totale']) * 100
        print(f"\n RISPARMIO con metodo integrato sovrapposto: {differenza} giorni ({percentuale:.1f}%)")
        print(f"   ✓ Ottimizzazione uso avannotteria")
        print(f"   ✓ Distribuzione efficiente su 6 impianti")
        print(f"   ✓ Maggiore flessibilità produttiva")

    # Analisi produzione
    tot_tonnellate_seq = sum(d['tonnellate_prodotte'] for d in risultati_seq['dettagli'])
    print(f"\n PRODUZIONE ANNUALE STIMATA:")
    print(f"   Tonnellate per ciclo: {tot_tonnellate_seq:.2f} t")
    cicli_anno = 365 / risultati_sov['tempo_totale']
    produzione_annua = tot_tonnellate_seq * cicli_anno
    print(f"   Cicli possibili/anno: {cicli_anno:.1f}")
    print(f"   Produzione annua stimata: {produzione_annua:.0f} tonnellate/anno")
    print(f"   Target aziendale: {config.capacita_produttiva_annua} tonnellate/anno")

    percentuale_target = (produzione_annua / config.capacita_produttiva_annua) * 100
    print(f"   Raggiungimento target: {percentuale_target:.1f}%")

    print("\n" + "=" * 80)
    print(f"Report grafico completo salvato in: '{file_png}'.")
    print(
        "Il PNG contiene tutti i grafici per un approfondimento dettagliato: confronto tra i metodi, trend dei tassi di sopravvivenza per fase, produzione per specie e utilizzo delle risorse.")
    print(f"Apri '{file_png}' per visualizzare le figure e i dettagli analitici.")
    print("=" * 80 + "\n")


# Esegui il programma
if __name__ == "__main__":
    main()