# Panduan Lengkap Deployment Aplikasi Streamlit

## Klasifikasi Spasial Tutupan Lahan Provinsi Jawa Timur Berbasis Sentinel-2 & Random Forest

---

## 1. Pengantar Deployment

Dokumen ini berisi panduan komprehensif untuk menjalankan aplikasi web **Streamlit** baik pada komputer lokal (*local development*) maupun melakukan publikasi ke cloud publik melalui **Streamlit Community Cloud** (hosting gratis terintegrasi dengan GitHub).

Aplikasi ini menyajikan visualisasi spasial interaktif hasil klasifikasi tutupan lahan Jawa Timur (5 kelas: Pemukiman, Lahan Pertanian, Perairan, Hutan Biasa, dan Hutan Mangrove) menggunakan citra satelit **Sentinel-2 Level-2A** dan algoritma **Random Forest**.

---

## 2. Struktur Direktori Deployment

Seluruh berkas aplikasi web dan data pendukung telah diisolasi di dalam folder `streamlit/` (dengan salinan cadangan di `uts/deploy/`):

```
PSD/
├── streamlit/
│   ├── app.py                         <-- File kode utama aplikasi Streamlit
│   ├── requirements.txt               <-- Daftar dependensi pustaka Python
│   ├── PANDUAN_DEPLOY_STREAMLIT.md    <-- Dokumen panduan ini
│   └── data/                          <-- Direktori seluruh data pendukung
│       ├── metrik_evaluasi.json       <-- Metrik akurasi piksel, poligon & laporan klasifikasi
│       ├── confusion_matrix.csv       <-- Tabel data matriks konfusi
│       ├── confusion_matrix.png       <-- Gambar visualisasi matriks konfusi
│       ├── feature_importance.csv     <-- Tabel data kepentingan 10 fitur spektral
│       ├── feature_importance.png     <-- Gambar diagram kepentingan fitur spektral
│       ├── prediksi_pixel_test.csv    <-- 8.996 sampel piksel uji beserta fitur & status
│       ├── prediksi_poligon_test.csv  <-- 46 poligon uji dengan hasil voting mayoritas
│       ├── peta_gabungan_jatim.html   <-- Peta interaktif Leaflet poligon evaluasi
│       ├── peta_klasifikasi_tutupan_lahan_jatim.html <-- Peta interaktif raster Jawa Timur
│       └── random_forest_jatim_pixel.joblib          <-- Model Random Forest terlatih (~40 MB)
├── .gitignore                         <-- Konfigurasi pengabaian berkas besar (>100MB)
└── ...
```

---

## 3. Rincian Kebutuhan Data & Fungsinya

Setiap berkas di dalam subfolder `streamlit/data/` memiliki fungsi spesifik pada aplikasi web:

| Nama Berkas | Ukuran | Fungsi dalam Aplikasi Streamlit |
| :--- | :---: | :--- |
| **`metrik_evaluasi.json`** | ~2 KB | Menyediakan nilai akurasi piksel (90.00%), akurasi poligon (76.09%), jumlah sampel latih/uji, dan metrik presisi/recall per kelas untuk kartu KPI dan tabel evaluasi. |
| **`confusion_matrix.png`** & **`.csv`** | ~163 KB | Menampilkan visualisasi matriks kesalahan prediksi model antara 5 kelas tutupan lahan pada data uji. |
| **`feature_importance.png`** & **`.csv`** | ~60 KB | Menampilkan diagram peringkat kontribusi 10 fitur spektral (Ratio B8A/B11, MNDWI, NDVI, B02, B03, NDBI, B11, B8A, B04, B08). |
| **`prediksi_pixel_test.csv`** | ~1.9 MB | Digunakan pada menu **Eksplorasi Data Uji** untuk filter interaktif baris piksel berdasarkan status (BENAR / SALAH) dan kelas tutupan lahan. |
| **`prediksi_poligon_test.csv`** | ~2.3 KB | Menampilkan tabel 46 poligon uji hasil penentuan kelas melalui voting mayoritas piksel (35 Benar, 11 Salah). |
| **`peta_gabungan_jatim.html`** | ~733 KB | Peta interaktif Leaflet/Folium yang dirender via iframe untuk melihat sebaran poligon train vs test serta poligon salah klasifikasi. |
| **`peta_klasifikasi_tutupan_lahan_jatim.html`** | ~2.3 MB | Peta tematik raster tutupan lahan seluruh Jawa Timur hasil prediksi model Random Forest. |
| **`random_forest_jatim_pixel.joblib`** | ~40.6 MB | Berkas serialisasi model Random Forest (200 trees). Disimpan untuk keperluan reproduksibilitas dan inferensi model. |

---

## 4. Kebutuhan Pustaka (`requirements.txt`)

Berkas `streamlit/requirements.txt` berisi daftar pustaka minimal yang wajib dipasang:

```txt
streamlit>=1.30.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.4.0
joblib>=1.3.0
matplotlib>=3.7.0
altair>=5.0.0
```

- **Python Versi Rekomendasi:** Python `3.10`, `3.11`, atau `3.12`.
- Hindari versi Python yang terlalu lama (< 3.9) agar kompatibel dengan Scikit-learn versi terbaru.

---

