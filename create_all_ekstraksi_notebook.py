import os
import nbformat as nbf
# pyrefly: ignore [missing-import]
from nbconvert.preprocessors import ExecutePreprocessor

cells = []

# --- 1. JUDUL & PENGANTAR ---
m1 = """# Preprocessing dan Ekstraksi Fitur Polutan Udara (CO, CH4, NO2, SO2)

Halaman ini mendokumentasikan seluruh tahapan pemrosesan data deret waktu (*time series*) untuk empat polutan utama di Kabupaten Lamongan:
1. **Karbon Monoksida (CO)**
2. **Metana (CH4)**
3. **Nitrogen Dioksida (NO2)**
4. **Sulfur Dioksida (SO2)**

Tahapan pengolahan data meliputi:
- **Deteksi & Imputasi Missing Value** menggunakan metode *Linear Interpolation*.
- **Deteksi Outlier** menggunakan metode *Interquartile Range (IQR)* beserta visualisasinya.
- **Penanganan Outlier & Pembersihan Data**.
- **Ekstraksi Fitur Time Series (68 Fitur TSFEL)** yang mencakup domain *Statistical*, *Temporal*, dan *Spectral*."""

cells.append(nbf.v4.new_markdown_cell(m1))

# --- 2. TAHAP 1: MISSING VALUE ---
m2 = """---

## 1. Preprocessing: Deteksi & Imputasi Missing Value (Interpolasi Linear)

*Missing value* adalah kondisi saat terdapat data yang tidak terekam pada periode observasi tertentu akibat kendala tutupan awan atau gangguan sensor satelit Sentinel-5P. 

Metode **Interpolasi Linear** memperkirakan nilai yang hilang berdasarkan tren linier antara titik data sebelum dan sesudahnya:
$$y = y_1 + \\frac{(x - x_1)(y_2 - y_1)}{x_2 - x_1}$$

Untuk nilai kosong di bagian awal atau akhir data deret waktu yang tidak memiliki titik batas, diterapkan teknik **Forward Fill (`ffill`)** dan **Backward Fill (`bfill`)**."""

cells.append(nbf.v4.new_markdown_cell(m2))

# Code Cell 1: Missing Value Imputation
c1 = """import pandas as pd
import numpy as np

# Daftar polutan dan lokasi dataset
pollutants = {
    "CO": "data/CO_lamongan.csv",
    "CH4": "data/CH4_lamongan.csv",
    "NO2": "data/No2_lamongan.csv",
    "SO2": "data/SO2_lamongan.csv"
}

missing_summary = []
dfs_imputed = {}

for polutan, path in pollutants.items():
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'], format='mixed')
    df = df.sort_values('date').reset_index(drop=True)
    df[polutan] = pd.to_numeric(df[polutan], errors='coerce')
    
    total_data = len(df)
    missing_before = df[polutan].isnull().sum()
    pct_missing = (missing_before / total_data) * 100
    
    # Imputasi Missing Value dengan Linear Interpolation, ffill, bfill
    df_clean = df.copy()
    df_clean[polutan] = df_clean[polutan].ffill().bfill().interpolate(method='linear')
    missing_after = df_clean[polutan].isnull().sum()
    
    # Simpan dataset hasil imputasi missing
    save_path = f"data/{polutan}_lamongan_missing.csv"
    df_clean.to_csv(save_path, index=False)
    dfs_imputed[polutan] = df_clean
    
    missing_summary.append({
        "Polutan": polutan,
        "Total Data": total_data,
        "Missing Awal": missing_before,
        "Persentase Missing": f"{pct_missing:.2f}%",
        "Missing Setelah Imputasi": missing_after,
        "Status": "Bersih (0 Missing)"
    })

pd.DataFrame(missing_summary)"""

cells.append(nbf.v4.new_code_cell(c1))

