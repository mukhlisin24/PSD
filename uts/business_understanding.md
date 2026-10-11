# Business Understanding

## Klasifikasi Tutupan Lahan Provinsi Jawa Timur Menggunakan Citra Sentinel-2 dan Random Forest

---

## 1. Latar Belakang

Provinsi Jawa Timur merupakan salah satu provinsi terluas di Pulau Jawa dengan keragaman tutupan lahan yang tinggi, meliputi kawasan permukiman, lahan pertanian (sawah), perairan, hutan, dan hutan mangrove. Pemantauan perubahan tutupan lahan secara berkala sangat penting untuk mendukung perencanaan tata ruang, pengelolaan sumber daya alam, pelestarian lingkungan, serta mitigasi bencana.

Metode konvensional pemetaan tutupan lahan berbasis survei lapangan memiliki keterbatasan dari segi biaya, waktu, dan cakupan wilayah. Oleh karena itu, pemanfaatan **citra satelit penginderaan jauh** yang dikombinasikan dengan **teknik machine learning** menjadi solusi yang efisien dan skalabel untuk memetakan tutupan lahan pada wilayah yang luas.

---

## 2. Tujuan Proyek

### 2.1 Tujuan Utama

Membangun model klasifikasi tutupan lahan di Provinsi Jawa Timur menggunakan citra satelit **Sentinel-2 Level-2A** dan algoritma **Random Forest**, sehingga menghasilkan peta tematik tutupan lahan yang akurat dan dapat dianalisis secara spasial.

### 2.2 Tujuan Khusus

1. **Mengidentifikasi dan memetakan** lima kelas tutupan lahan utama di Jawa Timur:
   - **Pemukiman (Built-up)** — area terbangun dan infrastruktur perkotaan/pedesaan.
   - **Lahan Pertanian (Sawah)** — area persawahan dan lahan budidaya tanaman.
   - **Perairan (Water Body)** — sungai, waduk, danau, dan badan air lainnya.
   - **Hutan Biasa** — kawasan hutan alami non-mangrove.
   - **Hutan Mangrove** — ekosistem mangrove di pesisir pantai.

2. **Mengekstraksi fitur spektral** dari citra Sentinel-2 berupa band reflektansi dan indeks turunan (NDVI, MNDWI, NDBI, Ratio B8A/B11) untuk membedakan karakteristik setiap kelas tutupan lahan.

3. **Melatih dan mengevaluasi** model Random Forest dengan pendekatan pembagian data berbasis poligon (*polygon-based split*) agar evaluasi mencerminkan kemampuan generalisasi model pada wilayah baru yang belum pernah dilihat saat pelatihan.

4. **Menghasilkan peta klasifikasi interaktif** yang dapat digunakan oleh pemangku kepentingan untuk analisis spasial lebih lanjut.

---

## 3. Manfaat Proyek

| Aspek | Manfaat |
|-------|---------|
| **Perencanaan Tata Ruang** | Menyediakan informasi distribusi tutupan lahan untuk perencanaan pembangunan dan tata guna lahan |
| **Pengelolaan Lingkungan** | Memantau luasan hutan dan mangrove untuk program konservasi dan restorasi ekosistem |
| **Pertanian** | Mengidentifikasi sebaran lahan pertanian untuk mendukung kebijakan ketahanan pangan |
| **Mitigasi Bencana** | Mendeteksi perubahan lahan yang berpotensi meningkatkan risiko banjir atau longsor |
| **Akademik** | Mengimplementasikan teknik penginderaan jauh dan machine learning dalam studi kasus nyata |

---

## 4. Ruang Lingkup

### 4.1 Cakupan Wilayah

- **Provinsi:** Jawa Timur
- **Batas Koordinat (Bounding Box):**
  - Barat (West): 111.2518° BT
  - Timur (East): 114.3613° BT
  - Selatan (South): 8.2555° LS
  - Utara (North): 7.1042° LS

### 4.2 Kelas Tutupan Lahan

Klasifikasi dilakukan terhadap **5 kelas** tutupan lahan:

