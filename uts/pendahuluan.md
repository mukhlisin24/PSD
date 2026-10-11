# Pendahuluan: Klasifikasi Tutupan Lahan Jawa Timur

## Profil Mahasiswa

| Keterangan | Informasi |
| :--- | :--- |
| **Nama** | Irwan Dwi Mukhlisin |
| **NIM** | 240411100010 |
| **Program Studi** | Teknik Informatika |
| **Mata Kuliah** | Proyek Sains Data (PSD) |
| **Kelas** | IF 5B |
| **Topik Proyek** | Klasifikasi Tutupan Lahan (*Land Cover Classification*) Berbasis Citra Satelit |

---

## 1. Pengantar Proyek

Selamat datang di proyek **Klasifikasi Tutupan Lahan Provinsi Jawa Timur** — sebuah implementasi sains data geospasial (*geospatial data science*) dan *machine learning* untuk memetakan serta menganalisis sebaran tutupan permukaan bumi di Provinsi Jawa Timur secara otomatis dan akurat.

Tutupan lahan (*land cover*) merupakan atribut biofisik permukaan bumi yang mencakup vegetasi, tanah terbuka, air, lahan pertanian, maupun struktur bangunan buatan manusia. Informasi mengenai tutupan lahan merupakan data fundamental yang sangat krusial bagi berbagai sektor strategis, antara lain:
- **Perencanaan Tata Ruang Wilayah (RTRW)**: Memastikan pemanfaatan ruang yang selaras dengan kapasitas lingkungan hidup.
- **Konservasi Ekosistem**: Memantau kelestarian hutan lindung dan hutan mangrove di pesisir pantai.
- **Ketahanan Pangan**: Mengawasi alih fungsi lahan sawah dan lahan pertanian produktif.
- **Mitigasi Bencana Lingkungan**: Mendeteksi deforestasi dan degradasi lahan yang berisiko memicu banjir serta tanah longsor.

Secara konvensional, survei lapangan langsung (*terrestrial survey*) membutuhkan biaya operasional yang sangat mahal, waktu yang lama, dan memiliki keterbatasan aksesibilitas pada area terpencil. Melalui proyek ini, pendekatan **Penginderaan Jauh (*Remote Sensing*)** dipadukan dengan algoritma **Machine Learning (Random Forest)** untuk menghasilkan peta tutupan lahan resolusi tinggi secara efisien dan objektif.

---

## 2. Wilayah Kajian: Provinsi Jawa Timur

Wilayah studi mencakup seluruh daratan dan pesisir **Provinsi Jawa Timur** dengan batas geografis:
- **Bujur Barat (West)**: 111.2518° BT
- **Bujur Timur (East)**: 114.3613° BT
- **Lintang Selatan (South)**: -8.2555° LS
- **Lintang Utara (North)**: -7.1042° LS

Jawa Timur memiliki topografi dan karakteristik bentang lahan yang sangat kaya dan bervariasi:
- **Pesisir Utara dan Selatan**: Area tambak, muara sungai, dan ekosistem mangrove pelindung pantai.
- **Dataran Rendah dan Lembah Sungai**: Sentra lumbung padi nasional (DAS Bengawan Solo dan DAS Brantas) dengan sawah irigasi intensif.
- **Kawasan Perkotaan dan Industri**: Aglomerasi metropolitan (Surabaya Raya, Malang Raya, Sidoarjo, Gresik) dengan kerapatan bangunan tinggi.
- **Zona Pegunungan dan Dataran Tinggi**: Kompleks hutan hujan tropis dan hutan pegunungan di sekitar jajaran gunung berapi (Semeru, Bromo, Arjuno, Welirang, Raung, Ijen).

---

## 3. Mengenal 5 Kelas Tutupan Lahan Utama

Berdasarkan karakteristik permukaan dan kebutuhan analisis wilayah Jawa Timur, tutupan lahan diklasifikasikan ke dalam **5 kelas utama**:

```
                                TUTUPAN LAHAN JAWA TIMUR
                                           │
         ┌───────────────┬─────────────────┼────────────────┬────────────────┐
         ▼               ▼                 ▼                ▼                ▼
   [ Pemukiman ]   [ Pertanian ]      [ Perairan ]     [ Hutan Biasa ]  [ Mangrove ]
   Area Terbangun   Sawah & Ladang   Sungai, Danau,    Hutan Tropis     Hutan Pesisir
   & Infrastruktur   Budidaya         Waduk, Laut       Daratan         Payau / Pantai
```

### 3.1 Pemukiman (Built-up)
- **Karakteristik**: Area yang didominasi oleh tutupan buatan manusia (*impervious surface*), mencakup kompleks perumahan, kawasan komersial, gedung pemerintahan, kawasan industri, dan jaringan jalan raya.
- **Ciri Spektral**: Memiliki nilai reflektansi tinggi pada band *Short-Wave Infrared* (SWIR / B11) dan indeks **NDBI** bernilai positif, dengan vegetasi yang sangat minim.
- **Simbol Warna**: 🔴 Merah (`#e74c3c`)

### 3.2 Lahan Pertanian (Sawah)
- **Karakteristik**: Area pertanian aktif, terutama sawah irigasi dan lahan basah tanaman pangan. Tutupan ini memiliki dinamika musiman tinggi (periode genangan air, masa tumbuh hijau, dan masa panen/bera).
- **Ciri Spektral**: Menampilkan kombinasi pantulan air saat fase penggenangan dan respon klorofil tinggi pada fase vegetatif. Memiliki nilai NDVI sedang hingga tinggi serta kelembaban tanah yang tinggi.
- **Simbol Warna**: 🟡 Kuning (`#f1c40f`)