# --- 3. TAHAP 2: DETEKSI OUTLIER (IQR) ---
m3 = """---

## 2. Preprocessing: Deteksi Outlier dengan Interquartile Range (IQR)

*Interquartile Range (IQR)* mengukur penyebaran 50% data bagian tengah antara Kuartil Pertama ($Q_1$) dan Kuartil Ketiga ($Q_3$):
$$\\text{IQR} = Q_3 - Q_1$$

Batas ambang deteksi data pencilan (*outlier*):
- **Batas Bawah (*Lower Bound*):**
  $$\\text{Batas Bawah} = Q_1 - 1.5 \\times \\text{IQR}$$
- **Batas Atas (*Upper Bound*):**
  $$\\text{Batas Atas} = Q_3 + 1.5 \\times \\text{IQR}$$

Data dengan nilai $x < \\text{Batas Bawah}$ atau $x > \\text{Batas Atas}$ dikategorikan sebagai **Outlier**."""

cells.append(nbf.v4.new_markdown_cell(m3))

# Code Cell 2: Deteksi Outlier IQR
c2 = """iqr_summary = []
outliers_dict = {}

for polutan, df in dfs_imputed.items():
    series = df[polutan]
    
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    
    batas_bawah = q1 - 1.5 * iqr
    batas_atas = q3 + 1.5 * iqr
    
    is_outlier = (series < batas_bawah) | (series > batas_atas)
    outlier_count = is_outlier.sum()
    outliers_dict[polutan] = df[is_outlier]
    
    iqr_summary.append({
        "Polutan": polutan,
        "Q1 (25%)": q1,
        "Q3 (75%)": q3,
        "IQR": iqr,
        "Batas Bawah": batas_bawah,
        "Batas Atas": batas_atas,
        "Jumlah Outlier": outlier_count,
        "Persentase Outlier": f"{(outlier_count / len(df)) * 100:.2f}%"
    })

pd.DataFrame(iqr_summary)"""

cells.append(nbf.v4.new_code_cell(c2))

# Code Cell 3: Plot Deteksi Outlier untuk Seluruh Polutan
c3 = """import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
axes = axes.flatten()

for idx, (polutan, df) in enumerate(dfs_imputed.items()):
    ax = axes[idx]
    
    q1 = df[polutan].quantile(0.25)
    q3 = df[polutan].quantile(0.75)
    iqr = q3 - q1
    batas_bawah = q1 - 1.5 * iqr
    batas_atas = q3 + 1.5 * iqr
    
    outliers = df[(df[polutan] < batas_bawah) | (df[polutan] > batas_atas)]
    
    # Plot garis time series
    ax.plot(df['date'], df[polutan], label=f'{polutan} Data', linewidth=1, color='#1f77b4')
    
    # Titik outlier
    if len(outliers) > 0:
        ax.scatter(outliers['date'], outliers[polutan], color='red', s=25, label=f'Outliers ({len(outliers)})', zorder=5)
    
    # Garis ambang batas IQR
    ax.axhline(batas_atas, color='orange', linestyle='--', linewidth=1.2, label='Upper Bound (IQR)')
    ax.axhline(batas_bawah, color='green', linestyle='--', linewidth=1.2, label='Lower Bound (IQR)')
    
    ax.set_title(f'Deteksi Outlier Polutan {polutan} (Metode IQR)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Bulan', fontsize=10)
    ax.set_ylabel(f'Kadar {polutan}', fontsize=10)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.tick_params(axis='x', rotation=30)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', fontsize=9)

plt.tight_layout()
plt.show()"""

cells.append(nbf.v4.new_code_cell(c3))

# --- 3b. TAHAP 2b: PERBANDINGAN DETEKSI OUTLIER METODE MACHINE LEARNING (PyOD) ---
m3_pyod = """---

## 2.1 Perbandingan Deteksi Outlier Metode Machine Learning & Probabilitas (PyOD)

Selain menerapkan pendekatan statistik konvensional seperti **Interquartile Range (IQR)** untuk mengidentifikasi data pencilan, analisis juga diperluas dengan membandingkan beberapa algoritma deteksi outlier yang tersedia dalam pustaka **PyOD**. Sebanyak **3 metode berbasis Machine Learning dan probabilitas** digunakan dalam pengujian:
- **KNN (*k-Nearest Neighbors*)**: Mengukur jarak suatu data ke k-tetangga terdekat. Jika jaraknya jauh, titik tersebut dianggap outlier.
- **Isolation Forest**: Memisahkan data secara acak menggunakan pohon biner; titik anomali lebih cepat terisolasi.
- **ECOD (*Empirical Cumulative Distribution Functions*)**: Menilai anomali berdasarkan fungsi distribusi kumulatif empiris pada ekor data."""

