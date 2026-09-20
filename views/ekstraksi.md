---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Preprocessing dan Ekstraksi Fitur

## Preprocessing: Menangani Missing Value Dan Outlier

### Deteksi Missing Value (Interpolasi linear)

Missing value adalah kondisi ketika terdapat nilai yang tidak tersedia atau kosong pada suatu dataset. Missing value biasanya ditandai dengan nilai `NaN`, `None`, atau sel kosong. Interpolasi linear merupakan metode yang digunakan untuk mengisi nilai yang hilang (missing value) dengan memperkirakan nilai tersebut berdasarkan nilai yang berada sebelum dan sesudah data yang kosong. Metode ini mengasumsikan bahwa perubahan nilai di antara dua titik data berlangsung secara linier atau bertahap.

Pada penelitian ini, missing value perlu diperiksa karena dapat memengaruhi hasil analisis dan visualisasi data. Data yang memiliki nilai kosong dapat menyebabkan proses perhitungan statistik, pembuatan grafik, maupun proses deteksi outlier menjadi kurang optimal.
Pada dataset kualitas udara, missing value dapat terjadi karena beberapa faktor, seperti data sensor yang tidak terekam, gangguan proses pengambilan data, atau adanya data yang tidak tersedia pada periode tertentu. Pada slide Data Understanding pada polutan CO yaitu sebanyak 76 data mising value. Dan disini saya akan menggunkan Interpolasi untuk menangani missing value.

```{code-cell}
import pandas as pd

# Membaca data
df = pd.read_csv("../data/CO_lamongan.csv")

# Mengubah kolom CO menjadi numerik
df["CO"] = pd.to_numeric(
    df["CO"],
    errors="coerce"
)

# Jika masih ada missing di awal/akhir, isi dengan nilai terdekat
df["CO"] = df["CO"].ffill()
df["CO"] = df["CO"].bfill()

# Mengisi missing value dengan interpolasi
df["CO"] = df["CO"].interpolate(
    method="linear"
)

df.to_csv("data/CO_lamongan_missing.csv", index=False)
print("File berhasil disimpan sebagai CO_lamongan_missing.csv")
print("\nMissing value setelah imputasi:")
print(df["CO"].isnull().sum())
```

```{image} ../img/jumlah_missing_co.png
:alt: Grafik Data
:width: 100%
:align: center
```

### Deteksi Outlier (Metode Interquartile Range)

Interquartile Range (IQR) adalah metode statistik yang digunakan untuk mengukur penyebaran data pada bagian tengah distribusi dan dapat digunakan untuk mendeteksi outlier. IQR dihitung dari selisih antara kuartil ketiga (Q3) dan kuartil pertama (Q1). Pada penelitian kualitas udara, metode IQR digunakan untuk mengidentifikasi nilai konsentrasi CO yang menyimpang dari sebagian besar data. Nilai CO yang berada di luar batas IQR akan ditandai sebagai outlier dan kemudian dapat dianalisis lebih lanjut untuk mengetahui apakah nilai tersebut merupakan kesalahan data atau memang menunjukkan kondisi konsentrasi CO yang ekstrem.

```
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("CO_lamongan_sorted.csv")
df["CO"] = pd.to_numeric(df["CO"], errors="coerce")

# Menghitung Q1 dan Q3
Q1 = df["CO"].quantile(0.25)
Q3 = df["CO"].quantile(0.75)

# Menghitung IQR
IQR = Q3 - Q1

# Menentukan batas
batas_bawah = Q1 - 1.5 * IQR
batas_atas = Q3 + 1.5 * IQR

# Menentukan status data
df["status"] = df["CO"].apply(
    lambda x: "Outlier"
    if x < batas_bawah or x > batas_atas
    else "Normal"
)
outliers_iqr = df[df["status"] == "Outlier"]

print("\nJumlah data:")
print(df["status"].value_counts())

print("\nData Outlier:")
print(df[df["status"] == "Outlier"][["date", "CO"]])
```

```{image} ../img/jumlah_outlier_co.png
:alt: Grafik Data
:width: 100%
:align: center
```

```
plt.figure(figsize=(15, 5))

# Grafik CO
plt.plot(
    df["date"],
    df["CO"],
    label="CO",
    linewidth=1
)

# Titik outlier
plt.scatter(
    outliers_iqr["date"],
    outliers_iqr["CO"],
    color="red",
    marker="o",
    label="Outliers"
)

# Batas atas IQR
plt.axhline(
    batas_atas,
    color="orange",
    linestyle="dashed",
    label="Upper Bound (IQR)"
)

# Batas bawah IQR
plt.axhline(
    batas_bawah,
    color="blue",
    linestyle="dashed",
    label="Lower Bound (IQR)"
)

# Judul dan label
plt.title("Deteksi Outlier Data CO (Metode IQR)")
plt.xlabel("Bulan")
plt.ylabel("Kadar CO")

# Menampilkan bulan pada sumbu X
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%B"))

plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
```

```{image} ../img/grafik_outlier_coo.png
:alt: Grafik Data
:width: 100%
:align: center
```
###  Perbandingan Deteksi Outlier Metode Machine Learning (PyOD)

