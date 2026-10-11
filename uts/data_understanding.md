# Data Understanding

## Klasifikasi Tutupan Lahan Provinsi Jawa Timur — Pemahaman Data

---

## 1. Ringkasan Sumber Data

Proyek ini menggunakan dua jenis data utama: **data vektor** berupa poligon sampel hasil digitasi dan **data raster** berupa citra satelit Sentinel-2. Kedua data digabungkan melalui proses ekstraksi fitur spektral untuk menghasilkan dataset pelatihan dan pengujian model klasifikasi.

| Jenis Data | Format | Sumber | Deskripsi |
|-----------|--------|--------|-----------|
| Data Vektor (Poligon Sampel) | GeoJSON (`build.geojson`) | Digitasi manual | 250 poligon sampel tutupan lahan se-Jawa Timur |
| Data Raster (Citra Satelit) | GeoTIFF (`.tif`) | Sentinel-2 Level-2A via Microsoft Planetary Computer | Citra multispektral 6 band dengan resolusi ~60m |
| Dataset Fitur | CSV | Hasil ekstraksi | Fitur spektral per piksel dari setiap poligon |

---

## 2. Data Vektor — Poligon Sampel Digitasi

### 2.1 Deskripsi Umum

File `build.geojson` berisi **250 poligon sampel** yang diperoleh melalui digitasi manual pada citra satelit. Setiap poligon merepresentasikan area dengan tutupan lahan tertentu di wilayah Provinsi Jawa Timur.

- **Jumlah total poligon:** 250 sampel
- **Sistem koordinat:** WGS84 (EPSG:4326)
- **Kolom kelas:** `Type` (berisi kode kelas tutupan lahan)

### 2.2 Distribusi Kelas

Setiap kelas memiliki jumlah poligon yang **seimbang (balanced)** yaitu masing-masing 50 poligon:

| No | Kelas Tutupan Lahan | Kode | Jumlah Poligon | Warna Visualisasi |
|----|---------------------|------|:--------------:|-------------------|
| 1 | Pemukiman (Built-up) | `pemukiman` | 50 | 🔴 Merah (`#e74c3c`) |
| 2 | Lahan Pertanian (Sawah) | `pertanian` | 50 | 🟡 Kuning (`#f1c40f`) |
| 3 | Perairan (Water Body) | `air` | 50 | 🔵 Biru (`#0984e3`) |
| 4 | Hutan Biasa | `hutan` | 50 | 🟢 Hijau (`#27ae60`) |
| 5 | Hutan Mangrove | `mangrove` | 50 | 🟣 Ungu (`#8e44ad`) |

### 2.3 Cakupan Spasial

Poligon tersebar di seluruh wilayah Provinsi Jawa Timur dengan batas koordinat:

| Batas | Koordinat |
|-------|-----------|
| Ujung Barat (West) | 111.2518° BT |
| Ujung Timur (East) | 114.3613° BT |
| Ujung Selatan (South) | 8.2555° LS |
| Ujung Utara (North) | 7.1042° LS |

### 2.4 Atribut Data Vektor

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `geometry` | Polygon | Bentuk geometri poligon sampel |
| `Type` | String | Kode kelas tutupan lahan (`pemukiman`, `pertanian`, `air`, `hutan`, `mangrove`) |
| `kelas_kode` | String | Salinan kolom `Type` sebagai kode kelas |
| `kelas_nama` | String | Label deskriptif (misal: "Pemukiman (Built-up)") |

---

## 3. Data Raster — Citra Sentinel-2

### 3.1 Deskripsi Umum

Citra satelit yang digunakan adalah **Sentinel-2 Level-2A** (Surface Reflectance) yang diunduh melalui Microsoft Planetary Computer menggunakan API STAC dan pustaka `stackstac`.

### 3.2 Metadata Raster

| Parameter | Nilai |
|-----------|-------|
| **Nama File** | `sentinel2_jatim.tif` |
| **Ukuran File** | 257.14 MB |
| **Dimensi Raster** | 6.210 × 3.797 piksel |
| **Jumlah Band** | 6 band |
| **Sistem Koordinat** | EPSG:32749 |
| **Resolusi Spasial** | ~60 meter |
| **Level Produk** | Level-2A (Bottom-of-Atmosphere Reflectance) |

### 3.3 Band Spektral yang Digunakan

