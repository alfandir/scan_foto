## Photo Rules Checker

**Author:** Alfandi R.

Script Python ini digunakan untuk **memeriksa aturan foto** seperti gender, background, pakaian, hijab, dan kerapian rambut.

Foto diinput dalam berbagai format (JPG, PNG, WEBP), lalu script akan menganalisis gambar dan menghasilkan dictionary hasil pemeriksaan.

---

## Fitur

1. **Deteksi gender**  
   Menggunakan model `gender_net.caffemodel` dan `gender_deploy.prototxt` untuk memprediksi apakah wajah dalam foto adalah **laki-laki (male)** atau **perempuan (female)**.

2. **Deteksi background merah**  
   Memeriksa 50 pixel teratas gambar, jika dominan merah → `background=True`.

3. **Deteksi jas hitam**  
   Memeriksa area sekitar dada/sisi kiri → jika rata-rata gelap → `jas_hitam=True`.

4. **Deteksi kemeja putih**  
   Memeriksa area dada → rasio pixel putih > 23% → `kemeja_putih=True`.

5. **Deteksi dasi hitam**  
   Jika gender = male, memeriksa area dasi → rata-rata gelap & standar deviasi kecil → `dasi_hitam=True`.

6. **Deteksi hijab hitam**  
   Jika gender = female & hijab=True → memeriksa area kepala/atas dada → rata-rata gelap → `hijab_hitam=True`.

7. **Rambut rapi (perempuan non-hijab)**  
   Jika gender = female & hijab=False → memeriksa variansi laplacian di area kepala → nilai rendah → `rambut_rapi=True`.

---

## Cara Pakai

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