Selain menerapkan pendekatan statistik konvensional seperti **Interquartile Range (IQR)** untuk mengidentifikasi data pencilan, analisis juga diperluas dengan membandingkan beberapa algoritma deteksi outlier yang tersedia dalam pustaka **PyOD**. Sebanyak **3 metode berbasis Machine Learning dan probabilitas** digunakan dalam pengujian. Ketiga metode tersebut memiliki pendekatan dan karakteristik algoritma yang berbeda dalam mengenali pola data yang dianggap tidak normal atau menyimpang dari data lainnya:
- **KNN (*k-Nearest Neighbors*)**: Mengukur jarak suatu data ke k-tetangga terdekat. Jika jaraknya jauh, titik tersebut dianggap outlier.
- **Isolation Forest**: Memisahkan data secara acak menggunakan pohon biner; titik anomali lebih cepat terisolasi.
- **ECOD (*Empirical Cumulative Distribution Functions*)**: Menilai anomali berdasarkan fungsi distribusi kumulatif empiris pada ekor data.

Berikut kode implementasi untuk deteksi outlier dengan metode PyOD :

```
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from pyod.models.knn import KNN
from pyod.models.iforest import IForest
from pyod.models.ecod import ECOD

pollutants = ['CH4', 'CO', 'NO2', 'SO2']

BULAN_MAP = {
    1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni', 
    7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
}

summary_dynamic = []

for pol in pollutants:
    # 1. Load Data
    file_path = f"{pol}_lamongan_missing.csv"
    if not os.path.exists(file_path):
        file_path = f"data/{pol}_lamongan_missing.csv"
    
    df_p = pd.read_csv(file_path)
    df_p['date'] = pd.to_datetime(df_p['date'])
    df_valid = df_p.dropna(subset=[pol]).copy()
    
    # 2. Standarisasi Data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_valid[[pol]].values)
    
    # 3. Model PyOD
    models = {
        'KNN': KNN(n_neighbors=5),
        'Isolation Forest': IForest(random_state=42),
        'ECOD': ECOD()
    }
    
    print("=" * 75)
    print(f"       DETEKSI OUTLIER DINAMIS (PyOD Anomaly Score) — {pol}")
    print("=" * 75)
    print(f"Total Data Valid: {len(df_valid)} hari\n")
    
    for name, model in models.items():
        # Training model tanpa memaksakan fixed contamination
        model.fit(X_scaled)
        
        # Ambil skor anomali kontinu (semakin tinggi = semakin anomali)
        scores = model.decision_scores_
        
        # Threshold Dinamis: Nilai yang berada di luar mean + 2.5 * std deviasi skor anomali
        dynamic_threshold = scores.mean() + (2.5 * scores.std())
        
        # Penentuan outlier secara dinamis
        is_outlier = scores > dynamic_threshold
        df_valid[f'outlier_{name}'] = is_outlier.astype(int)
        
        outliers_m = df_valid[df_valid[f'outlier_{name}'] == 1]
        persen = (len(outliers_m) / len(df_valid)) * 100
        
        summary_dynamic.append({
            "Polutan": pol,
            "Metode": name,
            "Total Data": len(df_valid),
            "Jumlah Outlier": len(outliers_m),
            "Persentase": f"{persen:.2f}%",
            "Threshold Skor": f"{dynamic_threshold:.4f}"
        })
        
        print(f">>> Metode: {name:<18} | Jumlah Outlier: {len(outliers_m)} hari ({persen:.2f}%)")
        if len(outliers_m) > 0:
            for idx, row in outliers_m.iterrows():
                dt = row['date']
                score_val = scores[df_valid.index.get_loc(idx)]
                print(f"    • {dt.day:>2} {BULAN_MAP[dt.month]:<9} {dt.year} | Nilai: {row[pol]:.6g} (Skor Anomali: {score_val:.3f})")
        else:
            print("    (Tidak ditemukan data anomali ekstrem)")
        print()
```

```
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

from pyod.models.knn import KNN
from pyod.models.iforest import IForest
from pyod.models.ecod import ECOD

pollutants = ['CH4', 'CO', 'NO2', 'SO2']
contamination_rate = 0.05

# Visualisasi Subplot 3 Metode Outlier untuk Setiap Polutan
for pol in pollutants:
    # 1. Cek lokasi file
    file_path = f"{pol}_lamongan_missing.csv" if os.path.exists(f"{pol}_lamongan_missing.csv") else f"data/{pol}_lamongan_missing.csv"
    
    df_p = pd.read_csv(file_path)
    df_p['date'] = pd.to_datetime(df_p['date'])
    df_valid_p = df_p.dropna(subset=[pol]).copy()
    
    # 2. Standarisasi data
    scaler = StandardScaler()
    X_p = scaler.fit_transform(df_valid_p[[pol]].values)
    
    # 3. Inisialisasi 3 Model yang Dipilih
    models_p = {
        'KNN': KNN(contamination=contamination_rate, n_neighbors=5),
        'Isolation Forest': IForest(contamination=contamination_rate, random_state=42),
        'ECOD': ECOD(contamination=contamination_rate)
    }
    
    # 4. Buat Subplot 3 baris
    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True, dpi=120)
    
    for i, (name, model) in enumerate(models_p.items()):
        model.fit(X_p)
        labels = model.labels_
        normal_m = df_valid_p[labels == 0]
        outliers_m = df_valid_p[labels == 1]
        
        ax = axes[i]
        # Garis data
        ax.plot(df_valid_p['date'], df_valid_p[pol], color='#bdc3c7', linewidth=0.8, alpha=0.6, zorder=1)
        # Titik normal (biru)
        ax.scatter(normal_m['date'], normal_m[pol], color='#2980b9', s=18, alpha=0.7, label='Normal', zorder=2)
        # Titik outlier (merah)
        ax.scatter(outliers_m['date'], outliers_m[pol], color='#e74c3c', s=40, edgecolors='black', linewidths=0.6, 
                   label=f'Outlier ({len(outliers_m)})', zorder=3)
        
        ax.set_title(f'Deteksi Outlier {pol} — Metode: {name}', fontsize=9, fontweight='bold')
        ax.set_ylabel(pol, fontsize=8)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, linestyle=':', alpha=0.5)
        
    plt.xlabel('Tanggal', fontsize=9)
    plt.suptitle(f'Grafik Deteksi Outlier (KNN, Isolation Forest, ECOD) — Polutan {pol}', fontsize=12, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.show()
```