| No | Nama Band | Panjang Gelombang | Deskripsi | Kegunaan Utama |
|----|-----------|:-----------------:|-----------|----------------|
| 1 | **B02** | 490 nm | Blue | Deteksi badan air, aerosol |
| 2 | **B03** | 560 nm | Green | Deteksi vegetasi hijau |
| 3 | **B04** | 665 nm | Red | Penyerapan klorofil, pembeda vegetasi |
| 4 | **B08** | 842 nm | NIR (Near-Infrared) | Reflektansi tinggi vegetasi sehat |
| 5 | **B8A** | 865 nm | Narrow NIR | Klasifikasi vegetasi lebih detail |
| 6 | **B11** | 1610 nm | SWIR (Short-Wave Infrared) | Deteksi kelembaban tanah, area terbangun |

### 3.4 Bounding Box Raster

```
BoundingBox(
    left   = 515820.0,
    bottom = 9041940.0,
    right  = 888420.0,
    top    = 9269760.0
)
```
*Koordinat dalam sistem proyeksi UTM Zone 49S (EPSG:32749)*

---

## 4. Fitur Turunan (Derived Features / Spectral Indices)

Selain 6 band reflektansi asli, 4 **indeks spektral turunan** dihitung untuk meningkatkan kemampuan diskriminasi antar kelas:

| No | Indeks | Formula | Kegunaan |
|----|--------|---------|----------|
| 1 | **NDVI** (Normalized Difference Vegetation Index) | `(B08 - B04) / (B08 + B04)` | Membedakan area vegetasi dari non-vegetasi |
| 2 | **MNDWI** (Modified Normalized Difference Water Index) | `(B03 - B11) / (B03 + B11)` | Mendeteksi badan air dan area basah |
| 3 | **NDBI** (Normalized Difference Built-up Index) | `(B11 - B08) / (B11 + B08)` | Mengidentifikasi area terbangun |
| 4 | **Ratio B8A/B11** | `B8A / B11` | Membedakan jenis vegetasi (hutan vs mangrove) |

---

## 5. Dataset Hasil Ekstraksi

### 5.1 Ekstraksi Tingkat Poligon (Centroid)

Pada tahap awal, nilai spektral diekstraksi dari **titik centroid** setiap poligon:

| Parameter | Nilai |
|-----------|-------|
| Jumlah sampel berhasil diekstrak | 250 dari 250 poligon |
| Jumlah kolom fitur | 13 kolom |
| File output | `data/csv/fitur_spektral_sampel.csv` |

### 5.2 Ekstraksi Tingkat Piksel (Multi-Pixel)

Untuk memperkaya dataset, semua piksel valid di dalam setiap poligon diekstraksi:

| Parameter | Nilai |
|-----------|-------|
| Metode | Rasterisasi seluruh piksel di dalam poligon |
| Batas maksimal per poligon | 2.000 piksel |
| Penanganan tumpang tindih | Piksel dengan label ambigu dibuang |
| Informasi poligon asal | Disimpan dalam kolom `poligon_id` |

### 5.3 Kolom Fitur yang Digunakan untuk Klasifikasi

Total **10 fitur** digunakan sebagai input model:

| No | Nama Fitur | Tipe | Sumber |
|----|-----------|------|--------|
| 1 | `B02` | Numerik (float) | Band reflektansi asli |
| 2 | `B03` | Numerik (float) | Band reflektansi asli |
| 3 | `B04` | Numerik (float) | Band reflektansi asli |
| 4 | `B08` | Numerik (float) | Band reflektansi asli |
| 5 | `B8A` | Numerik (float) | Band reflektansi asli |
| 6 | `B11` | Numerik (float) | Band reflektansi asli |
| 7 | `NDVI` | Numerik (float) | Indeks turunan |
| 8 | `MNDWI` | Numerik (float) | Indeks turunan |
| 9 | `NDBI` | Numerik (float) | Indeks turunan |
| 10 | `Ratio_B8A_B11` | Numerik (float) | Indeks turunan |

---

## 6. Pembagian Data (Train/Test Split)

### 6.1 Strategi Pembagian

Pembagian dilakukan pada **tingkat poligon** (*polygon-based split*), bukan pada tingkat piksel, untuk mencegah **kebocoran data spasial** (*spatial data leakage*). Seluruh piksel dari satu poligon masuk ke kelompok yang sama (train **atau** test, tidak keduanya).

### 6.2 Komposisi Data

| Parameter | Train | Test |
|-----------|:-----:|:----:|
| **Jumlah poligon** | 184 (80%) | 46 (20%) |
| **Jumlah piksel** | 27.313 | 8.996 |
| **Jumlah fitur** | 10 | 10 |

