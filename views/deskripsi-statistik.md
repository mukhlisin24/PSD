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

# Analisis dan Komputasi Statistik Deskriptif

Halaman ini berisi implementasi komputasi statistik deskriptif secara otomatis menggunakan Python untuk menganalisis data konsentrasi polutan di Kabupaten Lamongan, yaitu **CO (Karbon Monoksida)**, **NO₂ (Nitrogen Dioksida)**, **O₃ (Ozon)**, dan **SO₂ (Sulfur Dioksida)**.

---

## 1. Konsep & Rumus Properti Statistik

Statistik deskriptif digunakan untuk meringkas, menggambarkan, dan memahami karakteristik distribusi data pengamatan satelit Sentinel-5P.

### A. Ukuran Pemusatan Data (Central Tendency)
1. **Mean (Rata-rata):**
   $$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$
2. **Median (Nilai Tengah):**
   Nilai data ke-$\frac{n+1}{2}$ setelah data diurutkan dari terkecil hingga terbesar.
3. **Min & Max (Rentang Nilai):**
   Menunjukkan konsentrasi terendah $\min(X)$ dan tertinggi $\max(X)$ selama periode observasi.

### B. Ukuran Penyebaran Data (Dispersion)
1. **Variansi ($s^2$) & Standar Deviasi ($s$):**
   $$s^2 = \frac{\sum_{i=1}^{n}(x_i - \bar{x})^2}{n - 1}, \quad s = \sqrt{s^2}$$
2. **Interquartile Range (IQR):**
   $$\text{IQR} = Q_3 - Q_1$$

### C. Bentuk Distribusi (Shape of Distribution)
1. **Skewness (Tingkat Kemiringan):**
   $$\text{Skewness} = \frac{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^3}{s^3}$$
   - **$\approx 0$**: Distribusi simetris.
   - **$> 0$ (Positif)**: Miring ke kanan (*right-skewed*), terdapat ekor panjang ke konsentrasi tinggi.
   - **$< 0$ (Negatif)**: Miring ke kiri (*left-skewed*).
2. **Kurtosis (Tingkat Keruncingan / Ekor Ekstrem):**
   $$\text{Kurtosis} = \frac{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^4}{s^4} - 3$$
   - Nilai kurtosis yang tinggi menunjukkan keberadaan data ekstrem (*outlier*).

---

## 2. Load Dataset Polutan

Dataset yang digunakan berasal dari folder `data/` hasil pengamatan satelit Sentinel-5P untuk wilayah Kabupaten Lamongan.

```{code-cell} ipython3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Path folder data relatif terhadap root repository
data_paths = {
    "CO": "data/CO_lamongan.csv",
    "NO2": "data/No2_lamongan.csv",
    "O3": "data/O3_lamongan.csv",
    "SO2": "data/SO2_lamongan.csv"
}

# Membaca data ke dalam dictionary DataFrame
dfs = {}
for polutan, path in data_paths.items():
    dfs[polutan] = pd.read_csv(path)
    print(f"Polutan {polutan:4s}: {len(dfs[polutan])} baris data dimuat.")
```

---

## 3. Komputasi Tabel Statistik Deskriptif Lengkap

Kita menghitung seluruh metrik statistik utama (Jumlah observasi, Missing value, Min, Max, Mean, Median, Standar Deviasi, Variansi, Skewness, dan Kurtosis) untuk seluruh polutan:

```{code-cell} ipython3
summary_list = []

for polutan, df in dfs.items():
    col = df[polutan].dropna()
    total_records = len(df)
    missing_count = df[polutan].isnull().sum()
    missing_pct = (missing_count / total_records) * 100
    
    q1 = col.quantile(0.25)
    q3 = col.quantile(0.75)
    iqr = q3 - q1
    
    summary_list.append({
        "Polutan": polutan,
        "Total Data": total_records,
        "Valid": len(col),
        "Missing": f"{missing_count} ({missing_pct:.1f}%)",
        "Min": col.min(),
        "Mean": col.mean(),
        "Median": col.median(),
        "Max": col.max(),
        "Std Dev": col.std(),
        "Variance": col.var(),
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "Skewness": col.skew(),
        "Kurtosis": col.kurtosis()
    })

df_summary = pd.DataFrame(summary_list)
# Tampilkan tabel statistik format desimal rapi
pd.set_option('display.float_format', lambda x: '%.6f' % x)
df_summary
```

---

## 4. Analisis Detail Tiap Polutan

```{code-cell} ipython3
for polutan, df in dfs.items():
    col = df[polutan].dropna()
    print("=" * 60)
    print(f"RINGKASAN STATISTIK POLUTAN: {polutan}")
    print("=" * 60)
    print(f"- Jumlah Pengamatan Valid : {len(col)}")
    print(f"- Nilai Minimum           : {col.min():.6f}")
    print(f"- Nilai Rata-rata (Mean)  : {col.mean():.6f}")
    print(f"- Nilai Tengah (Median)   : {col.median():.6f}")
    print(f"- Nilai Maksimum          : {col.max():.6f}")
    print(f"- Standar Deviasi         : {col.std():.6f}")
    print(f"- Skewness (Kemiringan)   : {col.skew():.4f}")
    print(f"- Kurtosis (Keruncingan)  : {col.kurtosis():.4f}")
    print()
```

---

## 5. Visualisasi Distribusi & Deteksi Outlier

Berikut visualisasi Boxplot dan Histogram untuk memahami sebaran nilai masing-masing polutan:

```{code-cell} ipython3
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

for idx, (polutan, df) in enumerate(dfs.items()):
    ax = axes[idx]
    col = df[polutan].dropna()
    
    # Plot histogram + KDE
    ax.hist(col, bins=30, color=colors[idx], alpha=0.7, edgecolor='black', density=True)
    ax.set_title(f"Distribusi Konsentrasi {polutan}", fontsize=12, fontweight='bold')
    ax.set_xlabel("Konsentrasi", fontsize=10)
    ax.set_ylabel("Densitas", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
```

---

## 6. Interpretasi Hasil

1. **Karbon Monoksida (CO):**
   - Memiliki nilai **Skewness tinggi (16.13)** dan **Kurtosis (267.67)**, menunjukkan sebagian besar data terkonsentrasi pada nilai rendah sekitar `0.029 - 0.033`, namun terdapat beberapa anomali/lonjakan polutan yang sangat tinggi (mencapai `0.901`).
2. **Nitrogen Dioksida (NO₂):**
   - Memiliki tingkat *skewness* positif moderat (`1.47`) dengan nilai rata-rata `0.000027`.
3. **Ozon (O₃):**
   - Menunjukkan distribusi yang paling simetris (*Skewness* `0.38` dan *Kurtosis* `0.10`), dengan konsentrasi berkisar antara `0.108` hingga `0.124`.
4. **Sulfur Dioksida (SO₂):**
   - Memiliki tingkat missing value tertinggi (190 data kosong dari 366 observasi), dengan persebaran yang relatif simetris di sekitar `0.000076`.