### Penanganan Outlier dan Interpolasi Data

Setelah mendeteksi keberadaan outlier, langkah selanjutnya adalah menandainya sebagai nilai kosong (NaN). Kemudian, metode interpolasi linier diterapkan pada keseluruhan dataset untuk mengisi nilai kosong (NaN) tersebut. Di akhir proses, teknik backward fill serta forward fill dimanfaatkan guna mengatasi nilai kosong pada bagian awalan atau akhiran rangkaian data yang tidak bisa diinterpolasi linier.

```
import pandas as pd

df = pd.read_csv("CO_lamongan_sorted.csv")
df["CO"] = pd.to_numeric(df["CO"], errors="coerce")

# DETEKSI OUTLIER DENGAN IQR
Q1 = df["CO"].quantile(0.25)
Q3 = df["CO"].quantile(0.75)

IQR = Q3 - Q1

batas_bawah = Q1 - 1.5 * IQR
batas_atas = Q3 + 1.5 * IQR

# Menentukan data outlier
outlier = (
    (df["CO"] < batas_bawah) |
    (df["CO"] > batas_atas)
)

# Outlier diubah menjadi NaN
df.loc[outlier, "CO"] = None

# Mengisi nilai outlier dengan Linear Interpolation
df["CO"] = df["CO"].interpolate(method="linear")

# Menangani NaN jika berada di awal atau akhir data
df["CO"] = df["CO"].ffill().bfill()

df.to_csv("CO_lamongan_fix.csv", index=False)

print("\nFile berhasil disimpan sebagai:")
print("CO_lamongan_fix.csv")
```

```
plt.figure(figsize=(15, 6))
plt.plot(
    df["date"],
    df["CO"],
    linewidth=1,
    label="CO setelah penanganan outlier"
)

plt.title("Data CO Setelah Penanganan Outlier")
plt.xlabel("Bulan")
plt.ylabel("CO")

# Menampilkan nama bulan pada sumbu X
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%B"))

plt.xticks(rotation=45)

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

```{image} ../img/grafik_co.png
:alt: Grafik Data
:width: 100%
:align: center
```

## Ekstraksi Titur Time Series

Setelah data deret waktu polutan udara melalui tahap data cleaning, sehingga data yang digunakan sudah memiliki format yang sesuai, tidak terdapat nilai yang hilang, serta telah dilakukan penanganan terhadap outlier, tahap berikutnya adalah ekstraksi fitur time series. Tahap ini dilakukan untuk mengubah data deret waktu yang masih berupa rangkaian nilai pengamatan menjadi sekumpulan fitur numerik yang dapat menggambarkan karakteristik dan pola dari data tersebut.

Ekstraksi fitur diperlukan karena data deret waktu tidak hanya memiliki informasi berupa nilai polutan pada setiap waktu, tetapi juga memiliki karakteristik tertentu yang dapat digunakan untuk memahami pola datanya. Karakteristik tersebut dapat berupa nilai rata-rata, tingkat penyebaran data, perubahan nilai, hubungan antarwaktu, energi sinyal, maupun pola frekuensi. Dengan mengekstraksi karakteristik tersebut, informasi yang terdapat pada deret waktu dapat direpresentasikan dalam bentuk fitur yang lebih terstruktur dan dapat digunakan pada tahap analisis selanjutnya.

Dalam penelitian ini, proses ekstraksi fitur dilakukan menggunakan pustaka Python tsfel (Time Series Feature Extraction Library). TSFEL merupakan library yang menyediakan berbagai fungsi untuk menghitung fitur dari data deret waktu secara otomatis. Penggunaan TSFEL membantu mempercepat proses perhitungan serta menghasilkan fitur dengan metode yang lebih terstruktur dan konsisten.

Fitur yang diekstraksi dapat dikelompokkan ke dalam beberapa kategori utama, yaitu fitur statistik, temporal, dan spektral. Fitur statistik digunakan untuk menggambarkan karakteristik nilai pada data, seperti mean, median, standar deviasi, variansi, minimum, maksimum, skewness, kurtosis, dan RMS (Root Mean Square). Fitur temporal digunakan untuk melihat karakteristik perubahan sinyal dari waktu ke waktu, seperti autocorrelation, slope, mean difference, median difference, serta turning points. Sementara itu, fitur spektral digunakan untuk menganalisis karakteristik data berdasarkan domain frekuensi, seperti spectral centroid, spectral entropy, spectral spread, spectral skewness, spectral slope, dan spectral roll-off.

Pada proses ekstraksi, data konsentrasi polutan yang telah dibersihkan digunakan sebagai sinyal time series. Data tersebut kemudian diberikan kepada fungsi-fungsi fitur yang tersedia pada TSFEL. Setiap fungsi menghasilkan satu nilai yang merepresentasikan karakteristik tertentu dari keseluruhan sinyal. Seluruh hasil tersebut kemudian dikumpulkan menjadi sebuah tabel fitur, sehingga setiap kolom menunjukkan satu jenis fitur yang berhasil diekstraksi.

Hasil ekstraksi fitur kemudian disimpan dalam bentuk CSV sehingga dapat digunakan kembali untuk proses analisis dan pemodelan. Dengan demikian, data deret waktu polutan yang sebelumnya terdiri dari banyak pengamatan harian dapat direpresentasikan melalui sejumlah fitur numerik yang merangkum karakteristik penting dari data tersebut. Fitur-fitur tersebut selanjutnya dapat digunakan sebagai parameter input dalam proses machine learning maupun deep learning, atau sebagai dasar untuk melakukan analisis lebih lanjut terhadap pola dan karakteristik polutan udara. Dan disini kita akan ekstraksi fitur TSFEL sebanyak 68 fitur pada polutan CO:

```
import pandas as pd
import numpy as np
import inspect
import tsfel.feature_extraction.features as tsfel_features

