"""
GENERATORE DI REPORT GRAFICI - GRUPPO DEL PESCE
Classe per generare report visivi con grafici e tabelle in formato PNG
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
from typing import Dict, List
from datetime import datetime


class ReportGeneratorGruppoDelPesce:
    """
    Genera report grafici completi con:
    - Grafici a barre
    - Grafici a torta
    - Tabelle comparatives
    - Timeline produttive
    - KPI dashboard
    """

    def __init__(self, config):
        """
        Inizializza il generatore di report

        Args:
            config: Oggetto ConfigurazioneGruppoDelPesce
        """
        self.config = config
        self.colors = {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#48bb78',
            'warning': '#f6ad55',
            'danger': '#fc8181',
            'spigola': '#3182ce',
            'orata': '#dd6b20',
            'ombrina': '#38a169'
        }

        # Configura lo stile matplotlib
        plt.style.use('seaborn-v0_8-darkgrid')
        plt.rcParams['font.family'] = 'DejaVu Sans'  # Font che supporta emoji
        plt.rcParams['font.size'] = 9
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['xtick.labelsize'] = 9
        plt.rcParams['ytick.labelsize'] = 9
        plt.rcParams['legend.fontsize'] = 9

        # Disabilita warning per glifi mancanti
        import warnings
        warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

    def genera_report_completo(self,
                               risultati_seq: Dict,
                               risultati_sov: Dict,
                               lotti: List,
                               nome_file: str = None) -> str:
        """
        Genera un report completo con tutti i grafici e tabelle

        Args:
            risultati_seq: Risultati simulazione sequenziale
            risultati_sov: Risultati simulazione sovrapposta
            lotti: Lista dei lotti simulati
            nome_file: Nome del file di output (opzionale)

        Returns:
            str: Path del file PNG generato
        """
        if nome_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_file = f"report_gruppo_del_pesce_{timestamp}.png"

        # Crea figura con layout complesso
        fig = plt.figure(figsize=(20, 14))
        fig.suptitle('🐠 REPORT SIMULAZIONE PRODUZIONE - GRUPPO DEL PESCE',
                     fontsize=20, fontweight='bold', y=0.98)

        # Sottotitolo
        fig.text(0.5, 0.95,
                'Filiera integrata: dalla nascita alla taglia commerciale | Guidonia (RM)',
                ha='center', fontsize=12, style='italic', color='gray')

        # Crea griglia complessa
        gs = GridSpec(4, 3, figure=fig, hspace=0.4, wspace=0.3,
                     left=0.05, right=0.95, top=0.92, bottom=0.05)

        # 1. KPI Dashboard (riga 1)
        ax1 = fig.add_subplot(gs[0, :])
        self._crea_kpi_dashboard(ax1, lotti, risultati_sov)

        # 2. Confronto tempi (riga 2, colonna 1)
        ax2 = fig.add_subplot(gs[1, 0])
        self._crea_grafico_confronto_tempi(ax2, risultati_seq, risultati_sov)

        # 3. Distribuzione produzione (riga 2, colonna 2)
        ax3 = fig.add_subplot(gs[1, 1])
        self._crea_grafico_torta_produzione(ax3, risultati_sov)

        # 4. Analisi sopravvivenza (riga 2, colonna 3)
        ax4 = fig.add_subplot(gs[1, 2])
        self._crea_grafico_sopravvivenza(ax4, risultati_sov)

        # 5. Timeline produttiva (riga 3, colonne 1-2)
        ax5 = fig.add_subplot(gs[2, :2])
        self._crea_timeline_produttiva(ax5, risultati_sov)

        # 6. Risorse utilizzate (riga 3, colonna 3)
        ax6 = fig.add_subplot(gs[2, 2])
        self._crea_grafico_risorse(ax6, risultati_sov)

        # 7. Tabella comparativa (riga 4, colonne 1-2)
        ax7 = fig.add_subplot(gs[3, :2])
        self._crea_tabella_comparativa(ax7, risultati_seq, risultati_sov)

        # 8. Analisi produzione annuale (riga 4, colonna 3)
        ax8 = fig.add_subplot(gs[3, 2])
        self._crea_grafico_produzione_annuale(ax8, risultati_sov)

        # Salva figura
        plt.savefig(nome_file, dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()

        return nome_file

    def _crea_kpi_dashboard(self, ax, lotti, risultati):
        """Crea dashboard con KPI principali"""
        ax.axis('off')

        # Calcola KPI
        totale_larve = sum(l.numero_larve for l in lotti)
        totale_pesci = sum(d['pesci_commerciali'] for d in risultati['dettagli'])
        totale_tonnellate = sum(d['tonnellate_prodotte'] for d in risultati['dettagli'])
        tasso_sopravvivenza = (totale_pesci / totale_larve * 100)

        kpis = [
            ('🐟 LARVE SEMINATE', f'{totale_larve:,}', 'larve'),
            ('🎣 PESCI COMMERCIALI', f'{totale_pesci:,}', 'pesci'),
            ('⚖️ TONNELLATE', f'{totale_tonnellate:.2f} t', ''),
            ('📈 SOPRAVVIVENZA', f'{tasso_sopravvivenza:.1f}%', 'totale')
        ]

        # Disegna KPI cards
        card_width = 0.22
        card_height = 0.8
        start_x = 0.05

        for i, (label, value, subtitle) in enumerate(kpis):
            x = start_x + i * 0.24

            # Box colorato
            rect = mpatches.FancyBboxPatch(
                (x, 0.1), card_width, card_height,
                boxstyle="round,pad=0.02",
                facecolor=self.colors['primary'] if i % 2 == 0 else self.colors['secondary'],
                edgecolor='none', alpha=0.2, transform=ax.transAxes
            )
            ax.add_patch(rect)

            # Testo
            ax.text(x + card_width/2, 0.7, label,
                   ha='center', va='center', fontsize=10,
                   fontweight='bold', transform=ax.transAxes)

            ax.text(x + card_width/2, 0.45, value,
                   ha='center', va='center', fontsize=16,
                   fontweight='bold', color=self.colors['primary'],
                   transform=ax.transAxes)

            if subtitle:
                ax.text(x + card_width/2, 0.25, subtitle,
                       ha='center', va='center', fontsize=8,
                       style='italic', color='gray', transform=ax.transAxes)

    def _crea_grafico_confronto_tempi(self, ax, risultati_seq, risultati_sov):
        """Crea grafico a barre per confronto tempi"""
        metodi = ['Sequenziale', 'Sovrapposto']
        tempi = [risultati_seq['tempo_totale'], risultati_sov['tempo_totale']]
        colors = [self.colors['danger'], self.colors['success']]

        bars = ax.bar(metodi, tempi, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

        # Aggiungi valori sopra le barre
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)} gg',
                   ha='center', va='bottom', fontweight='bold', fontsize=11)

        # Calcola risparmio
        risparmio = risultati_seq['tempo_totale'] - risultati_sov['tempo_totale']
        percentuale = (risparmio / risultati_seq['tempo_totale'] * 100)

        ax.set_ylabel('Giorni', fontweight='bold')
        ax.set_title('⏱️ Confronto Tempi Produttivi', fontweight='bold', pad=15)
        ax.grid(axis='y', alpha=0.3)

        # Aggiungi testo risparmio
        ax.text(0.5, 0.95, f'Risparmio: {risparmio} giorni ({percentuale:.1f}%)',
               transform=ax.transAxes, ha='center', va='top',
               bbox=dict(boxstyle='round', facecolor=self.colors['success'], alpha=0.3),
               fontweight='bold')

    def _crea_grafico_torta_produzione(self, ax, risultati):
        """Crea grafico a torta per distribuzione produzione"""
        specie = [d['specie'] for d in risultati['dettagli']]
        tonnellate = [d['tonnellate_prodotte'] for d in risultati['dettagli']]

        colors_specie = [self.colors['spigola'], self.colors['orata'], self.colors['ombrina']]

        wedges, texts, autotexts = ax.pie(tonnellate, labels=specie, autopct='%1.1f%%',
                                          colors=colors_specie, startangle=90,
                                          explode=(0.05, 0.05, 0.05))

        # Migliora la leggibilità
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)

        for text in texts:
            text.set_fontsize(9)
            text.set_fontweight('bold')

        ax.set_title('🐟 Distribuzione Produzione per Specie', fontweight='bold', pad=15)

    def _crea_grafico_sopravvivenza(self, ax, risultati):
        """Crea grafico a barre per tassi di sopravvivenza"""
        specie = [d['specie'].split('/')[0] if '/' in d['specie'] else d['specie']
                 for d in risultati['dettagli']]
        tassi = [d['tasso_sopravvivenza_totale'] for d in risultati['dettagli']]

        colors_specie = [self.colors['spigola'], self.colors['orata'], self.colors['ombrina']]

        bars = ax.barh(specie, tassi, color=colors_specie, alpha=0.7, edgecolor='black', linewidth=1.5)

        # Aggiungi valori
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{tassi[i]}%',
                   ha='left', va='center', fontweight='bold', fontsize=10,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        ax.set_xlabel('Tasso di Sopravvivenza (%)', fontweight='bold')
        ax.set_title('📈 Tasso di Sopravvivenza Totale', fontweight='bold', pad=15)
        ax.set_xlim(0, 100)
        ax.grid(axis='x', alpha=0.3)

    def _crea_timeline_produttiva(self, ax, risultati):
        """Crea timeline Gantt della produzione sovrapposta"""
        dettagli = risultati['dettagli']

        y_pos = np.arange(len(dettagli))
        colors_specie = [self.colors['spigola'], self.colors['orata'], self.colors['ombrina']]

        for i, det in enumerate(dettagli):
            specie_nome = det['specie'].split('/')[0] if '/' in det['specie'] else det['specie']

            # Fase larvale
            ax.barh(i, det['giorni_larvali'], left=det['inizio_giorno'],
                   color=colors_specie[i], alpha=0.3, edgecolor='black', linewidth=1,
                   label='Larvale' if i == 0 else '')

            # Fase preingrasso
            ax.barh(i, det['giorni_preingrasso'], left=det['fine_larvale_giorno'],
                   color=colors_specie[i], alpha=0.6, edgecolor='black', linewidth=1,
                   label='Preingrasso' if i == 0 else '')

            # Fase ingrasso
            ax.barh(i, det['giorni_ingrasso'], left=det['fine_preingrasso_giorno'],
                   color=colors_specie[i], alpha=0.9, edgecolor='black', linewidth=1,
                   label='Ingrasso' if i == 0 else '')

            # Etichetta specie
            ax.text(det['inizio_giorno'] - 5, i, specie_nome,
                   ha='right', va='center', fontweight='bold', fontsize=9)

        ax.set_yticks(y_pos)
        ax.set_yticklabels([''] * len(dettagli))
        ax.set_xlabel('Giorni', fontweight='bold')
        ax.set_title('📅 Timeline Produttiva (Metodo Sovrapposto)', fontweight='bold', pad=15)
        ax.legend(loc='upper right', framealpha=0.9)
        ax.grid(axis='x', alpha=0.3)

    def _crea_grafico_risorse(self, ax, risultati):
        """Crea grafico delle risorse utilizzate"""
        categorie = ['Vasche\nLarvali', 'Vasche\nPreingrasso', 'Gabbie\nIngrasso']

        # Somma le risorse per tutte le specie
        vasche_larvali = [d['vasche_larvali'] for d in risultati['dettagli']]
        vasche_preingrasso = [d['vasche_preingrasso'] for d in risultati['dettagli']]
        gabbie_ingrasso = [d['gabbie_ingrasso'] for d in risultati['dettagli']]

        x = np.arange(len(categorie))
        width = 0.25

        colors_specie = [self.colors['spigola'], self.colors['orata'], self.colors['ombrina']]
        specie_nomi = [d['specie'].split('/')[0] if '/' in d['specie'] else d['specie']
                      for d in risultati['dettagli']]

        # Crea barre affiancate
        for i in range(len(risultati['dettagli'])):
            valori = [vasche_larvali[i], vasche_preingrasso[i], gabbie_ingrasso[i]]
            ax.bar(x + (i - 1) * width, valori, width, label=specie_nomi[i],
                  color=colors_specie[i], alpha=0.8, edgecolor='black', linewidth=1)

        ax.set_ylabel('Numero Unità', fontweight='bold')
        ax.set_title('🏭 Risorse Utilizzate', fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(categorie, fontsize=8)
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(axis='y', alpha=0.3)

    def _crea_tabella_comparativa(self, ax, risultati_seq, risultati_sov):
        """Crea tabella comparativa dettagliata"""
        ax.axis('off')

        # Prepara dati
        headers = ['Specie', 'Larve', 'Avannotti 2g', 'Pesci Comm.',
                  'Tonnellate', 'Sopravv.%', 'Giorni Seq.', 'Giorni Sov.']

        rows = []
        for i, det_sov in enumerate(risultati_sov['dettagli']):
            det_seq = risultati_seq['dettagli'][i]
            specie_nome = det_sov['specie'].split('(')[0].strip()

            row = [
                specie_nome,
                f"{det_sov['larve_seminate']:,}",
                f"{det_sov['avannotti_2g']:,}",
                f"{det_sov['pesci_commerciali']:,}",
                f"{det_sov['tonnellate_prodotte']}",
                f"{det_sov['tasso_sopravvivenza_totale']}%",
                f"{det_seq['giorni_totali'] if 'giorni_totali' in det_seq else det_seq['fine_ingrasso_giorno']}",
                f"{det_sov['fine_ingrasso_giorno']}"
            ]
            rows.append(row)

        # Aggiungi riga totali
        totale_larve = sum(d['larve_seminate'] for d in risultati_sov['dettagli'])
        totale_pesci = sum(d['pesci_commerciali'] for d in risultati_sov['dettagli'])
        totale_tonn = sum(d['tonnellate_prodotte'] for d in risultati_sov['dettagli'])

        rows.append([
            'TOTALE',
            f"{totale_larve:,}",
            '-',
            f"{totale_pesci:,}",
            f"{totale_tonn:.2f}",
            f"{(totale_pesci/totale_larve*100):.1f}%",
            f"{risultati_seq['tempo_totale']}",
            f"{risultati_sov['tempo_totale']}"
        ])

        # Crea tabella
        table = ax.table(cellText=rows, colLabels=headers,
                        cellLoc='center', loc='center',
                        colWidths=[0.15, 0.12, 0.12, 0.12, 0.10, 0.10, 0.10, 0.10])

        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 2.5)

        # Stile header
        for i in range(len(headers)):
            cell = table[(0, i)]
            cell.set_facecolor(self.colors['primary'])
            cell.set_text_props(weight='bold', color='white')

        # Stile riga totali
        for i in range(len(headers)):
            cell = table[(len(rows), i)]
            cell.set_facecolor(self.colors['success'])
            cell.set_text_props(weight='bold', color='white')

        # Alterna colori righe
        for i in range(1, len(rows)):
            for j in range(len(headers)):
                cell = table[(i, j)]
                if i % 2 == 0:
                    cell.set_facecolor('#f0f0f0')

        ax.set_title('📊 Tabella Comparativa Dettagliata', fontweight='bold',
                    fontsize=12, pad=20)

    def _crea_grafico_produzione_annuale(self, ax, risultati):
        """Crea grafico produzione annuale vs target"""
        tot_tonnellate = sum(d['tonnellate_prodotte'] for d in risultati['dettagli'])
        cicli_anno = 365 / risultati['tempo_totale']
        produzione_annua = tot_tonnellate * cicli_anno
        target = self.config.capacita_produttiva_annua

        categorie = ['Produzione\nStimata', 'Target\nAziendale']
        valori = [produzione_annua, target]
        colors = [self.colors['success'] if produzione_annua >= target else self.colors['warning'],
                 self.colors['primary']]

        bars = ax.bar(categorie, valori, color=colors, alpha=0.7, edgecolor='black', linewidth=2)

        # Aggiungi valori
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)} t',
                   ha='center', va='bottom', fontweight='bold', fontsize=11)

        ax.set_ylabel('Tonnellate/Anno', fontweight='bold')
        ax.set_title('📈 Produzione Annuale Stimata', fontweight='bold', pad=15)
        ax.grid(axis='y', alpha=0.3)

        # Percentuale raggiungimento
        percentuale = (produzione_annua / target * 100)
        ax.text(0.5, 0.95, f'Raggiungimento: {percentuale:.1f}%',
               transform=ax.transAxes, ha='center', va='top',
               bbox=dict(boxstyle='round', facecolor=colors[0], alpha=0.3),
               fontweight='bold')

        # Info cicli
        ax.text(0.5, 0.85, f'Cicli/anno: {cicli_anno:.1f}',
               transform=ax.transAxes, ha='center', va='top',
               fontsize=9, style='italic')


# ============================================================================
# ESEMPIO DI UTILIZZO
# ============================================================================

def esempio_utilizzo():
    """
    Esempio di come utilizzare la classe ReportGeneratorGruppoDelPesce
    """
    from config import settings
    from data_model.specie_ittica_model import SpecieIttica
    from data_model.lotto_produzione_model import LottoProduzione

    # Importa le funzioni di simulazione esistenti
    # from tuo_modulo import (
    #     ConfigurazioneGruppoDelPesce,
    #     genera_lotti_casuali,
    #     sequenza_produzione_completa_sequenziale,
    #     sequenza_produzione_integrata_sovrapposta
    # )

    # 1. Configura l'impianto (come nel codice esistente)
    # config = ConfigurazioneGruppoDelPesce()

    # 2. Definisci specie e genera lotti (come nel codice esistente)
    # specie_ittiche = [...]
    # lotti = genera_lotti_casuali(specie_ittiche)

    # 3. Esegui simulazioni (come nel codice esistente)
    # risultati_seq = sequenza_produzione_completa_sequenziale(lotti, config)
    # risultati_sov = sequenza_produzione_integrata_sovrapposta(lotti, config)

    # 4. NUOVO: Genera report grafico invece di stampare
    # report_generator = ReportGeneratorGruppoDelPesce(config)
    # file_output = report_generator.genera_report_completo(
    #     risultati_seq,
    #     risultati_sov,
    #     lotti,
    #     nome_file="report_produzione.png"
    # )

    # print(f"✅ Report generato: {file_output}")

    pass


if __name__ == "__main__":
    print("Classe ReportGeneratorGruppoDelPesce pronta all'uso!")
    print("\nPer utilizzarla, sostituisci la chiamata a stampa_risultati() con:")
    print("report_generator = ReportGeneratorGruppoDelPesce(config)")
    print("report_generator.genera_report_completo(risultati_seq, risultati_sov, lotti)")