## 5. Batasan Ukuran Berkas GitHub & `.gitignore`

> ⚠️ **PENTING: Batasan 100 MB GitHub**
> 
> GitHub menerapkan batas keras (*hard limit*) maksimal **100 MB** per berkas.
> - Citra satelit mentah `sentinel2_jatim.tif` berukuran **269.6 MB**, sehingga **WAJIB dikecualikan** menggunakan `.gitignore`.
> - Model `random_forest_jatim_pixel.joblib` berukuran **40.66 MB**, sehingga **AMAN** dan dapat diunggah langsung ke GitHub tanpa Git LFS.

Pastikan isi berkas `.gitignore` di repositori memuat baris berikut:
```gitignore
# Abaikan citra raster besar (>100MB)
*.tif
*.tiff
*.nc
data/tif/
uts/data/tif/
```

---

## 6. Langkah Menjalankan Aplikasi di Komputer Lokal

### Langkah 1: Buka Terminal / PowerShell
Masuk ke direktori proyek:
```powershell
cd "d:\SEMESTER 5\psd"
```

### Langkah 2: Buat & Aktifkan Virtual Environment (Disarankan)
```powershell
# Membuat virtual environment
python -m venv venv

# Mengaktifkan di Windows PowerShell
.\venv\Scripts\Activate.ps1
```

### Langkah 3: Pasang Dependensi
```powershell
pip install -r streamlit/requirements.txt
```

### Langkah 4: Jalankan Server Streamlit
```powershell
streamlit run streamlit/app.py
```
Aplikasi akan otomatis terbuka di browser pada alamat:
`http://localhost:8501`

---

## 7. Langkah Sinkronisasi & Upload ke GitHub

Sebelum melakukan hosting online di Streamlit Cloud, repositori GitHub harus diperbarui terlebih dahulu:

### 1. Periksa Status Berkas
```powershell
git status
```

### 2. Tambahkan Berkas ke Staging Area
```powershell
git add .gitignore streamlit/ uts/ pendahuluan.md business_understanding.md data_understanding.md _toc.yml
```

### 3. Buat Commit
```powershell
git commit -m "feat: setup aplikasi web streamlit, requirements, data, dan panduan deployment"
```

### 4. Push ke GitHub
```powershell
git push origin main
```

---

## 8. Langkah Hosting Publik di Streamlit Community Cloud

Hosting di Streamlit Community Cloud bersifat **gratis** dan langsung tersambung dengan repositori GitHub Anda:

### Langkah 1: Kunjungi Portal Streamlit Cloud
Buka [share.streamlit.io](https://share.streamlit.io/) pada browser dan masuk (*Sign In*) menggunakan akun GitHub Anda (`mukhlisin24`).

### Langkah 2: Buat Aplikasi Baru (*New App*)
1. Klik tombol **"Create app"** atau **"New app"** di pojok kanan atas.
2. Pilih opsi **"Yup, I have an app"** (jika diminta).

### Langkah 3: Isi Formulir Deployment
Konfigurasikan field berikut secara tepat:
- **Repository**: `mukhlisin24/PSD`
- **Branch**: `main`
- **Main file path**: `streamlit/app.py`
- **App URL (opsional)**: Tentukan nama subdomain kustom, misalnya `tutupan-lahan-jatim.streamlit.app`

### Langkah 4: Deploy
Klik tombol **"Deploy!"**.
- Streamlit Cloud akan secara otomatis mendeteksi berkas `streamlit/requirements.txt`.
- Proses instalasi pustaka memakan waktu sekitar 1–3 menit pada peluncuran pertama.
- Setelah selesai, aplikasi web Anda aktif dan dapat diakses publik oleh siapa saja melalui tautan URL yang diberikan.

---

## 9. Pemecahan Masalah (*Troubleshooting*)

| Gejala Masalah | Penyebab | Solusi |
| :--- | :--- | :--- |
| **Hanya menu pertama yang tampil** | Nama menu pada radio button tidak cocok persis dengan blok `elif menu == ...` (misal ada perbedaan spasi atau emoji). | Pastikan string pada `st.radio(...)` persis sama dengan string pada kondisi `if` dan `elif`. Pada versi saat ini, seluruh kondisi telah diselaraskan. |
| **Teks pada kotak tidak terlihat** | Warna teks mewarisi tema gelap (*Dark Mode*) sehingga kontras hilang pada latar putih. | Menggunakan CSS inline dengan atribut `color: #1e272e;` dan `background-color: #ffffff;` secara eksplisit agar selalu jelas baik di Light Mode maupun Dark Mode. |
| **`FileNotFoundError` saat deploy** | Posisi working directory berbeda saat dijalankan di server cloud vs lokal. | Gunakan fungsi pencari path dinamis `get_file_path()` yang telah terintegrasi di `app.py`. Fungsi ini otomatis memeriksa `./data/`, `../data/`, dan `streamlit/data/`. |
| **Git Push ditolak (*pre-receive hook declined*)** | Ada file yang ukurannya melebihi 100 MB yang tidak sengaja ter-stage (misal `sentinel2_jatim.tif`). | Jalankan `git rm --cached data/tif/*.tif` dan pastikan `.gitignore` telah menyertakan `*.tif`. |