# Memuuat data
df = pd.read_csv('CO_lamongan_fix.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)
target_pollutant = 'CO'

# Pastikan data tipe numerik.
df[target_pollutant] = pd.to_numeric(df[target_pollutant], errors='coerce')

df_clean = df.set_index('date').interpolate(method='time').ffill().bfill()
fs = 1
signal_1d = df_clean[target_pollutant].astype(float).values

# Iniliasiasi 68 Daftar Fitur TSFEL
FEATURE_LIST = """abs_energy auc autocorr average_power calc_centroid calc_max calc_mean
calc_median calc_min calc_std calc_var dfa distance ecdf ecdf_percentile ecdf_percentile_count
ecdf_slope entropy fundamental_frequency higuchi_fractal_dimension hist_mode human_range_energy
hurst_exponent interq_range kurtosis lempel_ziv lpcc max_frequency max_power_spectrum
maximum_fractal_length mean_abs_deviation mean_abs_diff mean_diff median_abs_deviation
median_abs_diff median_diff median_frequency mfcc mse negative_turning neighbourhood_peaks
petrosian_fractal_dimension pk_pk_distance positive_turning power_bandwidth rms skewness slope
spectral_centroid spectral_decrease spectral_distance spectral_entropy spectral_kurtosis
spectral_positive_turning spectral_roll_off spectral_roll_on spectral_skewness spectral_slope
spectral_spread spectral_variation spectrogram_mean_coeff sum_abs_diff wavelet_abs_mean
wavelet_energy wavelet_entropy wavelet_std wavelet_var zero_cross""".split()

print("Jumlah fitur yang diminta:", len(FEATURE_LIST))

# Fungsi bantuan merubah output multivariat TSFEL menjadi float tunggal/skalar
def to_scalar(result):
    if isinstance(result, dict) and "values" in result:
        result = result["values"]
    if isinstance(result, (list, tuple, np.ndarray)):
        arr = np.asarray(result, dtype=float)
        return float(np.nanmean(arr))
    return float(result)

# Pemanggilan fungsi TSFEL
def extract_one(fn_name, signal, fs):
    fn = getattr(tsfel_features, fn_name)
    params = inspect.signature(fn).parameters
    if "fs" in params:
        result = fn(signal, fs)
    else:
        result = fn(signal)
    return to_scalar(result)

# Ekstraksi Fitur
row = {}
for fn_name in FEATURE_LIST:
    row[fn_name] = extract_one(fn_name, signal_1d, fs)

extracted_features_final = pd.DataFrame([row])

print(f"Berhasil! Jumlah fitur yang diekstrak pada {target_pollutant}: {extracted_features_final.shape[1]}")

# Export hasil ke folder data
extracted_features_final.to_csv(f'data/polutan/{target_pollutant}_Lamongan_TSFEL.csv', index=False)
```

```{image} ../img/TSEFL.png
:alt: Grafik Data
:width: 100%
:align: center
```

# Penjelasan Domain Fitur TSFEL

TSFEL (_Time Series Feature Extraction Library_) menyediakan berbagai fitur yang dapat digunakan untuk menggambarkan karakteristik suatu data deret waktu. Fitur-fitur tersebut dapat dikelompokkan berdasarkan sudut pandang analisisnya, yaitu **Statistical**, **Temporal**, dan **Spectral**.

Pembagian ini memungkinkan data deret waktu polutan dianalisis secara lebih menyeluruh. Domain statistik berfokus pada karakteristik nilai dan distribusi data, domain temporal melihat pola perubahan berdasarkan urutan waktu, sedangkan domain spektral mempelajari pola berdasarkan komponen frekuensinya.

## 1. Domain Statistical

Domain **Statistical** digunakan untuk memperoleh informasi mengenai karakteristik numerik dari kumpulan nilai dalam deret waktu. Analisis pada domain ini dapat memberikan gambaran mengenai pusat data, tingkat penyebaran, bentuk distribusi, serta besarnya variasi nilai polutan.

Beberapa fitur statistik yang digunakan antara lain:

- **`calc_max`**: Menghasilkan nilai paling tinggi yang terdapat pada sinyal polutan.
- **`calc_min`**: Menentukan nilai terendah dari keseluruhan data.
- **`calc_mean`**: Menghitung nilai rata-rata dari data polutan.
- **`calc_median`**: Menentukan nilai tengah setelah data diurutkan.
- **`calc_std`**: Mengukur seberapa jauh nilai data tersebar dari nilai rata-ratanya melalui standar deviasi.
- **`calc_var`**: Menunjukkan tingkat variasi data berdasarkan nilai varians.
- **`ecdf`**: Menggambarkan distribusi kumulatif empiris dari nilai-nilai pada deret waktu.
- **`ecdf_percentile`**: Menghasilkan informasi persentil berdasarkan distribusi kumulatif empiris.
- **`ecdf_percentile_count`**: Menghitung jumlah data yang berkaitan dengan posisi persentil tertentu pada ECDF.
- **`ecdf_slope`**: Menggambarkan perubahan atau kemiringan distribusi pada ECDF.
- **`hist_mode`**: Menentukan nilai yang paling sering muncul berdasarkan distribusi histogram.
- **`interq_range`**: Mengukur rentang 50% bagian tengah data menggunakan selisih antara kuartil ketiga dan kuartil pertama.
- **`kurtosis`**: Menggambarkan karakteristik bentuk distribusi, khususnya tingkat keruncingan atau ketebalan ekornya.
- **`skewness`**: Menunjukkan tingkat kemiringan distribusi data terhadap nilai pusatnya.
- **`mean_abs_deviation`**: Menghitung rata-rata jarak absolut setiap nilai terhadap nilai pusat.
- **`median_abs_deviation`**: Mengukur penyebaran data berdasarkan median sehingga relatif lebih tahan terhadap nilai ekstrem.
- **`rms`**: Menghitung _Root Mean Square_, yaitu ukuran besarnya nilai sinyal berdasarkan akar dari rata-rata kuadrat seluruh nilai.

Fitur pada domain statistik dapat digunakan untuk mengetahui bagaimana karakteristik umum dan penyebaran data polutan selama periode pengamatan.

## 2. Domain Temporal

Domain **Temporal** mempertimbangkan susunan nilai berdasarkan waktu. Berbeda dengan statistik yang lebih menitikberatkan pada distribusi nilai, fitur temporal digunakan untuk melihat bagaimana sinyal mengalami perubahan dari satu pengamatan ke pengamatan berikutnya.

Fitur yang termasuk dalam domain ini meliputi:

- **`abs_energy`**: Menghitung akumulasi kuadrat nilai sinyal sehingga dapat digunakan untuk menggambarkan besarnya energi keseluruhan sinyal.
- **`auc`**: Menghitung luas area yang terbentuk di bawah kurva deret waktu.
- **`autocorr`**: Mengukur hubungan antara nilai pada suatu waktu dengan nilai pada waktu sebelumnya.
- **`average_power`**: Menentukan besarnya daya rata-rata yang terdapat pada sinyal.
- **`calc_centroid`**: Menentukan posisi pusat massa atau titik keseimbangan sinyal pada dimensi waktunya.
- **`dfa`**: Menggunakan pendekatan _Detrended Fluctuation Analysis_ untuk mempelajari pola korelasi atau ketergantungan jangka panjang dalam deret waktu.
- **`distance`**: Mengukur panjang lintasan yang terbentuk dari perubahan posisi antar titik data secara berurutan.
- **`entropy`**: Menggambarkan tingkat ketidakpastian atau ketidakteraturan yang terdapat pada sinyal.
- **`higuchi_fractal_dimension`**: Mengestimasi dimensi fraktal menggunakan metode Higuchi untuk menggambarkan kompleksitas sinyal.
- **`petrosian_fractal_dimension`**: Mengukur kompleksitas sinyal berdasarkan perubahan atau jumlah variasi pada deret waktu menggunakan pendekatan Petrosian.
- **`hurst_exponent`**: Memberikan informasi mengenai karakteristik memori jangka panjang pada data dan kecenderungan suatu pola untuk berlanjut.
- **`lempel_ziv`**: Menggambarkan kompleksitas pola dalam sinyal berdasarkan struktur dan kemunculan pola yang dapat ditemukan.
- **`maximum_fractal_length`**: Mengukur panjang fraktal maksimum yang diperoleh dari analisis sinyal pada skala tertentu.
- **`mean_abs_diff`**: Menghitung rata-rata nilai absolut dari perubahan antar pengamatan yang berurutan.
- **`mean_diff`**: Menentukan rata-rata perubahan nilai antara satu titik waktu dengan titik waktu berikutnya.
- **`median_abs_diff`**: Menghasilkan median dari nilai perubahan absolut antar data yang berurutan.
- **`median_diff`**: Menghitung median perubahan nilai pada titik-titik waktu yang berdekatan.
- **`mse`**: Menghitung _Mean Squared Error_, yaitu rata-rata kuadrat kesalahan antara nilai sinyal dengan nilai pembanding atau estimasinya.
- **`negative_turning`**: Mengidentifikasi perubahan arah sinyal yang menunjukkan pergerakan dari kondisi meningkat menuju menurun.
- **`positive_turning`**: Mengidentifikasi perubahan arah sinyal dari kondisi menurun menuju meningkat.
- **`neighbourhood_peaks`**: Mendeteksi keberadaan titik puncak dengan mempertimbangkan nilai-nilai di sekitar titik tersebut.
- **`pk_pk_distance`**: Mengukur selisih antara nilai puncak tertinggi dan lembah terendah pada sinyal.
- **`slope`**: Menunjukkan kecenderungan arah perubahan sinyal secara keseluruhan melalui kemiringan garis regresi.
- **`sum_abs_diff`**: Menjumlahkan seluruh perubahan absolut yang terjadi antar titik data secara berurutan.
- **`zero_cross`**: Menghitung jumlah kejadian ketika sinyal melewati atau memotong nilai nol sebagai titik referensi.

Fitur temporal sangat berguna dalam penelitian polutan karena nilai suatu polutan tidak hanya penting dari sisi besarannya, tetapi juga bagaimana nilai tersebut berubah dari hari ke hari.

## 3. Domain Spectral

Domain **Spectral** menganalisis sinyal berdasarkan komponen frekuensi yang terkandung di dalamnya. Pendekatan ini berguna untuk menemukan pola berulang, dominasi frekuensi tertentu, distribusi energi, serta karakteristik perubahan sinyal yang tidak selalu terlihat apabila hanya diamati berdasarkan nilai waktunya.

Fitur-fitur yang digunakan dalam domain ini antara lain:

- **`fundamental_frequency`**: Menentukan frekuensi dasar yang menjadi komponen utama dalam sinyal.
- **`max_frequency`**: Menunjukkan frekuensi tertinggi yang teridentifikasi dalam hasil analisis spektrum.
- **`median_frequency`**: Menentukan titik frekuensi yang membagi distribusi energi spektrum menjadi dua bagian yang relatif seimbang.
- **`human_range_energy`**: Mengukur energi sinyal pada rentang frekuensi tertentu yang didefinisikan dalam TSFEL.
- **`lpcc`**: Menghasilkan _Linear Prediction Cepstral Coefficients_, yaitu representasi karakteristik spektral yang berasal dari pendekatan prediksi linear.
- **`mfcc`**: Menghasilkan _Mel-Frequency Cepstral Coefficients_ untuk merepresentasikan karakteristik spektrum menggunakan skala Mel.
- **`max_power_spectrum`**: Menentukan nilai daya terbesar yang muncul pada spektrum frekuensi.
- **`power_bandwidth`**: Menggambarkan lebar rentang frekuensi yang mengandung sebagian besar energi sinyal.
- **`spectral_centroid`**: Menentukan titik pusat distribusi energi pada spektrum frekuensi.
- **`spectral_decrease`**: Mengukur kecenderungan penurunan magnitudo spektrum ketika frekuensi meningkat.
- **`spectral_distance`**: Mengukur perbedaan antara karakteristik spektrum pada bagian-bagian yang dianalisis.
- **`spectral_entropy`**: Menilai tingkat penyebaran atau ketidakaturan distribusi energi pada spektrum.
- **`spectral_kurtosis`**: Menggambarkan bentuk distribusi spektrum berdasarkan karakteristik keruncingannya.
- **`spectral_positive_turning`**: Mengidentifikasi perubahan arah positif pada karakteristik spektral.
- **`spectral_roll_off`**: Menentukan frekuensi batas ketika sebagian besar energi spektrum telah tercapai.
- **`spectral_roll_on`**: Menentukan posisi awal frekuensi ketika energi spektrum mulai mencapai bagian tertentu dari total energinya.
- **`spectral_skewness`**: Menggambarkan tingkat kemiringan distribusi energi pada spektrum frekuensi.
- **`spectral_slope`**: Mengukur kecenderungan naik atau turunnya magnitudo spektrum terhadap perubahan frekuensi.
- **`spectral_spread`**: Menunjukkan tingkat penyebaran energi frekuensi terhadap posisi _spectral centroid_.
- **`spectral_variation`**: Menggambarkan perubahan karakteristik spektrum dari satu bagian analisis ke bagian lainnya.
- **`spectrogram_mean_coeff`**: Menghasilkan nilai rata-rata koefisien yang diperoleh dari representasi spektrogram.
- **`wavelet_abs_mean`**: Menghitung rata-rata nilai absolut dari koefisien yang diperoleh melalui analisis wavelet.
- **`wavelet_energy`**: Mengukur energi yang terdapat pada koefisien wavelet.
- **`wavelet_entropy`**: Menggambarkan tingkat ketidakaturan distribusi energi pada koefisien wavelet.
- **`wavelet_std`**: Menghitung standar deviasi dari koefisien wavelet.
- **`wavelet_var`**: Menghitung varians dari koefisien wavelet.

Analisis spektral dapat membantu mengidentifikasi pola periodik pada data polutan. Informasi tersebut dapat melengkapi hasil analisis statistik dan temporal sehingga karakteristik deret waktu dapat dipahami dari beberapa sisi.

### Rumus dan Perhitungan Beberapa Fitur TSFEL

Untuk memahami proses ekstraksi fitur menggunakan TSFEL, beberapa fitur dapat dihitung secara manual menggunakan data deret waktu sederhana. Perhitungan manual ini digunakan untuk menunjukkan bagaimana nilai fitur diperoleh dari sekumpulan data polutan.

Sebagai contoh, digunakan lima data pengamatan konsentrasi polutan sebagai berikut:

| Hari | Nilai Polutan |
| ---- | ------------: |
| 1    |             2 |
| 2    |             4 |
| 3    |             5 |
| 4    |             7 |
| 5    |             8 |

Sehingga diperoleh data:

$$
X = [2,4,5,7,8]
$$

Jumlah data:

$$
n = 5
$$

## 1. Mean (`calc_mean`)

### Pengertian

Mean atau rata-rata digunakan untuk mengetahui nilai pusat dari seluruh data pengamatan.

### Rumus

$$
\bar{x} = \frac{\sum_{i=1}^{n}x_i}{n}
$$

Keterangan:

- $\bar{x}$ = nilai rata-rata
- $x_i$ = nilai pengamatan ke-$i$
- $n$ = jumlah data

### Perhitungan

Data yang digunakan:

$$
2,4,5,7,8
$$

Jumlah seluruh data:

$$
2+4+5+7+8=26
$$

Jumlah data:

$$
n=5
$$

Maka:

$$
\bar{x}=\frac{26}{5}
$$

$$
\bar{x}=5.2
$$

### Hasil

Nilai **mean = 5,2**.

Artinya, rata-rata konsentrasi polutan pada lima pengamatan tersebut adalah **5,2**.

## 2. Median (`calc_median`)

### Pengertian

Median merupakan nilai yang berada di posisi tengah setelah seluruh data disusun dari nilai terkecil hingga terbesar.

### Rumus

Jika jumlah data ganjil:

$$
Median = x_{\frac{n+1}{2}}
$$

### Perhitungan

Data sudah disusun dari terkecil hingga terbesar:

$$
2,4,5,7,8
$$

Jumlah data:

$$
n=5
$$

Posisi median:

$$
\frac{5+1}{2}=3
$$

Maka nilai pada posisi ke-3 adalah:

$$
Median=5
$$

### Hasil

Nilai **median = 5**.

Median menunjukkan nilai tengah dari kumpulan data setelah data diurutkan.

## 3. Varians (`calc_var`)

### Pengertian

Varians digunakan untuk mengetahui seberapa besar penyebaran nilai data terhadap rata-ratanya.

Untuk perhitungan populasi, rumus varians adalah:

$$
\sigma^2 = \frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n}
$$

Keterangan:

- $\sigma^2$ = varians
- $x_i$ = nilai pengamatan
- $\bar{x}$ = rata-rata
- $n$ = jumlah data

### Perhitungan

Diketahui:

$$
\bar{x}=5.2
$$

Selanjutnya hitung selisih setiap nilai dengan rata-rata.

| Nilai ($x_i$) | $x_i-\bar{x}$ | $(x_i-\bar{x})^2$ |
| ------------: | ------------: | ----------------: |
|             2 |          -3,2 |             10,24 |
|             4 |          -1,2 |              1,44 |
|             5 |          -0,2 |              0,04 |
|             7 |           1,8 |              3,24 |
|             8 |           2,8 |              7,84 |

Jumlah kuadrat selisih:

$$
10.24+1.44+0.04+3.24+7.84=22.80
$$

Maka:

$$
\sigma^2=\frac{22.80}{5}
$$

$$
\sigma^2=4.56
$$

### Hasil

Nilai **varians = 4,56**.

Semakin besar nilai varians, semakin besar pula penyebaran data terhadap rata-ratanya.

> **Catatan:** Jika menggunakan varians sampel, penyebutnya adalah $n-1$, bukan $n$. Oleh karena itu hasilnya akan berbeda.

## 4. Standar Deviasi (`calc_std`)

### Pengertian

Standar deviasi merupakan akar kuadrat dari varians. Fitur ini menunjukkan tingkat penyebaran data dalam satuan yang sama dengan data aslinya.

### Rumus

$$
\sigma = \sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n}}
$$

Karena sebelumnya telah diperoleh:

$$
\sigma^2=4.56
$$

Maka:

$$
\sigma=\sqrt{4.56}
$$

$$
\sigma\approx2.14
$$

### Hasil

Nilai **standar deviasi ≈ 2,14**.

Artinya, nilai pengamatan memiliki penyebaran sekitar **2,14 satuan** dari nilai rata-ratanya.

## 5. Root Mean Square (`rms`)

### Pengertian

RMS (_Root Mean Square_) digunakan untuk mengetahui besarnya nilai sinyal dengan menghitung akar dari rata-rata kuadrat seluruh nilai.

Fitur ini berbeda dengan mean karena setiap nilai terlebih dahulu dikuadratkan.

### Rumus

$$
RMS=\sqrt{\frac{\sum_{i=1}^{n}x_i^2}{n}}
$$

### Perhitungan

Data:

$$
2,4,5,7,8
$$

Kuadrat setiap nilai:

$$
2^2=4
$$

$$
4^2=16
$$

$$
5^2=25
$$

$$
7^2=49
$$

$$
8^2=64
$$

Jumlah kuadrat:

$$
4+16+25+49+64=158
$$

Kemudian:

$$
RMS=\sqrt{\frac{158}{5}}
$$

$$
RMS=\sqrt{31.6}
$$

$$
RMS\approx5.62
$$

### Hasil

Nilai **RMS ≈ 5,62**.

RMS memberikan gambaran mengenai besarnya sinyal berdasarkan keseluruhan nilai pengamatan.

## 6. Interquartile Range (`interq_range`)

### Pengertian

IQR (_Interquartile Range_) digunakan untuk mengukur rentang dari 50% data yang berada di bagian tengah distribusi.

IQR juga sering digunakan dalam proses **identifikasi outlier**.

### Rumus

$$
IQR=Q_3-Q_1
$$

Keterangan:

- $Q_1$ = kuartil pertama
- $Q_3$ = kuartil ketiga

### Perhitungan

Data:

$$
2,4,5,7,8
$$

Dengan metode kuartil yang umum digunakan pada perhitungan statistik:

$$
Q_1=4
$$

dan

$$
Q_3=7
$$

Sehingga:

$$
IQR=7-4
$$

$$
IQR=3
$$

### Hasil

Nilai **IQR = 3**.

Nilai tersebut menunjukkan rentang penyebaran 50% data yang berada di bagian tengah.

IQR juga dapat digunakan untuk menentukan batas outlier:

$$
Batas\ Bawah=Q_1-1.5(IQR)
$$

$$
Batas\ Atas=Q_3+1.5(IQR)
$$

Dengan data di atas:

$$
Batas\ Bawah=4-1.5(3)
$$

$$
Batas\ Bawah=-0.5
$$

Sedangkan:

$$
Batas\ Atas=7+1.5(3)
$$

$$
Batas\ Atas=11.5
$$

Jadi, nilai yang berada di bawah **-0,5** atau di atas **11,5** dapat dikategorikan sebagai outlier berdasarkan metode IQR.

# Evaluasi Perbandingan Clustering K-Means dan Deteksi Outlier

Setelah diperoleh 272 fitur hasil ekstraksi TSFEL dari 19 sampel yang berasal dari masing-masing daerah atau mahasiswa, tahap selanjutnya adalah melakukan proses pengelompokan data menggunakan algoritma **K-Means**. Evaluasi clustering dilakukan dengan membandingkan dua skenario jumlah cluster, yaitu pengelompokan menjadi **2 cluster** dan pengelompokan menjadi **3 cluster**. Proses clustering dilakukan menggunakan dua pendekatan, yaitu data yang telah direduksi dimensinya menggunakan **PCA** dengan 19 komponen utama (PCA 0 hingga PCA 18) serta data yang tetap menggunakan keseluruhan fitur tanpa reduksi PCA. Perbandingan kedua pendekatan tersebut digunakan untuk melihat perbedaan hasil pengelompokan berdasarkan fitur yang telah direduksi dan fitur TSFEL secara keseluruhan.

## Visualisasi Workflow KNIME & Scatter Plot Analytics Platform

Proses ekstraksi, praprocessing, reduksi dimensi PCA, dan pengelompokan K-Means dijalankan menggunakan alur kerja (workflow) KNIME Analytics Platform:
 
```{image} ../img/clustering.png
:alt: Grafik Data
:width: 100%
:align: center
```
Hasil proses clustering yang diperoleh melalui alur KNIME kemudian divisualisasikan menggunakan **Scatter Plot**. Grafik tersebut digunakan untuk memperlihatkan posisi dan persebaran 19 sampel mahasiswa/daerah berdasarkan cluster yang terbentuk. Setiap titik pada grafik merepresentasikan satu sampel, sedangkan label atau warna yang berbeda menunjukkan kelompok (*cluster*) tempat sampel tersebut berada. Visualisasi ini membantu melihat pola pemisahan dan kedekatan antaranggota cluster secara lebih jelas.

```{image} ../img/k2 pca.png
:alt: Grafik Data
:width: 100%
:align: center
```
Berdasarkan hasil clustering menggunakan K-Means dengan reduksi dimensi PCA, data 19 mahasiswa/daerah terbagi menjadi dua kelompok. Sebanyak 18 sampel berada pada cluster_0, sedangkan 1 sampel, yaitu asal Burneh Bangkalan, berada pada cluster_1. Pemisahan satu sampel tersebut menunjukkan bahwa karakteristik fitur yang dimilikinya memiliki perbedaan yang cukup jauh dibandingkan dengan sampel lainnya sehingga membentuk kelompok tersendiri pada hasil clustering.

```{image} ../img/k2 no pca.png
:alt: Grafik Data
:width: 100%
:align: center
```

Pada pengelompokan menggunakan **K-Means dengan seluruh 272 fitur TSFEL yang telah dinormalisasi tanpa melalui reduksi PCA**, diperoleh pembagian cluster yang sama dengan skenario sebelumnya. Sebanyak **18 daerah** masuk ke dalam **`cluster_0`**, sementara **Burneh, Bangkalan** berada sendiri pada **`cluster_1`**. Hasil ini menunjukkan bahwa daerah tersebut tetap memiliki pola karakteristik yang berbeda dibandingkan 18 daerah lainnya, meskipun proses clustering dilakukan menggunakan seluruh fitur TSFEL tanpa reduksi dimensi.

```{image} ../img/k5 pca.png
:alt: Grafik Data
:width: 100%
:align: center
```

Pada skenario dengan jumlah cluster yang lebih banyak dan menggunakan reduksi dimensi **PCA**, hasil pengelompokan menjadi lebih terperinci. Dari 19 mahasiswa/daerah yang dianalisis, terbentuk **5 kelompok** dengan karakteristik yang berbeda. Sebagian besar sampel, yaitu **14 daerah**, terkumpul pada **`cluster_2`**. Sementara itu, empat daerah lainnya membentuk cluster secara terpisah, yaitu **Kraton, Bangkalan** pada **`cluster_4`**, **Kadur, Pamekasan** pada **`cluster_0`**, **Burneh, Bangkalan** pada **`cluster_1`**, serta **Sokobanah** pada **`cluster_3`**. Hasil tersebut menunjukkan bahwa peningkatan jumlah cluster menghasilkan pembagian kelompok yang lebih spesifik dibandingkan skenario dengan jumlah cluster yang lebih sedikit.

```{image} ../img/k5 no pca.png
:alt: Grafik Data
:width: 100%
:align: center
```
Pada skenario clustering menggunakan **272 fitur TSFEL secara keseluruhan tanpa menerapkan reduksi dimensi PCA**, diperoleh pola pengelompokan yang relatif sama dengan hasil pada skenario menggunakan PCA. Dari 19 daerah, sebagian besar data tergabung dalam **satu cluster utama**, sedangkan empat daerah lainnya masing-masing membentuk **cluster tersendiri**. Dengan demikian, penggunaan seluruh fitur TSFEL tetap menghasilkan pemisahan terhadap beberapa daerah yang memiliki karakteristik berbeda dari kelompok utama.