cells.append(nbf.v4.new_markdown_cell(m3_pyod))

c3_pyod_table = """from sklearn.preprocessing import StandardScaler
from pyod.models.knn import KNN
from pyod.models.iforest import IForest
from pyod.models.ecod import ECOD

summary_pyod = []

for polutan, df in dfs_imputed.items():
    df_valid = df.dropna(subset=[polutan]).copy()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_valid[[polutan]].values)
    
    models = {
        'KNN': KNN(contamination=0.05, n_neighbors=5),
        'Isolation Forest': IForest(contamination=0.05, random_state=42),
        'ECOD': ECOD(contamination=0.05)
    }
    
    for name, model in models.items():
        model.fit(X_scaled)
        pred = model.labels_
        outliers_count = int((pred == 1).sum())
        persen = (outliers_count / len(df_valid)) * 100
        
        summary_pyod.append({
            "Polutan": polutan,
            "Metode": name,
            "Total Data": len(df_valid),
            "Jumlah Outlier": outliers_count,
            "Persentase": f"{persen:.2f}%",
            "Threshold Skor": f"{model.threshold_:.4f}"
        })

df_summary_pyod = pd.DataFrame(summary_pyod)
print("=" * 80)
print("     TABEL PERBANDINGAN DETEKSI OUTLIER METODE MACHINE LEARNING (PyOD)")
print("=" * 80)
display(df_summary_pyod.style
    .set_properties(**{'text-align': 'center'})
    .set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#2c3e50'), ('color', 'white'), ('font-size', '12px'), ('text-align', 'center')]},
        {'selector': 'td', 'props': [('font-size', '12px')]},
        {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#f8f9fa')]}
    ])
)"""

cells.append(nbf.v4.new_code_cell(c3_pyod_table))

c3_pyod_plot = """# Visualisasi Subplot 3 Metode Outlier untuk Setiap Polutan
for polutan, df in dfs_imputed.items():
    df_valid = df.dropna(subset=[polutan]).copy()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_valid[[polutan]].values)
    
    models = {
        'KNN': KNN(contamination=0.05, n_neighbors=5),
        'Isolation Forest': IForest(contamination=0.05, random_state=42),
        'ECOD': ECOD(contamination=0.05)
    }
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 8), sharex=True, dpi=120)
    
    for i, (name, model) in enumerate(models.items()):
        model.fit(X_scaled)
        labels = model.labels_
        normal_m = df_valid[labels == 0]
        outliers_m = df_valid[labels == 1]
        
        ax = axes[i]
        ax.plot(df_valid['date'], df_valid[polutan], color='#bdc3c7', linewidth=0.8, alpha=0.6, zorder=1)
        ax.scatter(normal_m['date'], normal_m[polutan], color='#2980b9', s=16, alpha=0.7, label='Normal', zorder=2)
        ax.scatter(outliers_m['date'], outliers_m[polutan], color='#e74c3c', s=35, edgecolors='black', linewidths=0.6, 
                   label=f'Outlier ({len(outliers_m)} hari)', zorder=3)
        
        ax.set_title(f'Deteksi Outlier {polutan} — Metode: {name}', fontsize=10, fontweight='bold')
        ax.set_ylabel(polutan, fontsize=8)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, linestyle=':', alpha=0.5)
        
    plt.xlabel('Tanggal Observasi', fontsize=9)
    plt.suptitle(f'Grafik Deteksi Outlier (KNN, Isolation Forest, ECOD) — Polutan {polutan}', fontsize=12, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.show()"""

cells.append(nbf.v4.new_code_cell(c3_pyod_plot))

