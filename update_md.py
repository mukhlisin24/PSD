import json

with open('notebooks/klasifikasiLahan.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 1. Intro Header
nb['cells'][0]['source'] = [
    "# Pemetaan & Klasifikasi Lahan Sawah dan Bukan Sawah Menggunakan Sentinel-2A & openEO\n",
    "\n",
    "Notebook ini berisi alur kerja komprehensif untuk klasifikasi tutupan lahan **Sawah** dan **Bukan Sawah (Pemukiman, Lahan Terbangun, dan Tanah Terbuka)** di wilayah **Kabupaten Lamongan, Jawa Timur**.\n",
    "\n",
    "Pendekatan yang digunakan memadukan penginderaan jauh (*remote sensing*) berbasis komputasi awan menggunakan citra optik **Sentinel-2A (Level-2A / Surface Reflectance)** via platform **openEO** (Copernicus Data Space Ecosystem) dengan algoritma Machine Learning **Random Forest Classifier**.\n",
    "\n",
    "---\n",
    "### 📌 Metodologi & Pencegahan Kebocoran Data (Spatial Data Leakage)\n",
    "Untuk mencegah bias evaluasi dan kebocoran data (*spatial data leakage*) akibat autokorelasi spasial antar-piksel dalam area poligon yang sama, pembagian dataset **70% Training** dan **30% Testing** dilakukan secara terstratifikasi pada tingkat **Poligon Sampel (Group-based Stratified Split)**.\n",
    "\n",
    "Berkas data hasil pembagian diekspor secara terstruktur ke dalam direktori `data/csv/split_dataset/`:\n",
    "1. **Tingkat Poligon (Area Sampel Lapangan):**\n",
    "   - `data_training_poligon.csv` : 70 Poligon Sampel Latih (34 Sawah, 36 Bukan Sawah)\n",
    "   - `data_testing_poligon.csv`  : 30 Poligon Sampel Uji (14 Sawah, 16 Bukan Sawah)\n",
    "2. **Tingkat Piksel Spektral (Fitur Reflektansi & Indeks Spektral):**\n",
    "   - `fitur_piksel_training.csv` : 6.934 Baris Piksel Data Latih (Hanya digunakan untuk melatih model)\n",
    "   - `fitur_piksel_testing.csv`  : 2.601 Baris Piksel Data Uji (Murni untuk menguji performa generalisasi model)\n"
]

# 2. Section 1: GeoJSON & Split
nb['cells'][1]['source'] = [
    "## 1. Data Masukan Geospasial & Pembagian Dataset Poligon (Train vs Test)\n",
    "\n",
    "Tahap awal membaca berkas geospasial vector `data/geojson/lamongan.geojson` yang terdiri atas **101 geometri**:\n",
    "- **1 Poligon Batas Wilayah**: Mendefinisikan batas administratif area studi untuk pengunduhan citra Sentinel-2A.\n",
    "- **48 Poligon Sawah**: Area observasi sampel tutupan lahan persawahan.\n",
    "- **52 Poligon Bukan Sawah**: Area observasi sampel pemukiman, kawasan terbangun, infrastruktur, dan lahan non-vegetasi.\n",
    "\n",
    "Setiap poligon diberikan **ID Unik** (`sawah_01..48`, `bukan_sawah_01..52`). Pembagian dilakukan secara terstratifikasi (*Stratified Split*) sebesar 70% data latih (70 poligon: 34 Sawah, 36 Bukan Sawah) dan 30% data uji (30 poligon: 14 Sawah, 16 Bukan Sawah).\n"
]

# 3. Section 2: Fitur Spektral
nb['cells'][3]['source'] = [
    "## 2. Ekstraksi Fitur Spektral & Pembentukan Dataset Piksel (Latih & Uji)\n",
    "\n",
    "Pada tahap ini, dilakukan proses *masking* spasial antara citra raster Sentinel-2A dengan geometri poligon sampel. Dari setiap piksel yang berada di dalam poligon, diekstrak 5 kanal reflektansi dasar dan dihitung 3 indeks spektral kunci:\n",
    "\n",
    "### 🧪 Kanal & Indeks Spektral yang Dihitung:\n",
    "1. **Kanal Reflektansi Dasar:**\n",
    "   - `B02` (Blue, 490 nm) : Reflektansi spektrum biru.\n",
    "   - `B03` (Green, 560 nm): Reflektansi spektrum hijau (sensitif terhadap klorofil & kebasahan).\n",
    "   - `B04` (Red, 665 nm)  : Reflektansi spektrum merah (penyerapan tinggi oleh tanaman hijau).\n",
    "   - `B08` (NIR, 842 nm)  : Reflektansi inframerah dekat (sangat tinggi pada struktur kanopi daun).\n",
    "   - `B11` (SWIR, 1610 nm): Reflektansi inframerah gelombang pendek (sensitif terhadap kadar air dan lahan terbangun).\n",
    "\n",
    "2. **Indeks Spektral:**\n",
    "   - **NDVI (*Normalized Difference Vegetation Index*):**\n",
    "     $$\\text{NDVI} = \\frac{\\text{B08} - \\text{B04}}{\\text{B08} + \\text{B04}}$$\n",
    "     Mengukur tingkat kerapatan dan kehijauan vegetasi tanaman padi (nilai sawah tinggi ~0.61, nilai bukan sawah rendah ~0.19).\n",
    "   - **NDWI (*Normalized Difference Water Index*):**\n",
    "     $$\\text{NDWI} = \\frac{\\text{B03} - \\text{B08}}{\\text{B03} + \\text{B08}}$$\n",
    "     Mengukur kebasahan permukaan dan kandungan air pada petak sawah.\n",
    "   - **NDBI (*Normalized Difference Built-up Index*):**\n",
    "     $$\\text{NDBI} = \\frac{\\text{B11} - \\text{B08}}{\\text{B11} + \\text{B08}}$$\n",
    "     Membedakan lahan terbangun/pemukiman (nilai positif ~+0.14) dari lahan sawah vegetatif (nilai negatif ~-0.26).\n",
    "\n",
    "### 📊 Hasil Ekstraksi Dataset Piksel:\n",
    "- **6.934 piksel Latih** diekspor ke `data/csv/split_dataset/fitur_piksel_training.csv`\n",
    "- **2.601 piksel Uji** diekspor ke `data/csv/split_dataset/fitur_piksel_testing.csv`\n"
]

# 4. Section 3: Modeling
nb['cells'][5]['source'] = [
    "## 3. Pemodelan Machine Learning (Random Forest) & Evaluasi Performa\n",
    "\n",
    "Model **Random Forest Classifier** dibangun dengan konfigurasi:\n",
    "- `n_estimators=300`: Menggunakan ensemble 300 pohon keputusan (*decision trees*) untuk stabilitas prediksi.\n",
    "- `class_weight=\"balanced\"`: Menyeimbangkan bobot kelas sampel.\n",
    "- `random_state=42`: Menjamin replikabilitas eksperimen.\n",
    "\n",
    "Model dilatih murni menggunakan **6.934 piksel data latih** dan dievaluasi secara independen pada **2.601 piksel data uji** yang belum pernah dilihat sebelumnya.\n",
    "\n",
    "Evaluasi mencakup matriks performa komprehensif:\n",
    "- **Akurasi Data Latih vs Data Uji**\n",
    "- **Cohen's Kappa Score** (Tingkat kesepakatan prediksi terhadap kebenaran lapangan tanpa faktor kebetulan)\n",
    "- **Confusion Matrix** (Jumlah True Positive, False Positive, False Negative, True Negative)\n",
    "- **Classification Report** (Precision, Recall, dan F1-Score per kelas)\n",
    "- **Feature Importances** (Peringkat fitur yang paling berkontribusi dalam pemisahan kelas)\n"
]

# 5. Section 4: 2D & 3D Map
nb['cells'][7]['source'] = [
    "## 4. Visualisasi Peta Tutupan Lahan 2D & Peta 3D Interaktif\n",
    "\n",
    "Setelah model terlatih dengan baik, dilakukan inferensi prediksi piksel-demi-piksel terhadap keseluruhan citra raster Sentinel-2A area studi untuk menghasilkan berkas Geotiff klasifikasi `data/tif/klasifikasi_sawah_pemukiman.tif`.\n",
    "\n",
    "Pada tahap ini disajikan dua bentuk visualisasi:\n",
    "1. **Peta Klasifikasi 2D (Matplotlib):** Menampilkan sebaran spasial kelas Sawah (hijau) dan Bukan Sawah (oranye) beserta statistik jumlah piksel dan persentase luas lahan.\n",
    "2. **Peta 3D Interaktif (Plotly Surface):** Memetakan tutupan lahan ke atas grid permukaan 3D interaktif yang dapat diputar (*rotate*), digeser (*pan*), dan diperbesar (*zoom*) langsung di dalam notebook.\n"
]

with open('notebooks/klasifikasiLahan.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print('SUCCESS: Berhasil memperbarui teks markdown di notebooks/klasifikasiLahan.ipynb!')
