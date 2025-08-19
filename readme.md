# Photo Rules Checker - Python Script untuk Validasi Foto

**Author:** Alfandi R.  
**Email:** alfandisullivan@gmail.com

**Deskripsi:**  
Photo Rules Checker adalah script Python yang digunakan untuk **memeriksa aturan foto**, termasuk gender, background, pakaian formal, hijab, dan kerapian rambut. Mendukung berbagai format gambar seperti JPG, PNG, dan WEBP. Script ini memanfaatkan model deep learning untuk deteksi gender dan analisis citra untuk atribut lainnya.

---

## Fitur Utama

-   **Deteksi Gender Otomatis:** Menggunakan model `gender_net.caffemodel` dan `gender_deploy.prototxt` untuk memprediksi apakah wajah dalam foto adalah **laki-laki (male)** atau **perempuan (female)**.
-   **Deteksi Background Merah:** Memeriksa 50 pixel teratas untuk warna dominan merah.
-   **Deteksi Jas Hitam:** Memeriksa area dada/sisi kiri, mendeteksi jas formal.
-   **Deteksi Kemeja Putih:** Menghitung rasio pixel putih di area dada ≥ 23%.
-   **Deteksi Dasi Hitam:** Untuk laki-laki, mendeteksi dasi formal gelap.
-   **Deteksi Hijab Hitam:** Untuk perempuan berhijab, mendeteksi hijab gelap.
-   **Rambut Rapi:** Untuk perempuan non-hijab, memeriksa kerapian rambut menggunakan variansi laplacian.

---

## Cara Menggunakan Photo Rules Checker

1. Install dependencies:

```bash
pip install opencv-python pillow numpy
```

2. Pastikan file model gender tersedia di folder project:

```bash
gender_net.caffemodel

gender_deploy.prototxt
```

3. Siapkan folder foto input, misal:

```bash
assets
├── img1.jpg
├── img2.jpg
└── img3.jpg
```

4. Jalankan script dengan command `python cek_foto.py`

5. Output akan muncul di terminal.

```bash
{
    "gender": "male",
    "background": True,
    "jas_hitam": True,
    "kemeja_putih": True,
    "dasi_hitam": True,
    "hijab_hitam": False,
    "rambut_rapi": False
}
```