### 3.3 Perairan (Water Body)
- **Karakteristik**: Badan air terbuka seperti sungai besar (Bengawan Solo, Brantas), waduk (Karangkates, Sutami, Selorejo), danau alami, muara, dan perairan pesisir.
- **Ciri Spektral**: Menyerap hampir seluruh radiasi inframerah dekat (*Near-Infrared* / NIR) dan inframerah gelombang pendek (SWIR), namun memantulkan spektrum biru-hijau (B02 dan B03). Memiliki nilai indeks **MNDWI** sangat tinggi (> 0) dan NDVI sangat rendah (< 0).
- **Simbol Warna**: 🔵 Biru (`#0984e3`)

### 3.4 Hutan Biasa
- **Karakteristik**: Formasi vegetasi berkayu alami dengan tajuk rapat di kawasan dataran tinggi, lereng pegunungan, dan kawasan konservasi daratan Jawa Timur.
- **Ciri Spektral**: Penyerapan kuat pada spektrum merah (B04) karena konsentrasi klorofil tinggi, dan pantulan sangat kuat pada inframerah dekat (B08 / B8A). Menghasilkan indeks **NDVI** yang sangat tinggi (> 0.6).
- **Simbol Warna**: 🟢 Hijau (`#27ae60`)

### 3.5 Hutan Mangrove
- **Karakteristik**: Ekosistem hutan pantai pasang-surut (*intertidal zone*) yang khas tumbuh di sepanjang muara sungai dan pantai berlumpur (misalnya di pesisir Ujung Pangkah Gresik, Surabaya Timur, Probolinggo, dan Banyuwangi).
- **Ciri Spektral**: Memiliki respons spektral mirip hutan tropis pada band NIR, namun substrat tanah yang tergenang air asin menyebabkan nilai serapan SWIR lebih tinggi dibanding hutan daratan biasa. Rasio **B8A / B11** dan nilai **MNDWI** menjadi fitur diskriminan penting untuk membedakannya dari hutan biasa.
- **Simbol Warna**: 🟣 Ungu (`#8e44ad`)

---

## 4. Pendekatan dan Teknologi yang Digunakan

Proyek ini mengintegrasikan rantai teknologi (*tech stack*) modern berbasis Python:

| Komponen | Teknologi | Deskripsi dan Fungsi |
| :--- | :--- | :--- |
| **Sumber Data Raster** | **Copernicus Sentinel-2 L2A** | Citra multispektral 6 band (B02, B03, B04, B08, B8A, B11) koreksi atmosfer BOA melalui Microsoft Planetary Computer STAC API |
| **Sumber Data Vektor** | **GeoJSON (`build.geojson`)** | 250 poligon sampel representatif (50 poligon per kelas) hasil digitasi se-Jawa Timur |
| **Pengolahan Geospasial** | **GeoPandas & Rasterio** | Manipulasi vektor CRS (EPSG:4326 ke EPSG:32749), *raster masking*, dan ekstraksi nilai spektral piksel |
| **Ekstraksi Fitur Spektral** | **Indeks Turunan Spektral** | Perhitungan formula NDVI, MNDWI, NDBI, dan Rasio B8A/B11 untuk mempertajam kontras spektral |
| **Algoritma Klasifikasi** | **Random Forest Classifier** | Model *ensemble learning* berbasis 200 *decision trees* dengan pembobotan kelas seimbang (`class_weight="balanced"`) |
| **Validasi Bebas Bocor** | **Polygon-Based Train/Test Split** | Pembagian data uji dan latih berdasarkan ID poligon (bukan piksel acak) guna mencegah *spatial autocorrelation leakage* |
| **Visualisasi Interaktif** | **Folium & Matplotlib** | Pembuatan peta interaktif berbasis Leaflet dengan multi-basemap dan overlay hasil klasifikasi |

---

## 5. Struktur dan Alur Dokumentasi

Dokumentasi proyek ini disusun secara bertahap dan terstruktur mengikuti metodologi sains data standar industri (**CRISP-DM**):

```
                        DOKUMENTASI PROYEK
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
  [ 1. Pendahuluan ]    [ 2. Business ]         [ 3. Data ]
  - Profil Pengembang   - Latar Belakang        - Metadata Raster
  - Urgensi Kajian      - Tujuan Proyek         - Data Poligon
  - 5 Kelas Lahan       - Manfaat & Lingkup     - Ekstraksi Fitur
  - Teknologi Kunci     - Kriteria Sukses       - Evaluasi Kualitas
```

Berikut tautan menuju dokumen pemahaman lanjutan:
1. **[Business Understanding](file:///d:/SEMESTER%205/psd/uts/business_understanding.md)**: Menguraikan latar belakang masalah, tujuan bisnis dan teknis, manfaat multi-sektor, kriteria keberhasilan kuantitatif, stakeholder, alur kerja proyek, serta batasan implementasi.
2. **[Data Understanding](file:///d:/SEMESTER%205/psd/uts/data_understanding.md)**: Menjelaskan profil lengkap data vektor poligon, spesifikasi raster Sentinel-2A, band spektral, formula indeks turunan, strategi split data tanpa kebocoran spasial, *feature importance*, dan evaluasi performa model.
3. **[Notebook Implementasi Utama](file:///d:/SEMESTER%205/psd/uts/klasifikasi%20tutupan%20lahan%20jatim.ipynb)**: Berisi keseluruhan kode komputasi, mulai dari unduh citra, ekstraksi piksel, pelatihan model, evaluasi metrik, hingga ekspor peta tematik dan keluaran Streamlit.
