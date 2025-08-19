from PIL import Image
import cv2
import numpy as np

# ====================
# Konfigurasi model
# ====================
GENDER_MODEL = "gender_net.caffemodel"
GENDER_PROTO = "gender_deploy.prototxt"
GENDER_LIST = ["Male", "Female"]

# Load sekali saja
gender_net = cv2.dnn.readNetFromCaffe(GENDER_PROTO, GENDER_MODEL)

# Haarcascade untuk deteksi wajah
FACE_PROTO = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


# ====================
# Util
# ====================
def load_image(image_path):
    """Baca semua format gambar termasuk WEBP"""
    try:
        img = Image.open(image_path).convert("RGB")
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img
    except Exception as e:
        raise ValueError(f"Gagal membaca gambar {image_path}: {e}")

import cv2
import numpy as np

def detect_long_hair(img_resized):
    h, w, _ = img_resized.shape

    # Area di atas bahu hingga kepala (menghindari kerah & leher)
    top = int(h*0.1)
    bottom = int(h*0.8)
    left = int(w*0.1)
    right = int(w*0.9)
    hair_area = img_resized[top:bottom, left:right]

    # Ubah ke HSV untuk mendeteksi rambut lebih stabil
    hsv = cv2.cvtColor(hair_area, cv2.COLOR_BGR2HSV)
    lower_hair = np.array([0, 0, 0])        # gelap
    upper_hair = np.array([180, 255, 80])   # threshold gelap (rambut)
    mask = cv2.inRange(hsv, lower_hair, upper_hair)

    # Morphology untuk hapus noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Hitung kontur besar di area rambut
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    long_hair_detected = False
    for cnt in contours:
        x, y, w_cnt, h_cnt = cv2.boundingRect(cnt)
        area_cnt = cv2.contourArea(cnt)
        # Filter: cukup tinggi & area besar
        if area_cnt > 1500 and h_cnt > (bottom-top)*0.4:
            long_hair_detected = True
            break

    return long_hair_detected




def detect_gender(face_img):
    """Deteksi gender dari wajah"""
    blob = cv2.dnn.blobFromImage(
        face_img,
        1.0,
        (227, 227),
        (78.4263377603, 87.7689143744, 114.895847746),
        swapRB=False
    )
    gender_net.setInput(blob)
    preds = gender_net.forward()
    print(">>> Gender raw preds:", preds)  # Debug
    gender = GENDER_LIST[preds[0].argmax()]
    return gender.lower()  # "male" atau "female"


# ====================
# Main Check (Update)
# ====================
def check_ppg_photo_rules(image_path, hijab=False):
    result = {
        "gender": None,
        "background": False,
        "jas_hitam": False,
        "kemeja_putih": False,
        "dasi_hitam": False,
        "hijab_hitam": False,
        "rambut_rapi": False
    }

    # Load gambar
    img = load_image(image_path)
    img_resized = cv2.resize(img, (256, 256))

    # -----------------
    # 1. Deteksi wajah + gender
    # -----------------
    face_cascade = cv2.CascadeClassifier(FACE_PROTO)
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        margin = 20
        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(img_resized.shape[1], x + w + margin)
        y2 = min(img_resized.shape[0], y + h + margin)
        face_img = img_resized[y1:y2, x1:x2]

        try:
            # Pakai prediksi gender model langsung
            gender = detect_gender(face_img)
            result["gender"] = gender
        except Exception:
            result["gender"] = "unknown"
    else:
        result["gender"] = "unknown"

    # -----------------
    # Override gender kalau pakai hijab
    # -----------------
    if hijab:
        print("⚠️ Hijab detected → set gender=female")
        result["gender"] = "female"

    # -----------------
    # 2. Background merah
    # -----------------
    top_area = img_resized[0:50, :, :]
    avg_color = np.mean(top_area.reshape(-1, 3), axis=0)
    if avg_color[2] > 100 and avg_color[2] > avg_color[1] and avg_color[2] > avg_color[0]:
        result["background"] = True

    # -----------------
    # 3. Jas hitam
    # -----------------
    side_area = img_resized[100:200, 30:80, :]
    if np.mean(side_area) < 100:
        result["jas_hitam"] = True

    # -----------------
    # 4. Kemeja putih
    # -----------------
    chest_area = img_resized[150:230, 80:180, :]
    gray_chest = cv2.cvtColor(chest_area, cv2.COLOR_BGR2GRAY)
    white_pixels = np.sum(gray_chest > 180)
    total_pixels = gray_chest.size
    white_ratio = white_pixels / total_pixels
    if white_ratio > 0.23:
        result["kemeja_putih"] = True

    # -----------------
    # 5. Dasi hitam (laki-laki)
    # -----------------
    if result["gender"] == "male":
        tie_area = img_resized[180:240, 120:140, :]
        if np.mean(tie_area) < 100 and np.std(tie_area) < 30:
            result["dasi_hitam"] = True

    # -----------------
    # 6. Hijab hitam (perempuan hijab)
    # -----------------
    if result["gender"] == "female" and hijab and len(faces) > 0:
        x, y, w, h = faces[0]
        hijab_area = img_resized[y:y+h+40, x-30:x+w+30]
        if hijab_area.size > 0:
            avg_intensity = np.mean(cv2.cvtColor(hijab_area, cv2.COLOR_BGR2GRAY))
            if avg_intensity < 100:
                result["hijab_hitam"] = True

    # -----------------
    # 7. Rambut rapi (perempuan non-hijab)
    # -----------------
    if result["gender"] == "female" and not hijab:
        head_area = img_resized[40:100, 80:180, :]
        gray_head = cv2.cvtColor(head_area, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray_head, cv2.CV_64F).var()
        if laplacian_var < 3800:
            result["rambut_rapi"] = True

    return result



# ====================
# Contoh penggunaan
# ====================
if __name__ == "__main__":
    hasil = check_ppg_photo_rules("assets/foto2.jpg", hijab=False)
    print(hasil)
