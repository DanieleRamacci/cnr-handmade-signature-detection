import os
import fitz  # PyMuPDF
import cv2
import numpy as np
from huggingface_hub import login, hf_hub_download
from ultralytics import YOLO

# === CONFIGURAZIONE ===
HUGGINGFACE_TOKEN = "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"
PDF_FOLDER = "./docs-firmati/pdf/"
OUTPUT_FOLDER = "output_risultati"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)




# === Login a Hugging Face ===
login(HUGGINGFACE_TOKEN)

# === Scarica modello YOLOv8 da Hugging Face ===
model_path = hf_hub_download(
    repo_id="tech4humans/yolov8s-signature-detector",
    filename="yolov8s.pt"
)
model = YOLO(model_path)

# === Converti ogni PDF in immagini OpenCV ===
def pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(dpi=200)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n).copy()
        if pix.n == 4:  # con alpha
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        images.append((i, img))
    return images

# === Esegui inferenza e annota firme ===
def annota_firme(img):
    h, w = img.shape[:2]
    results = model.predict(source=img, save=False)[0]
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(img, f"firma {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return img, len(results.boxes)

# === Crea PDF dalle immagini annotate ===
def crea_pdf_da_immagini(annotated_images, out_pdf_path):
    doc = fitz.open()
    for img in annotated_images:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_bytes = cv2.imencode(".png", img_rgb)[1].tobytes()
        img_doc = fitz.open("png", img_bytes)
        rect = img_doc[0].rect
        page = doc.new_page(width=rect.width, height=rect.height)
        page.insert_image(rect, stream=img_bytes)
    doc.save(out_pdf_path)
    doc.close()

# === Loop sui PDF nella cartella ===
for pdf_file in os.listdir(PDF_FOLDER):
    if not pdf_file.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(PDF_FOLDER, pdf_file)
    print(f"🔍 Analizzo: {pdf_file}")
    images = pdf_to_images(pdf_path)

    annotated = []
    firma_trovata = False

    for page_num, img in images:
        img_annotata, count = annota_firme(img)
        if count > 0:
            firma_trovata = True
        annotated.append(img_annotata)

    if firma_trovata:
        out_pdf = os.path.join(OUTPUT_FOLDER, f"annotato_{pdf_file}")
        crea_pdf_da_immagini(annotated, out_pdf)
        print(f"✅ Firme trovate. PDF salvato in: {out_pdf}")
    else:
        print(f"❌ Nessuna firma rilevata in: {pdf_file}")