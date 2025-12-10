"""
GENERATORE DI REPORT GRAFICI - GRUPPO DEL PESCE
Classe per generare report visivi con grafici e tabelle in formato PNG
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
from typing import Dict, List
from datetime import datetime


class ReportGeneratorGruppoDelPesce:
    """
    Genera report grafici completi con layout pulito e ordinato
    """

    def __init__(self, config):
        """
        Inizializza il generatore di report configurando i colori per i grafici,
        lo stile matplotlib (font, dimensioni testo, spessori), e disabilitando
        i warning relativi ai glifi mancanti. Memorizza la configurazione
        dell'impianto per calcoli successivi (es. capacità produttiva annua).
        """
        self.config = config
        self.colors = {
            'primary': '#2563eb',
            'secondary': '#7c3aed',
            'success': '#16a34a',
            'warning': '#ea580c',
            'danger': '#dc2626',
            'seq': '#dc2626',      # Rosso per sequenziale
            'sov': '#16a34a',      # Verde per sovrapposto
            'spigola': '#0891b2',
            'orata': '#f59e0b',
            'ombrina': '#059669'
        }

        # Configura lo stile matplotlib
        plt.style.use('default')
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
        plt.rcParams['font.size'] = 11
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.titleweight'] = 'bold'
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.titlesize'] = 16
        plt.rcParams['figure.titleweight'] = 'bold'

        # Disabilita warning
        import warnings
        warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

    def genera_report_completo(self, risultati_seq: Dict, risultati_sov: Dict, lotti: List, nome_file: str = None) -> str:
        """
        Crea un report visivo completo in formato PNG con 7 sezioni:
        1) KPI globali (larve, pesci, tonnellate, sopravvivenza, risparmio)
        2) Confronto diretto tra metodo sequenziale e sovrapposto
        3) Dettagli metodo sequenziale con tempi per specie
        4) Dettagli metodo sovrapposto con timeline delle fasi
        5) Distribuzione produzione per specie (grafico a torta)
        6) Risorse utilizzate (vasche e gabbie per specie)
        7) Tabella riepilogo comparativo con tutti i dati
        Salva il file nella cartella "report" e restituisce il percorso assoluto.
        """
        if nome_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_file = f"report_gruppo_del_pesce_{timestamp}.png"

        # Crea figura più grande con più spazio
        fig = plt.figure(figsize=(24, 16))
        fig.patch.set_facecolor('white')

        # Titolo principale
        fig.suptitle('REPORT SIMULAZIONE PRODUZIONE - GRUPPO DEL PESCE', fontsize=22, fontweight='bold', y=0.97)

        # Sottotitolo
        fig.text(0.5, 0.945, 'Filiera integrata: dalla nascita alla taglia commerciale | Guidonia (RM)', ha='center', fontsize=13, style='italic', color='#4b5563')

        # Crea griglia con più spazio
        gs = GridSpec(5, 2, figure=fig, hspace=0.5, wspace=0.35, left=0.06, right=0.94, top=0.92, bottom=0.05)

        # 1. KPI GLOBALI (riga 1, colonne 1-2)
        ax1 = fig.add_subplot(gs[0, :])
        self._crea_kpi_globali(ax1, lotti, risultati_seq, risultati_sov)

        # 2. CONFRONTO DIRETTO SEQUENZIALE VS SOVRAPPOSTO (riga 2, colonne 1-2)
        ax2 = fig.add_subplot(gs[1, :])
        self._crea_confronto_principale(ax2, risultati_seq, risultati_sov)

        # 3. DETTAGLI METODO SEQUENZIALE (riga 3, colonna 1)
        ax3 = fig.add_subplot(gs[2, 0])
        self._crea_dettagli_sequenziale(ax3, risultati_seq)

        # 4. DETTAGLI METODO SOVRAPPOSTO (riga 3, colonna 2)
        ax4 = fig.add_subplot(gs[2, 1])
        self._crea_dettagli_sovrapposto(ax4, risultati_sov)

        # 5. DISTRIBUZIONE PRODUZIONE (riga 4, colonna 1)
        ax5 = fig.add_subplot(gs[3, 0])
        self._crea_distribuzione_specie(ax5, risultati_sov)

        # 6. RISORSE UTILIZZATE (riga 4, colonna 2)
        ax6 = fig.add_subplot(gs[3, 1])
        self._crea_grafico_risorse(ax6, risultati_sov)

        # 7. TABELLA COMPARATIVA (riga 5, colonne 1-2)
        ax7 = fig.add_subplot(gs[4, :])
        self._crea_tabella_riepilogo(ax7, risultati_seq, risultati_sov)

        # --- Salva figura nella cartella "report" situata allo stesso livello di "app" ---
        # Cartella report: ../report relative al file current (app/report_generator.py)
        report_dir = Path(__file__).resolve().parent.parent / "report"
        report_dir.mkdir(parents=True, exist_ok=True)

        # Assicura che il nome file non contenga slash imprevisti
        nome_file = Path(nome_file).name

        file_path = report_dir / nome_file
        plt.savefig(file_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close()

        # Ritorna il percorso assoluto del file come stringa
        return str(file_path)

    def _crea_kpi_globali(self, ax, lotti, risultati_seq, risultati_sov):
        """
        Crea una dashboard con 5 KPI principali visualizzati come card colorate:
        larve seminate, pesci prodotti, tonnellate, tasso di sopravvivenza totale
        e risparmio di tempo tra i due metodi. Ogni card ha un colore distintivo,
        un'etichetta in alto e il valore numerico grande al centro. Le card sono
        distribuite orizzontalmente nella parte superiore del report.
        """
        ax.axis('off')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        # Calcola KPI
        totale_larve = sum(l.numero_larve for l in lotti)
        totale_pesci = sum(d['pesci_commerciali'] for d in risultati_sov['dettagli'])
        totale_tonnellate = sum(d['tonnellate_prodotte'] for d in risultati_sov['dettagli'])
        tasso_sopravvivenza = (totale_pesci / totale_larve * 100)

        risparmio = risultati_seq['tempo_totale'] - risultati_sov['tempo_totale']
        risparmio_perc = (risparmio / risultati_seq['tempo_totale'] * 100)

        kpis = [
            ('LARVE SEMINATE', f'{totale_larve:,}', self.colors['primary']),
            ('PESCI PRODOTTI', f'{totale_pesci:,}', self.colors['success']),
            ('TONNELLATE', f'{totale_tonnellate:.1f} t', self.colors['warning']),
            ('SOPRAVVIVENZA', f'{tasso_sopravvivenza:.1f}%', self.colors['secondary']),
            ('RISPARMIO TEMPO', f'{risparmio} gg ({risparmio_perc:.0f}%)', self.colors['sov'])
        ]

        card_width = 0.18
        spacing = 0.205
        start_x = 0.01

        for i, (label, value, color) in enumerate(kpis):
            x = start_x + i * spacing

            # Box con bordo
            rect = mpatches.FancyBboxPatch(
                (x, 0.15), card_width, 0.7,
                boxstyle="round,pad=0.015",
                facecolor=color,
                edgecolor=color,
                alpha=0.15,
                linewidth=2,
                transform=ax.transAxes
            )
            ax.add_patch(rect)

            # Label
            ax.text(x + card_width/2, 0.75, label,
                   ha='center', va='center', fontsize=11,
                   fontweight='bold', color='#374151',
                   transform=ax.transAxes)

            # Value
            ax.text(x + card_width/2, 0.4, value,
                   ha='center', va='center', fontsize=18,
                   fontweight='bold', color=color,
                   transform=ax.transAxes)

    def _crea_confronto_principale(self, ax, risultati_seq, risultati_sov):
        """
        Crea il grafico di confronto principale con due barre orizzontali grandi
        che rappresentano i tempi totali dei due metodi produttivi. Il metodo
        sequenziale è in rosso (sopra), il metodo sovrapposto in verde (sotto).
        Include etichette sui lati, valori sui centri delle barre, e una freccia
        bidirezionale centrale che evidenzia il risparmio in giorni e percentuale.
        Questo grafico è il punto focale del report per il confronto immediato.
        """
        ax.set_xlim(0, max(risultati_seq['tempo_totale'], risultati_sov['tempo_totale']) * 1.2)
        ax.set_ylim(-0.5, 1.5)

        # Barre orizzontali grandi
        bar_height = 0.35

        # SEQUENZIALE (sopra)
        ax.barh(1, risultati_seq['tempo_totale'], height=bar_height,
               color=self.colors['seq'], alpha=0.7, edgecolor='black', linewidth=2,
               label='Metodo Sequenziale')

        # Testo sulla barra
        ax.text(risultati_seq['tempo_totale']/2, 1,
               f"SEQUENZIALE: {risultati_seq['tempo_totale']} giorni",
               ha='center', va='center', fontsize=14, fontweight='bold',
               color='white')

        # SOVRAPPOSTO (sotto)
        ax.barh(0, risultati_sov['tempo_totale'], height=bar_height,
               color=self.colors['sov'], alpha=0.7, edgecolor='black', linewidth=2,
               label='Metodo Sovrapposto')

        # Testo sulla barra
        ax.text(risultati_sov['tempo_totale']/2, 0,
               f"SOVRAPPOSTO: {risultati_sov['tempo_totale']} giorni",
               ha='center', va='center', fontsize=14, fontweight='bold',
               color='white')

        # Etichette metodi
        ax.text(-50, 1, 'METODO\nSEQUENZIALE',
               ha='right', va='center', fontsize=12, fontweight='bold',
               color=self.colors['seq'])

        ax.text(-50, 0, 'METODO\nSOVRAPPOSTO\n(OTTIMALE)',
               ha='right', va='center', fontsize=12, fontweight='bold',
               color=self.colors['sov'])

        # Freccia risparmio
        risparmio = risultati_seq['tempo_totale'] - risultati_sov['tempo_totale']
        percentuale = (risparmio / risultati_seq['tempo_totale'] * 100)

        ax.annotate('',
                   xy=(risultati_sov['tempo_totale'], 0.5),
                   xytext=(risultati_seq['tempo_totale'], 0.5),
                   arrowprops=dict(arrowstyle='<->', color=self.colors['sov'], lw=3, mutation_scale=20))

        ax.text((risultati_seq['tempo_totale'] + risultati_sov['tempo_totale'])/2, 0.6,
               f'RISPARMIO: {risparmio} giorni ({percentuale:.1f}%)',
               ha='center', va='bottom', fontsize=13, fontweight='bold',
               color=self.colors['sov'],
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=self.colors['sov'], linewidth=2))

        ax.set_xlabel('TEMPO TOTALE DI PRODUZIONE (giorni)', fontsize=13, fontweight='bold')
        ax.set_yticks([])
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_title('CONFRONTO TEMPI PRODUTTIVI: SEQUENZIALE VS SOVRAPPOSTO', fontsize=15, fontweight='bold', pad=20)

        # Bordo
        for spine in ax.spines.values():
            spine.set_edgecolor('#d1d5db')
            spine.set_linewidth(2)

    def _crea_dettagli_sequenziale(self, ax, risultati):
        """
        Visualizza i dettagli del metodo sequenziale con un grafico a barre
        orizzontali che mostra i giorni totali necessari per ogni specie
        (Spigola, Orata, Ombrina). Ogni barra ha un colore distintivo per specie,
        i valori sono mostrati a destra delle barre, e il bordo del grafico è
        rosso per identificarlo come relativo al metodo sequenziale. Include
        il tempo totale nel titolo.
        """
        dettagli = risultati['dettagli']

        specie_nomi = []
        giorni_totali = []

        for d in dettagli:
            nome = d['specie'].split('/')[0] if '/' in d['specie'] else d['specie']
            specie_nomi.append(nome)
            giorni = d.get('giorni_totali', d.get('fine_ingrasso_giorno', 0))
            giorni_totali.append(giorni)

        # Grafico a barre orizzontali
        y_pos = np.arange(len(specie_nomi))
        colors = [self.colors['spigola'], self.colors['orata'], self.colors['ombrina']]

        bars = ax.barh(y_pos, giorni_totali, color=colors, alpha=0.8,
                      edgecolor='black', linewidth=1.5)

        # Valori sulle barre
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + 20, bar.get_y() + bar.get_height()/2,
                   f'{int(giorni_totali[i])} gg',
                   ha='left', va='center', fontsize=11, fontweight='bold')

        ax.set_yticks(y_pos)
        ax.set_yticklabels(specie_nomi, fontsize=11, fontweight='bold')
        ax.set_xlabel('Giorni per Specie', fontsize=11, fontweight='bold')
        ax.set_title(f'METODO SEQUENZIALE\nTempo totale: {risultati["tempo_totale"]} giorni',
                    fontsize=13, fontweight='bold', pad=15,
                    color=self.colors['seq'])
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.invert_yaxis()

        # Bordo rosso
        for spine in ax.spines.values():
            spine.set_edgecolor(self.colors['seq'])
            spine.set_linewidth=3

    def _crea_dettagli_sovrapposto(self, ax, risultati):
        """
        Crea una timeline Gantt che visualizza la sovrapposizione temporale
        dei lotti nel metodo sovrapposto. Per ogni specie mostra tre segmenti
        di barra con opacità crescente che rappresentano le tre fasi produttive:
        larvale (chiara), preingrasso (media), ingrasso (scura). La timeline
        permette di vedere come i lotti si sovrappongono nel tempo, ottimizzando
        l'uso delle risorse. Il bordo verde identifica il metodo sovrapposto.
        """
        dettagli = risultati['dettagli']

        y_pos = np.arange(len(dettagli))
        colors = [self.colors['spigola'], self.colors['orata'], self.colors['ombrina']]

        for i, det in enumerate(dettagli):
            specie_nome = det['specie'].split('/')[0] if '/' in det['specie'] else det['specie']

            # Fase larvale (chiara)
            ax.barh(i, det['giorni_larvali'], left=det['inizio_giorno'],
                   color=colors[i], alpha=0.3, edgecolor='black', linewidth=1.5,
                   label='Larvale' if i == 0 else '')

            # Fase preingrasso (media)
            ax.barh(i, det['giorni_preingrasso'], left=det['fine_larvale_giorno'],
                   color=colors[i], alpha=0.6, edgecolor='black', linewidth=1.5,
                   label='Preingrasso' if i == 0 else '')

            # Fase ingrasso (scura)
            ax.barh(i, det['giorni_ingrasso'], left=det['fine_preingrasso_giorno'],
                   color=colors[i], alpha=0.9, edgecolor='black', linewidth=1.5,
                   label='Ingrasso' if i == 0 else '')

            # Nome specie
            ax.text(-15, i, specie_nome,
                   ha='right', va='center', fontsize=11, fontweight='bold')

        ax.set_yticks(y_pos)
        ax.set_yticklabels([''] * len(dettagli))
        ax.set_xlabel('Timeline (giorni)', fontsize=11, fontweight='bold')
        ax.set_title(f'METODO SOVRAPPOSTO (OTTIMALE)\nTempo totale: {risultati["tempo_totale"]} giorni',
                    fontsize=13, fontweight='bold', pad=15,
                    color=self.colors['sov'])
        ax.legend(loc='upper right', framealpha=0.95, fontsize=10)
        ax.grid(axis='x', alpha=0.3, linestyle='--')

        # Bordo verde
        for spine in ax.spines.values():
            spine.set_edgecolor(self.colors['sov'])
            spine.set_linewidth(3)

    def _crea_distribuzione_specie(self, ax, risultati):
        """
        Crea un grafico a torta che mostra la distribuzione percentuale della
        produzione in tonnellate tra le tre specie ittiche. Ogni spicchio ha
        un colore distintivo (azzurro per spigola, arancione per orata, verde
        per ombrina), è leggermente esploso per migliore leggibilità, e mostra
        il nome della specie e la percentuale. Utile per capire quali specie
        contribuiscono maggiormente alla produzione totale.
        """
        specie = []
        tonnellate = []

        for d in risultati['dettagli']:
            nome = d['specie'].split('/')[0] if '/' in d['specie'] else d['specie']
            specie.append(nome)
            tonnellate.append(d['tonnellate_prodotte'])

        colors = [self.colors['spigola'], self.colors['orata'], self.colors['ombrina']]

        wedges, texts, autotexts = ax.pie(
            tonnellate,
            labels=specie,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            explode=(0.05, 0.05, 0.05),
            textprops={'fontsize': 12, 'fontweight': 'bold'}
        )

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(13)
            autotext.set_fontweight('bold')

        ax.set_title('DISTRIBUZIONE PRODUZIONE\nper Specie (tonnellate)', fontsize=13, fontweight='bold', pad=15)

    def _crea_grafico_risorse(self, ax, risultati):
        """
        Visualizza le risorse utilizzate (vasche larvali, vasche preingrasso,
        gabbie ingrasso) per ogni specie con un grafico a barre raggruppate.
        Per ogni specie ci sono tre barre affiancate di colori diversi che
        rappresentano i tre tipi di risorse. Questo permette di confrontare
        rapidamente l'utilizzo delle risorse tra le diverse specie e capire
        quali richiedono più infrastrutture in ciascuna fase produttiva.
        """
        specie_nomi = []
        vasche_larvali = []
        vasche_preingrasso = []
        gabbie_ingrasso = []

        for d in risultati['dettagli']:
            nome = d['specie'].split('/')[0] if '/' in d['specie'] else d['specie']
            specie_nomi.append(nome)
            vasche_larvali.append(d['vasche_larvali'])
            vasche_preingrasso.append(d['vasche_preingrasso'])
            gabbie_ingrasso.append(d['gabbie_ingrasso'])

        x = np.arange(len(specie_nomi))
        width = 0.25

        ax.bar(x - width, vasche_larvali, width, label='Vasche Larvali',
              color=self.colors['primary'], alpha=0.8, edgecolor='black', linewidth=1)
        ax.bar(x, vasche_preingrasso, width, label='Vasche Preingrasso',
              color=self.colors['warning'], alpha=0.8, edgecolor='black', linewidth=1)
        ax.bar(x + width, gabbie_ingrasso, width, label='Gabbie Ingrasso',
              color=self.colors['success'], alpha=0.8, edgecolor='black', linewidth=1)

        ax.set_ylabel('Numero Unità', fontsize=11, fontweight='bold')
        ax.set_xlabel('Specie', fontsize=11, fontweight='bold')
        ax.set_title('RISORSE UTILIZZATE\nper Fase e Specie',
                    fontsize=13, fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(specie_nomi, fontsize=11, fontweight='bold')
        ax.legend(fontsize=10, loc='upper left')
        ax.grid(axis='y', alpha=0.3, linestyle='--')

    def _crea_tabella_riepilogo(self, ax, risultati_seq, risultati_sov):
        """
        Genera una tabella riepilogativa completa con 8 colonne che confronta
        i due metodi produttivi per ogni specie. Include: nome specie, larve
        seminate, pesci commerciali prodotti, tonnellate, tasso di sopravvivenza,
        giorni metodo sequenziale, giorni metodo sovrapposto, e risparmio.
        La colonna "RISPARMIO" è evidenziata in verde chiaro. L'ultima riga
        mostra i totali aggregati. Header blu, riga totali verde, celle dati
        alternate grigio/bianco per migliore leggibilità.
        """
        ax.axis('off')

        headers = ['SPECIE', 'LARVE', 'PESCI COMM.', 'TONNELLATE', 'SOPRAVV.%', 'GG SEQ.', 'GG SOV.', 'RISPARMIO']

        rows = []
        for i, det_sov in enumerate(risultati_sov['dettagli']):
            det_seq = risultati_seq['dettagli'][i]
            nome = det_sov['specie'].split('(')[0].strip()

            gg_seq = det_seq.get('giorni_totali', det_seq.get('fine_ingrasso_giorno', 0))
            gg_sov = det_sov['fine_ingrasso_giorno']
            risparmio = gg_seq - gg_sov

            row = [
                nome,
                f"{det_sov['larve_seminate']:,}",
                f"{det_sov['pesci_commerciali']:,}",
                f"{det_sov['tonnellate_prodotte']} t",
                f"{det_sov['tasso_sopravvivenza_totale']}%",
                str(gg_seq),
                str(gg_sov),
                f"{risparmio} gg"
            ]
            rows.append(row)

        # Riga totali
        totale_larve = sum(d['larve_seminate'] for d in risultati_sov['dettagli'])
        totale_pesci = sum(d['pesci_commerciali'] for d in risultati_sov['dettagli'])
        totale_tonn = sum(d['tonnellate_prodotte'] for d in risultati_sov['dettagli'])
        risparmio_tot = risultati_seq['tempo_totale'] - risultati_sov['tempo_totale']

        rows.append([
            'TOTALE',
            f"{totale_larve:,}",
            f"{totale_pesci:,}",
            f"{totale_tonn:.1f} t",
            f"{(totale_pesci/totale_larve*100):.1f}%",
            str(risultati_seq['tempo_totale']),
            str(risultati_sov['tempo_totale']),
            f"{risparmio_tot} gg"
        ])

        # Crea tabella
        table = ax.table(
            cellText=rows,
            colLabels=headers,
            cellLoc='center',
            loc='center',
            colWidths=[0.14, 0.12, 0.12, 0.11, 0.09, 0.09, 0.09, 0.11]
        )

        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 3)

        # Stile header
        for i in range(len(headers)):
            cell = table[(0, i)]
            cell.set_facecolor(self.colors['primary'])
            cell.set_text_props(weight='bold', color='white', fontsize=12)
            cell.set_edgecolor('white')
            cell.set_linewidth(2)

        # Stile riga totali
        for i in range(len(headers)):
            cell = table[(len(rows), i)]
            cell.set_facecolor(self.colors['success'])
            cell.set_text_props(weight='bold', color='white', fontsize=12)
            cell.set_edgecolor('white')
            cell.set_linewidth(2)

        # Stile celle dati
        for i in range(1, len(rows)):
            for j in range(len(headers)):
                cell = table[(i, j)]
                if i % 2 == 0:
                    cell.set_facecolor('#f3f4f6')
                else:
                    cell.set_facecolor('white')
                cell.set_edgecolor('#d1d5db')
                cell.set_linewidth(1)

                # Evidenzia colonna risparmio
                if j == 7:
                    cell.set_facecolor('#d1fae5')

        ax.set_title('TABELLA RIEPILOGO COMPARATIVO', fontsize=14, fontweight='bold', pad=20, y=0.98)