# --- 4. TAHAP 3: PENANGANAN OUTLIER ---
m4 = """---

## 3. Preprocessing: Penanganan Outlier & Pembersihan Data

Setelah nilai *outlier* terdeteksi, data pencilan tersebut ditandai (*set as NaN*). Selanjutnya, diterapkan kembali teknik **Linear Interpolation** serta *forward/backward fill* untuk menghasilkan deret waktu yang kontinu, halus, dan representatif."""

cells.append(nbf.v4.new_markdown_cell(m4))

# Code Cell 4: Penanganan Outlier & Simpan Data Bersih
c4 = """dfs_fixed = {}

for polutan, df in dfs_imputed.items():
    df_fixed = df.copy()
    
    q1 = df_fixed[polutan].quantile(0.25)
    q3 = df_fixed[polutan].quantile(0.75)
    iqr = q3 - q1
    batas_bawah = q1 - 1.5 * iqr
    batas_atas = q3 + 1.5 * iqr
    
    outliers = (df_fixed[polutan] < batas_bawah) | (df_fixed[polutan] > batas_atas)
    
    # Ubah outlier menjadi None/NaN
    df_fixed.loc[outliers, polutan] = None
    
    # Interpolasi linier untuk mengisi outlier
    df_fixed[polutan] = df_fixed[polutan].interpolate(method='linear').ffill().bfill()
    
    # Simpan dataset bersih
    save_path = f"data/{polutan}_lamongan_fix.csv"
    df_fixed.to_csv(save_path, index=False)
    dfs_fixed[polutan] = df_fixed
    print(f"Data bersih {polutan:4s} berhasil disimpan ke: {save_path}")"""

cells.append(nbf.v4.new_code_cell(c4))

# Code Cell 5: Plot Visualisasi Time Series Setelah Penanganan Outlier
c5 = """fig, axes = plt.subplots(2, 2, figsize=(16, 10))
axes = axes.flatten()

colors = ['#1f77b4', '#9467bd', '#2ca02c', '#d62728']

for idx, (polutan, df) in enumerate(dfs_fixed.items()):
    ax = axes[idx]
    
    ax.plot(df['date'], df[polutan], linewidth=1.2, color=colors[idx], label=f'{polutan} Bersih')
    ax.set_title(f'Data {polutan} Setelah Penanganan Outlier', fontsize=12, fontweight='bold')
    ax.set_xlabel('Bulan', fontsize=10)
    ax.set_ylabel(f'Kadar {polutan}', fontsize=10)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.tick_params(axis='x', rotation=30)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='upper right')

plt.tight_layout()
plt.show()"""

cells.append(nbf.v4.new_code_cell(c5))

# --- 5. TAHAP 4: EKSTRAKSI FITUR TSFEL ---
m5 = """---

## 4. Ekstraksi Fitur Time Series (68 Fitur TSFEL)

Setelah rangkaian data polutan bersih dari *missing value* dan *outlier*, dilakukan ekstraksi fitur numerik menggunakan library **TSFEL (*Time Series Feature Extraction Library*)**. 

Fitur yang diekstraksi sebanyak **68 fitur** yang mencakup:
- **Domain Statistical (17 Fitur):** `calc_max`, `calc_min`, `calc_mean`, `calc_median`, `calc_std`, `calc_var`, `ecdf`, `ecdf_percentile`, `ecdf_percentile_count`, `ecdf_slope`, `hist_mode`, `interq_range`, `kurtosis`, `skewness`, `mean_abs_deviation`, `median_abs_deviation`, `rms`.
- **Domain Temporal (25 Fitur):** `abs_energy`, `auc`, `autocorr`, `average_power`, `calc_centroid`, `dfa`, `distance`, `entropy`, `higuchi_fractal_dimension`, `petrosian_fractal_dimension`, `hurst_exponent`, `lempel_ziv`, `maximum_fractal_length`, `mean_abs_diff`, `mean_diff`, `median_abs_diff`, `median_diff`, `mse`, `negative_turning`, `positive_turning`, `neighbourhood_peaks`, `pk_pk_distance`, `slope`, `sum_abs_diff`, `zero_cross`.
- **Domain Spectral (26 Fitur):** `fundamental_frequency`, `max_frequency`, `median_frequency`, `human_range_energy`, `lpcc`, `mfcc`, `max_power_spectrum`, `power_bandwidth`, `spectral_centroid`, `spectral_decrease`, `spectral_distance`, `spectral_entropy`, `spectral_kurtosis`, `spectral_positive_turning`, `spectral_roll_off`, `spectral_roll_on`, `spectral_skewness`, `spectral_slope`, `spectral_spread`, `spectral_variation`, `spectrogram_mean_coeff`, `wavelet_abs_mean`, `wavelet_energy`, `wavelet_entropy`, `wavelet_std`, `wavelet_var`."""