| No | Kode Kelas | Nama Kelas | Deskripsi |
|----|-----------|------------|-----------|
| 1 | `pemukiman` | Pemukiman (Built-up) | Area terbangun, permukiman, dan infrastruktur |
| 2 | `pertanian` | Lahan Pertanian (Sawah) | Sawah irigasi dan lahan budidaya pertanian |
| 3 | `air` | Perairan (Water Body) | Sungai, danau, waduk, dan badan air |
| 4 | `hutan` | Hutan Biasa | Hutan tropis alami non-mangrove |
| 5 | `mangrove` | Hutan Mangrove | Ekosistem mangrove di kawasan pesisir |

### 4.3 Metodologi

- **Sumber Data Satelit:** Sentinel-2 Level-2A (diakses via Microsoft Planetary Computer / STAC)
- **Algoritma Klasifikasi:** Random Forest (`n_estimators=200`, `class_weight="balanced"`)
- **Strategi Pembagian Data:** Polygon-based split (80% train, 20% test) untuk menghindari kebocoran data spasial
- **Level Analisis:** Berbasis piksel (*pixel-based classification*)

---

## 5. Kriteria Keberhasilan

| Kriteria | Target |
|----------|--------|
| Akurasi tingkat piksel | ≥ 85% |
| Akurasi tingkat poligon (voting mayoritas) | ≥ 70% |
| Tidak ada kebocoran data antara train dan test | Lulus validasi |
| Peta klasifikasi dapat divisualisasikan secara interaktif | Tersedia dalam format HTML |

### Hasil yang Dicapai

- **Akurasi piksel:** 90.00%
- **Akurasi poligon:** 76.09%
- **Validasi kebocoran data:** LULUS — tidak ada poligon yang masuk ke dua split sekaligus

---

## 6. Alur Kerja (*Workflow*)

```
1. Persiapan Library & Direktori
        │
        ▼
2. Membaca Poligon Sampel Digitasi (GeoJSON)
        │
        ▼
3. Visualisasi Peta Interaktif Poligon
        │
        ▼
4. Mengunduh Citra Sentinel-2 (Planetary Computer)
        │
        ▼
5. Memeriksa Metadata & Membaca Band Raster
        │
        ▼
6. Ekstraksi Fitur Spektral (Band + Indeks Turunan)
        │
        ▼
7. Pembagian Train/Test Berdasarkan Poligon
        │
        ▼
8. Pelatihan Random Forest & Evaluasi Model
        │
        ▼
9. Klasifikasi Seluruh Raster & Peta Tutupan Lahan
```

---

## 7. Stakeholder

| Stakeholder | Peran |
|-------------|-------|
| Mahasiswa / Peneliti | Pelaksana analisis dan pengembangan model |
| Dosen Pembimbing | Supervisi dan validasi metodologi |
| Pemerintah Daerah Jawa Timur | Pengguna potensial hasil peta untuk perencanaan wilayah |
| Komunitas Lingkungan | Pemanfaatan data hutan dan mangrove untuk program konservasi |

---

## 8. Asumsi dan Batasan

### Asumsi
- Citra Sentinel-2 yang digunakan memiliki kualitas reflektansi yang baik (minim tutupan awan).
- Poligon sampel digitasi mewakili keragaman kondisi setiap kelas tutupan lahan.
- Fitur spektral dan indeks turunan cukup representatif untuk membedakan kelima kelas.

### Batasan
- Klasifikasi terbatas pada **5 kelas** utama; kelas lain (seperti lahan terbuka, tambak, atau rawa) tidak dimodelkan secara terpisah.
- Resolusi citra diresample ke **~60 meter**, sehingga objek-objek kecil mungkin tidak terdeteksi dengan baik.
- Model belum mempertimbangkan aspek temporal (multi-waktu) dan hanya menggunakan satu periode citra.
- Kelas dengan jumlah piksel yang sedikit (seperti Perairan dan Lahan Pertanian pada data uji) berpotensi menghasilkan evaluasi yang kurang stabil.
