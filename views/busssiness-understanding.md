# Business & Data Understanding

## Business Understanding: Mengamati Kualitas Udara

**Indeks Kualitas Udara (Air Quality Index - AQI)** adalah ukuran yang digunakan untuk menilai seberapa bersih atau tercemar udara di suatu wilayah tertentu, serta dampaknya terhadap kesehatan manusia. Nilai AQI yang tinggi menunjukkan tingkat polusi udara yang lebih parah dan potensi risiko kesehatan yang lebih besar.

**Polutan yang Mempengaruhi Kualitas Udara**
Kualitas udara yang baik atau buruk sangat dipengaruhi oleh keberadaan gas-gas dan partikel berbahaya di atmosfer (polutan). Polutan ini umumnya berasal dari asap kendaraan, aktivitas industri, pembakaran lahan, maupun limbah. Beberapa unsur utama penyebab pencemaran udara meliputi:
*   **NO2 (Nitrogen Dioksida):** Gas beracun yang umumnya dihasilkan oleh pembakaran bahan bakar kendaraan bermotor dan emisi pabrik industri.
*   **CO (Karbon Monoksida):** Gas tidak berwarna dan tidak berbau yang beracun, berasal dari pembakaran tidak sempurna seperti dari knalpot kendaraan.


**Profil Wilayah: Kabupaten Lamongan**
Kabupaten Lamongan adalah salah satu kabupaten yang terletak di Provinsi Jawa Timur, Indonesia. Wilayah ini memiliki karakteristik geografis dan ekonomi yang beragam, mulai dari kawasan pesisir di utara hingga dataran rendah yang didominasi oleh aktivitas pertanian, perikanan, perdagangan, serta sektor industri yang terus berkembang. Peningkatan volume kendaraan bermotor, operasional pabrik, dan aktivitas harian masyarakat di Lamongan berpotensi memengaruhi kondisi lingkungan, khususnya kualitas udara.

Oleh karena itu, dari beberapa unsur polutan yang ada, studi di wilayah **Kabupaten Lamongan** ini akan berfokus **mengamati kadar NO2 dan CO** menggunakan tangkapan citra satelit untuk menganalisis kualitas udara setempat secara lebih mendalam.

## Data Understanding

Pada tahap ini, kita akan melakukan eksplorasi data mentah yang telah ditarik, membersihkan anomali, serta memvisualisasikannya agar mudah dipahami.

## Parameter Pencarian Data

*   **Sumber Data:** Copernicus Data Space Ecosystem (Sentinel-5P)
*   **Waktu Observasi:** 24 Agustus 2025 - 24 Agustus 2026
*   **Bounding Box (Lamongan):**
    *   Longitude: `112.0111` hingga `112.6139`
    *   Latitude: `-7.4250` hingga `-6.8222`

## Lingkungan & Tools

Untuk mengeksekusi ekstraksi dan visualisasi, kita memanfaatkan:
*   **Akun Copernicus:** Untuk akses API citra satelit NetCDF.
*   **geojson.io:** Pemetaan manual Bounding Box Lamongan.