cells.append(nbf.v4.new_markdown_cell(m5))

# Code Cell 6: Ekstraksi 68 Fitur TSFEL untuk Semua Polutan
c6 = """import os
import inspect
import tsfel.feature_extraction.features as tsfel_features

FEATURE_LIST = \"\"\"abs_energy auc autocorr average_power calc_centroid calc_max calc_mean
calc_median calc_min calc_std calc_var dfa distance ecdf ecdf_percentile ecdf_percentile_count
ecdf_slope entropy fundamental_frequency higuchi_fractal_dimension hist_mode human_range_energy
hurst_exponent interq_range kurtosis lempel_ziv lpcc max_frequency max_power_spectrum
maximum_fractal_length mean_abs_deviation mean_abs_diff mean_diff median_abs_deviation
median_abs_diff median_diff median_frequency mfcc mse negative_turning neighbourhood_peaks
petrosian_fractal_dimension pk_pk_distance positive_turning power_bandwidth rms skewness slope
spectral_centroid spectral_decrease spectral_distance spectral_entropy spectral_kurtosis
spectral_positive_turning spectral_roll_off spectral_roll_on spectral_skewness spectral_slope
spectral_spread spectral_variation spectrogram_mean_coeff sum_abs_diff wavelet_abs_mean
wavelet_energy wavelet_entropy wavelet_std wavelet_var zero_cross\"\"\".split()

print(f"Total daftar fitur TSFEL yang diekstrak: {len(FEATURE_LIST)} fitur\\n")

def to_scalar(result):
    if isinstance(result, dict) and "values" in result:
        result = result["values"]
    if isinstance(result, (list, tuple, np.ndarray)):
        arr = np.asarray(result, dtype=float)
        return float(np.nanmean(arr))
    return float(result)

def extract_one(fn_name, signal, fs=1):
    fn = getattr(tsfel_features, fn_name)
    params = inspect.signature(fn).parameters
    if "fs" in params:
        result = fn(signal, fs)
    else:
        result = fn(signal)
    return to_scalar(result)

os.makedirs("data/polutan", exist_ok=True)
tsfel_results = {}

for polutan, df in dfs_fixed.items():
    signal_1d = df[polutan].astype(float).values
    row = {}
    
    for i, fn_name in enumerate(FEATURE_LIST, start=1):
        col_name = f"f{i}_{fn_name}"
        row[col_name] = extract_one(fn_name, signal_1d, fs=1)
        
    df_features = pd.DataFrame([row])
    
    # Simpan ke folder data/polutan dan folder data/
    csv_path_polutan = f"data/polutan/{polutan}_Lamongan_TSFEL.csv"
    csv_path_data = f"data/{polutan}_Lamongan_TSFEL.csv"
    
    df_features.to_csv(csv_path_polutan, index=False)
    try:
        df_features.to_csv(csv_path_data, index=False)
    except Exception:
        pass
        
    tsfel_results[polutan] = df_features
    
    print(f"✓ Berhasil mengekstrak {df_features.shape[1]} fitur untuk polutan {polutan:4s} -> Disimpan di {csv_path_polutan}")"""

cells.append(nbf.v4.new_code_cell(c6))

