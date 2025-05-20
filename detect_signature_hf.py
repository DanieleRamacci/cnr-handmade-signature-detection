import os
from huggingface_hub import login, hf_hub_download
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# === CONFIGURAZIONE ===
HUGGINGFACE_TOKEN = "ß"  # <-- Incolla il  token Huggig Face qui
IMAGES_DIR = "./docs-firmati/"       # Cartella con immagini PNG da analizzare
OUTPUT_DIR = "output_inferenza"       # Dove salvare immagini annotate e file .txt
SAVE_LABELS = True                    # True: salva anche le annotazioni in formato YOLO

# === LOGIN HUGGING FACE ===
login(HUGGINGFACE_TOKEN)

# === CREA CARTELLE SE MANCANO ===
os.makedirs(OUTPUT_DIR, exist_ok=True)


# === SCARICA MODELLO YOLOv8s PRE-ADDESTRATO PER FIRME ===
model_path = hf_hub_download(
    repo_id="tech4humans/yolov8s-signature-detector",
    filename="yolov8s.pt"
)

# === CARICA MODELLO ===
model = YOLO(model_path)

# === OTTIENI IMMAGINI DA CARTELLA ===
image_paths = [os.path.join(IMAGES_DIR, f) for f in os.listdir(IMAGES_DIR) if f.lower().endswith(".png")]

if not image_paths:
    print(f"❌ Nessuna immagine .png trovata nella cartella '{IMAGES_DIR}'.")
    exit()

# === PROCESSA OGNI IMMAGINE ===
for img_path in image_paths:
    print(f"🔍 Analizzo {os.path.basename(img_path)} ...")
    results = model.predict(source=img_path, save=False)[0]
    img = cv2.imread(img_path)

    h, w = img.shape[:2]
    label_lines = []

    for box in results.boxes:
        x1, y1, x2, y2 = map(float, box.xyxy[0])
        conf = float(box.conf[0])

        # Disegna il box
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(img, f"firma {conf:.2f}", (int(x1), int(y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Prepara riga in formato YOLO
        if SAVE_LABELS:
            cx = (x1 + x2) / 2 / w
            cy = (y1 + y2) / 2 / h
            bw = (x2 - x1) / w
            bh = (y2 - y1) / h
            label_lines.append(f"0 {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")

    # Salva immagine annotata
    output_img_path = os.path.join(OUTPUT_DIR, f"detected_{os.path.basename(img_path)}")
    cv2.imwrite(output_img_path, img)

    # Salva file di annotazione YOLO
    if SAVE_LABELS and label_lines:
        label_txt_path = os.path.join(OUTPUT_DIR, os.path.splitext(os.path.basename(img_path))[0] + ".txt")
        with open(label_txt_path, "w") as f:
            f.write("\n".join(label_lines))

    # Mostra immagine
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(f"Rilevata: {os.path.basename(img_path)}")
    plt.axis("off")
    plt.show()

print(f"\n✅ Firme analizzate! Risultati salvati in: {OUTPUT_DIR}")
