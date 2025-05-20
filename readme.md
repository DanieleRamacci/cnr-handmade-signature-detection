# Report sullo stato attuale e obiettivi futuri

## Stato attuale del software

Il progetto attuale implementa un sistema per il rilevamento automatico di firme all'interno di documenti PDF utilizzando un modello YOLOv8 già addestrato e disponibile su Hugging Face. Il sistema converte i PDF in immagini, esegue l'inferenza per pagina e salva il risultato annotato in un nuovo PDF.

### Funzionalità attuali:
- Rilevamento firme nei documenti PDF.
- Conversione dei PDF in immagini e ricostruzione con annotazioni.
- Uso del modello `tech4humans/yolov8s-signature-detector`.

### Limiti riscontrati:
- Il sistema riconosce **una sola firma per pagina** anche se ve ne sono più di una.
- La qualità del rilevamento dipende fortemente dalla posizione, nitidezza e stile della firma.
- Il modello attuale è stato addestrato probabilmente con immagini contenenti una sola firma per documento.
- Il software non è ancora in grado di rilevare altri elementi sensibili come timbri, carte d’identità, codici fiscali, ecc.

---

## Obiettivo generale

L’obiettivo è evolvere il progetto in un **tool generalizzato per il rilevamento di dati personali** e **informazioni sensibili** all'interno di documenti digitalizzati (PDF e immagini), con la possibilità di:

- Evidenziare i dati rilevati.
- Generare un punteggio di sensibilità per documento.
- Offrire strumenti automatici per l’oscuramento (obfuscation) con successiva validazione manuale.

---

## Timeline e fasi di sviluppo

### **Fase 1: Miglioramento del rilevamento firme**
- Espansione del dataset attuale con:
  - Documenti simili a quelli del CNR.
  - Firme reali prese da un database interno.
- Generazione automatica di documenti PDF fake con:
  - Diverse firme, posizioni, angolazioni, trasparenze e sfocature.
  - Annotazioni automatiche associate alle immagini per training supervisionato.
- Riaddestramento o fine-tuning del modello YOLOv8 con il nuovo dataset.
- Validazione su documenti reali a più firme.

### **Fase 2: Estensione a nuovi tipi di dati sensibili**
- Definizione di nuove classi nel modello:
  - `id_card`, `fiscal_code`, `stamp`, `iban`, `medical_term`, `phone_number`, ecc.
- Annotazione e generazione di un dataset realistico o simulato per ciascun tipo.
- Implementazione di una pipeline multi-classe per il rilevamento simultaneo di più entità.
- Utilizzo di database ufficiali per migliorare la classificazione (es. codici fiscali noti, pattern delle patologie, codici sanitari, ecc.).

### **Fase 3: Integrazione con motore OCR**
- Implementazione di una seconda pipeline basata su OCR (es. Tesseract o EasyOCR).
- Analisi testuale dei documenti acquisiti (scansioni, immagini).
- Riconoscimento di pattern sensibili tramite:
  - Espressioni regolari.
  - Liste predefinite (e.g., codici ICD per malattie).
- Collegamento tra dati testuali e coordinate visive nel documento per l’annotazione e l’oscuramento.

### **Fase 4: Punteggio di rischio e revisione**
- Sviluppo di un sistema di scoring per ogni documento:
  - Numero e tipo di dati sensibili rilevati.
  - Rilevamenti ad alta confidenza.
- Interfaccia per la revisione e validazione manuale.
- Oscuramento automatico e auditabile dei dati.

---

## Obiettivo finale

Costruire un tool per l’analisi automatizzata dei documenti digitalizzati, in grado di:

- Individuare firme e dati sensibili.
- Generare report dettagliati.
- Facilitare la revisione umana e l’oscuramento dei dati.
- Essere integrabile in pipeline di data privacy, digital forensics e gestione documentale.

Il sistema sarà adattabile a diversi contesti: legale, sanitario, accademico, amministrativo.

---





# 📄 Handmade Signature Detection

> Rilevamento automatico di firme all'interno di documenti PDF tramite modello YOLOv8.

---
libreria usata : https://huggingface.co/tech4humans/yolov8s-signature-detector

## 📦 Requisiti

Il progetto richiede **Python 3.8+** e le seguenti dipendenze:

- [`pymupdf`](https://pymupdf.readthedocs.io/) (`fitz`)
- `opencv-python` *(oppure `opencv-python-headless` se si usa in ambiente server o su Mac M1/M2)*
- `numpy`
- `huggingface_hub`
- `ultralytics` *(per YOLOv8)*

---

## ⚙️ Installazione

### 1. Clona il repository

```bash
git clone https://github.com/DanieleRamacci/cnr-handmade-signature-detection.git
cd cnr-handmade-signature-detection


2. Crea un ambiente virtuale (consigliato)
bash
Copia codice
python3 -m venv venv
source venv/bin/activate
3. Installa le dipendenze
bash
Copia codice
pip install -r requirements.txt
Se non hai il file requirements.txt, puoi installare manualmente con:

bash
Copia codice
pip install pymupdf opencv-python numpy huggingface_hub ultralytics
Su Mac M1/M2:

bash
Copia codice
pip install pymupdf opencv-python-headless numpy huggingface_hub ultralytics
🚀 Esecuzione del programma
Assicurati di avere un token Hugging Face valido salvato o gestito via script.

Poi esegui:

bash
Copia codice
python script_firma_pdf.py
Questo script:

Estrae le pagine del PDF

Applica YOLOv8 per rilevare le firme

Salva i risultati in una cartella di output

📝 Note e comportamento attuale
Il programma riconosce una sola firma per ogni pagina.

Se ci sono più firme nella stessa pagina, solo la prima viene rilevata (comportamento attuale da migliorare).

Il modello potrebbe non riconoscere tutte le firme, specialmente se:

sono poco leggibili,

sono sovrapposte ad altri elementi,

hanno uno stile atipico rispetto al training set.

📌 TODO / miglioramenti futuri
 Rilevare tutte le firme per ogni pagina

 Migliorare la precisione del modello

 Aggiungere un'interfaccia di verifica visiva dei risultati

 Inserire logging e opzioni da riga di comando (argparse)