# Code Cell 7: Tampilkan Semua 68 Fitur per Polutan (Transposed) + Tabel Gabungan
c7 = """from IPython.display import display, HTML

# --- Tabel Gabungan Semua Polutan (baris = polutan, kolom = fitur) ---
print("=" * 70)
print("TABEL PERBANDINGAN FITUR TSFEL - SEMUA POLUTAN (68 Fitur)")
print("=" * 70)

combined_list = []
for polutan, df_feat in tsfel_results.items():
    row = df_feat.copy()
    row.insert(0, "Polutan", polutan)
    combined_list.append(row)

df_combined = pd.concat(combined_list, ignore_index=True)
df_combined = df_combined.set_index("Polutan")

display(df_combined.style
    .format("{:.6g}")
    .set_caption("Hasil Ekstraksi 68 Fitur TSFEL untuk Semua Polutan")
    .set_table_styles([
        {'selector': 'caption', 'props': [('font-size', '14px'), ('font-weight', 'bold'), ('text-align', 'left'), ('padding-bottom', '8px')]},
        {'selector': 'th', 'props': [('background-color', '#2c3e50'), ('color', 'white'), ('font-size', '11px'), ('text-align', 'center'), ('padding', '4px 6px')]},
        {'selector': 'td', 'props': [('font-size', '11px'), ('text-align', 'right'), ('padding', '4px 6px')]},
        {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#f2f2f2')]},
    ])
)"""

cells.append(nbf.v4.new_code_cell(c7))

# --- 6. PENJELASAN DOMAIN FITUR ---
m6 = """---

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

Analisis spektral dapat membantu mengidentifikasi pola periodik pada data polutan. Informasi tersebut dapat melengkapi hasil analisis statistik dan temporal sehingga karakteristik deret waktu dapat dipahami dari beberapa sisi."""

cells.append(nbf.v4.new_markdown_cell(m6))