### 6.3 Validasi Kebocoran

> ✅ **LULUS** — Tidak ada poligon yang masuk ke kelompok train dan test sekaligus.

---

## 7. Kepentingan Fitur (*Feature Importance*)

Berdasarkan model Random Forest yang dilatih, berikut adalah peringkat kontribusi setiap fitur:

| Peringkat | Fitur | Importance (%) |
|:---------:|-------|:--------------:|
| 1 | **Ratio_B8A_B11** | 14.27% |
| 2 | **MNDWI** | 13.44% |
| 3 | **NDVI** | 12.78% |
| 4 | **B02** | 12.63% |
| 5 | B03 | 8.71% |
| 6 | NDBI | 8.59% |
| 7 | B11 | 8.24% |
| 8 | B8A | 7.58% |
| 9 | B04 | 7.20% |
| 10 | B08 | 6.56% |

**Temuan utama:**
- Fitur turunan (Ratio, MNDWI, NDVI) mendominasi 3 peringkat teratas, menunjukkan bahwa indeks spektral sangat efektif dalam membedakan kelas tutupan lahan.
- Band B02 (Blue) memiliki kontribusi tinggi karena kemampuannya membedakan badan air dan area terbangun.
- Semua 10 fitur memiliki kontribusi yang relatif merata (6–14%), mengindikasikan tidak ada fitur yang redundan.

---

## 8. Evaluasi Kualitas Data

### 8.1 Kelebihan
- **Distribusi kelas seimbang** pada tingkat poligon (50 poligon per kelas).
- **Pembagian berbasis poligon** mencegah bias akibat autokorelasi spasial.
- **Fitur beragam** — kombinasi band asli dan indeks turunan meningkatkan kemampuan klasifikasi.
- **Sumber data terbuka** — Sentinel-2 tersedia gratis dan memiliki resolusi temporal tinggi.

### 8.2 Kekurangan / Perhatian
- **Ketidakseimbangan piksel pada data uji** — kelas Hutan Biasa mendominasi (7.798 piksel) dibandingkan Perairan (61 piksel), yang memengaruhi interpretasi metrik evaluasi.
- **Resolusi ~60m** — lebih kasar dari resolusi asli beberapa band Sentinel-2 (10m untuk B02, B03, B04, B08), sehingga detail spasial hilang akibat resampling.
- **Single temporal** — hanya menggunakan satu waktu perekaman, sehingga variasi musiman tidak tertangkap.
- **Kelas yang mirip secara spektral** — Hutan Biasa dan Hutan Mangrove memiliki karakteristik vegetasi yang serupa, begitu pula Pemukiman dan Lahan Pertanian yang kering.

---

## 9. Ringkasan Performa Model

| Level Evaluasi | Akurasi | Keterangan |
|---------------|:-------:|------------|
| **Piksel** | **90.00%** | Setiap piksel uji diklasifikasikan secara independen |
| **Poligon** (voting mayoritas) | **76.09%** | Label poligon ditentukan dari kelas terbanyak pada piksel-pikselnya |

### Detail per Kelas (Tingkat Piksel)

| Kelas | Precision | Recall | F1-Score | Support |
|-------|:---------:|:------:|:--------:|:-------:|
| Hutan Biasa | 0.95 | 0.95 | 0.95 | 7.798 |
| Hutan Mangrove | 0.98 | 0.82 | 0.89 | 218 |
| Lahan Pertanian (Sawah) | 0.23 | 0.43 | 0.30 | 116 |
| Pemukiman (Built-up) | 0.53 | 0.90 | 0.66 | 254 |
| Perairan (Water Body) | 0.62 | 0.44 | 0.51 | 610 |

### Detail per Kelas (Tingkat Poligon)

| Kelas | Precision | Recall | F1-Score | Support |
|-------|:---------:|:------:|:--------:|:-------:|
| Hutan Biasa | 0.77 | 1.00 | 0.87 | 10 |
| Hutan Mangrove | 1.00 | 0.90 | 0.95 | 10 |
| Lahan Pertanian (Sawah) | 0.57 | 0.44 | 0.50 | 9 |
| Pemukiman (Built-up) | 0.60 | 0.86 | 0.71 | 7 |
| Perairan (Water Body) | 0.86 | 0.60 | 0.71 | 10 |

**Catatan:** Kelas Lahan Pertanian dan Perairan memiliki performa lebih rendah karena jumlah piksel uji yang kecil serta kemiripan spektral dengan kelas lain.
