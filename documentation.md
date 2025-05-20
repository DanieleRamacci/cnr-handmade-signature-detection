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