# --- 7. EVALUASI PERBANDINGAN CLUSTERING K-MEANS DAN DETEKSI OUTLIER ---
m7 = """---

# Evaluasi Perbandingan Clustering K-Means dan Deteksi Outlier

Setelah diperoleh 272 fitur hasil ekstraksi TSFEL dari 19 sampel yang berasal dari masing-masing daerah atau mahasiswa, tahap selanjutnya adalah melakukan proses pengelompokan data menggunakan algoritma **K-Means**. Evaluasi clustering dilakukan dengan membandingkan dua skenario jumlah cluster, yaitu pengelompokan menjadi **2 cluster** dan pengelompokan menjadi **3 cluster / 5 cluster**. Proses clustering dilakukan menggunakan dua pendekatan, yaitu data yang telah direduksi dimensinya menggunakan **PCA** dengan 19 komponen utama (PCA 0 hingga PCA 18) serta data yang tetap menggunakan keseluruhan fitur tanpa reduksi PCA. Perbandingan kedua pendekatan tersebut digunakan untuk melihat perbedaan hasil pengelompokan berdasarkan fitur yang telah direduksi dan fitur TSFEL secara keseluruhan.

## Visualisasi Workflow KNIME & Scatter Plot Analytics Platform

Proses ekstraksi, praprocessing, reduksi dimensi PCA, dan pengelompokan K-Means dijalankan menggunakan alur kerja (*workflow*) KNIME Analytics Platform:
 
```{image} ../img/clustering.png
:alt: Workflow Clustering KNIME
:width: 100%
:align: center
```

Hasil proses clustering yang diperoleh melalui alur KNIME kemudian divisualisasikan menggunakan **Scatter Plot**. Grafik tersebut digunakan untuk memperlihatkan posisi dan persebaran 19 sampel mahasiswa/daerah berdasarkan cluster yang terbentuk. Setiap titik pada grafik merepresentasikan satu sampel, sedangkan label atau warna yang berbeda menunjukkan kelompok (*cluster*) tempat sampel tersebut berada. Visualisasi ini membantu melihat pola pemisahan dan kedekatan antaranggota cluster secara lebih jelas.

### Skenario 1: K-Means (k=2) dengan Reduksi Dimensi PCA

```{image} ../img/k2 pca.png
:alt: K-Means k=2 PCA
:width: 100%
:align: center
```

Berdasarkan hasil clustering menggunakan K-Means dengan reduksi dimensi PCA, data 19 mahasiswa/daerah terbagi menjadi dua kelompok. Sebanyak **18 sampel** berada pada `cluster_0`, sedangkan **1 sampel**, yaitu asal Burneh Bangkalan, berada pada `cluster_1`. Pemisahan satu sampel tersebut menunjukkan bahwa karakteristik fitur yang dimilikinya memiliki perbedaan yang cukup jauh dibandingkan dengan sampel lainnya sehingga membentuk kelompok tersendiri pada hasil clustering.

### Skenario 2: K-Means (k=2) Tanpa Reduksi PCA (272 Fitur Penuh)

```{image} ../img/k2 no pca.png
:alt: K-Means k=2 No PCA
:width: 100%
:align: center
```

Pada pengelompokan menggunakan **K-Means dengan seluruh 272 fitur TSFEL yang telah dinormalisasi tanpa melalui reduksi PCA**, diperoleh pembagian cluster yang sama dengan skenario sebelumnya. Sebanyak **18 daerah** masuk ke dalam **`cluster_0`**, sementara **Burneh, Bangkalan** berada sendiri pada **`cluster_1`**. Hasil ini menunjukkan bahwa daerah tersebut tetap memiliki pola karakteristik yang berbeda dibandingkan 18 daerah lainnya, meskipun proses clustering dilakukan menggunakan seluruh fitur TSFEL tanpa reduksi dimensi.

### Skenario 3: K-Means (k=5) dengan Reduksi Dimensi PCA

```{image} ../img/k5 pca.png
:alt: K-Means k=5 PCA
:width: 100%
:align: center
```

Pada skenario dengan jumlah cluster yang lebih banyak dan menggunakan reduksi dimensi **PCA**, hasil pengelompokan menjadi lebih terperinci. Dari 19 mahasiswa/daerah yang dianalisis, terbentuk **5 kelompok** dengan karakteristik yang berbeda. Sebagian besar sampel, yaitu **14 daerah**, terkumpul pada **`cluster_2`**. Sementara itu, empat daerah lainnya membentuk cluster secara terpisah, yaitu **Kraton, Bangkalan** pada **`cluster_4`**, **Kadur, Pamekasan** pada **`cluster_0`**, **Burneh, Bangkalan** pada **`cluster_1`**, serta **Sokobanah** pada **`cluster_3`**. Hasil tersebut menunjukkan bahwa peningkatan jumlah cluster menghasilkan pembagian kelompok yang lebih spesifik dibandingkan skenario dengan jumlah cluster yang lebih sedikit.

### Skenario 4: K-Means (k=5) Tanpa Reduksi PCA (272 Fitur Penuh)

```{image} ../img/k5 no pca.png
:alt: K-Means k=5 No PCA
:width: 100%
:align: center
```

Pada skenario clustering menggunakan **272 fitur TSFEL secara keseluruhan tanpa menerapkan reduksi dimensi PCA**, diperoleh pola pengelompokan yang relatif sama dengan hasil pada skenario menggunakan PCA. Dari 19 daerah, sebagian besar data tergabung dalam **satu cluster utama**, sedangkan empat daerah lainnya masing-masing membentuk **cluster tersendiri**. Dengan demikian, penggunaan seluruh fitur TSFEL tetap menghasilkan pemisahan terhadap beberapa daerah yang memiliki karakteristik berbeda dari kelompok utama."""

cells.append(nbf.v4.new_markdown_cell(m7))

# Buat Objek Notebook
nb = nbf.v4.new_notebook(cells=cells)

print("Mengeksekusi notebook ekstraksi untuk semua polutan (CO, CH4, NO2, SO2)...")
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
ep.preprocess(nb, {'metadata': {'path': '.'}})

os.makedirs("notebooks", exist_ok=True)
with open("notebooks/ekstraksi.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("Berhasil membuat dan mengeksekusi notebooks/ekstraksi.ipynb!")
