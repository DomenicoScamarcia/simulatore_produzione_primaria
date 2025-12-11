# Simulatore Produzione Primaria - Gruppo Del Pesce

## 📋 Descrizione del Progetto

Questo progetto implementa un **simulatore avanzato per il processo produttivo integrato** di un'avannotteria nel settore dell'acquacoltura, specificamente modellato sulla realtà operativa del **Gruppo Del Pesce** (Guidonia, RM).

Il simulatore analizza e confronta due diverse strategie produttive per l'allevamento di tre specie ittiche del Mediterraneo:
- **Spigola/Branzino** (*Dicentrarchus labrax*)
- **Orata** (*Sparus aurata*)
- **Ombrina** (*Argyrosomus regius*)

### 🎯 Scopo del Progetto

Il sistema simula l'intero **ciclo di vita produttivo dalla nascita alla taglia commerciale**, attraversando tre fasi principali:

1. **Fase Larvale** (35-45 giorni) - Avannotteria con vasche specializzate
2. **Fase Preingrasso** (65-80 giorni) - Crescita fino a 2 grammi
3. **Fase Ingrasso** (420-480 giorni) - Crescita fino a taglia commerciale (330-900g)

Il simulatore calcola automaticamente:
- ✅ Risorse necessarie (vasche larvali, vasche preingrasso, gabbie in mare)
- ✅ Tempi di produzione per ogni fase e specie
- ✅ Tassi di sopravvivenza e rese produttive
- ✅ Tonnellate di pesce prodotto
- ✅ Ottimizzazione dell'uso delle infrastrutture

### 🔬 Metodi di Produzione Confrontati

#### Metodo Sequenziale
Completa l'intero ciclo produttivo di una specie prima di iniziare la successiva. Approccio tradizionale che garantisce semplicità gestionale ma tempi totali più lunghi.

#### Metodo Sovrapposto (Ottimale)
Gestione simultanea di più lotti in fasi diverse, permettendo a un nuovo lotto di iniziare quando il precedente libera le vasche larvali. Ottimizza l'uso delle risorse e riduce significativamente i tempi totali di produzione (risparmio tipico del 59-60%).

### 📊 Output del Sistema

Il simulatore genera:
- **Report grafico PNG** con 7 visualizzazioni:
  - Dashboard KPI globali
  - Confronto diretto tra metodi produttivi
  - Timeline Gantt delle fasi sovrapposte
  - Distribuzione produzione per specie
  - Analisi risorse utilizzate
  - Tabella riepilogativa comparativa
  - Dettagli per metodo e specie

- **Output console** con dati dettagliati su:
  - Configurazione impianto
  - Lotti generati
  - Risultati simulazione
  - Analisi produzione annuale
  - Raggiungimento target aziendale (4.500 t/anno)

---

## 🚀 Installazione e Configurazione

### Prerequisiti

- **Python 3.8+** installato sul sistema
- **pip** (package manager Python)
- **git** (opzionale, per clonare il repository)

### 1. Clonazione del Repository

```bash
git clone https://github.com/tuo-username/simulatore_produzione_primaria.git
cd simulatore_produzione_primaria
```

*Oppure scarica il progetto come archivio ZIP ed estrailo.*

### 2. Creazione Ambiente Virtuale (Raccomandato)

È fortemente consigliato utilizzare un ambiente virtuale per isolare le dipendenze del progetto:

**Su Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Su Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Installazione Dipendenze

Installa tutte le librerie richieste dal file `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 💻 Esecuzione del Simulatore

### Comando Base

Per eseguire la simulazione completa:

```bash
python main.py
```

### Output Atteso

1. **Console:** Visualizzazione in tempo reale di:
   - Configurazione dell'impianto
   - Generazione lotti casuali
   - Risultati delle due simulazioni
   - Confronto dettagliato tra metodi
   - Analisi produzione annuale

2. **File PNG:** Report grafico completo salvato nella cartella `report/`:
   ```
   report/report_produzione.png
   ```
   Il file contiene tutte le visualizzazioni grafiche per l'analisi comparativa.

---

## 📁 Struttura del Progetto

```
simulatore-produzione_primaria/
│
├── app/
│   ├── report_generator.py         # Classe per generazione report PNG
│   └── main.py                     # Script principale di esecuzione
│
├── data_model/
│   ├── lotto_produzione_model.py   # Modello dati lotto
│   └── specie_ittica_model.py      # Modello dati specie
│
├── utils/
│   ├── calcolo_vasche.py           # Funzioni calcolo risorse
│   ├── configurazione.py           # Configurazione impianto
│   └── generazione_lotti.py        # Generazione lotti casuali
│
├── report/
│   └── report_produzione.png        # Report grafico generato
│
├── requirements.txt                 # Dipendenze del progetto
├── config.py                        # File di configurazione
└── README.md                        # Questo file
```

---

## ⚙️ Configurazione Parametri

I parametri dell'impianto possono essere configurati nel file `config.py`:

```python
# Vasche Larvali
VASCHE_LARVALI_PICCOLE = 30
VASCHE_LARVALI_MEDIE = 25
VASCHE_LARVALI_GRANDI = 10

# Impianti Produttivi
NUMERO_IMPIANTI = 6
GABBIE_PER_IMPIANTO = 20
VOLUME_GABBIA = 1000  # mc

# Parametri Produttivi
TASSO_SOPRAVVIVENZA_LARVALE = 0.70
TASSO_SOPRAVVIVENZA_PREINGRASSO = 0.90
TASSO_SOPRAVVIVENZA_INGRASSO = 0.95
EFFICIENZA_OPERATIVA = 0.85

# Target Aziendale
CAPACITA_PRODUTTIVA_ANNUA = 4500  # tonnellate/anno
```

---

## 📈 Casi d'Uso

### 1. Pianificazione Produttiva
Utilizzare il simulatore per pianificare la produzione annuale e verificare il raggiungimento dei target aziendali.

### 2. Ottimizzazione Risorse
Confrontare i due metodi per identificare strategie di ottimizzazione dell'uso di vasche e gabbie.

### 3. Analisi di Scenario
Modificare parametri (tassi di sopravvivenza, densità, tempi) per analizzare diversi scenari produttivi.

### 4. Supporto Decisionale
Fornire dati quantitativi per decisioni strategiche su investimenti in infrastrutture o modifiche ai processi.

### 5. Formazione e Didattica
Strumento educativo per comprendere le dinamiche dell'acquacoltura intensiva e l'importanza dell'ottimizzazione produttiva.

---

## 📄 Licenza

Questo progetto è stato sviluppato per scopi didattici e di ricerca nell'ambito del corso di Informatica per le Aziende Digitali.

---

## 👥 Autore

**Domenico Scamarcia**  
Corso di Laurea in Informatica per le Aziende Digitali (L-31)  
Project Work: Simulazione Processo Produttivo nel Settore Primario

---

**Versione:** 1.0.0  
**Ultimo aggiornamento:** Dicembre 2024
