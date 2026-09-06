# Penjelasan Properti Statistik

Node **Statistics** digunakan untuk memperoleh informasi statistik deskriptif dari dataset. Statistik deskriptif digunakan untuk menggambarkan karakteristik utama dari data berdasarkan nilai-nilai yang terdapat di dalam dataset.

Pada penelitian kualitas udara, node **Statistics** digunakan untuk menganalisis data konsentrasi polutan, yaitu **O3 (Ozon), CO (Karbon Monoksida), NO2 (Nitrogen Dioksida), dan SO2 (Sulfur Dioksida)**.

Beberapa properti statistik yang dihasilkan oleh KNIME meliputi:

## 1. Column

**Column** menunjukkan nama kolom atau atribut yang sedang dianalisis oleh node **Statistics**.

Pada dataset kualitas udara, kolom yang dianalisis antara lain:

- `date`
- `o3`
- `co`
- `no2`
- `so2`

Kolom `date` digunakan untuk menunjukkan tanggal pengamatan, sedangkan kolom `o3`, `co`, `no2`, dan `so2` berisi nilai konsentrasi masing-masing polutan.

Properti **Column tidak memiliki rumus perhitungan**, karena nilainya merupakan nama atau identitas kolom yang berasal langsung dari dataset.

# 2. Min

**Min (Minimum)** menunjukkan nilai terkecil yang terdapat pada suatu kolom.  
Nilai minimum digunakan untuk mengetahui konsentrasi polutan paling rendah yang tercatat selama periode pengamatan.

### Rumus

Jika terdapat kumpulan data:

$$X = \{x_1, x_2, x_3, \ldots, x_n\}$$

maka nilai minimum dihitung dengan:

$$\text{Min}(X) = \min(x_1, x_2, x_3, \ldots, x_n)$$

**Keterangan:**

- $X$ = kumpulan data
- $x_i$ = nilai data ke-$i$
- $n$ = jumlah data
- $\min$ = fungsi untuk mencari nilai terkecil

Nilai Min menunjukkan konsentrasi polutan paling rendah yang terdapat pada dataset selama periode pengamatan.

# 3. Mean

**Mean** atau rata-rata merupakan nilai yang diperoleh dengan menjumlahkan seluruh nilai data kemudian membaginya dengan jumlah data.  
Mean digunakan untuk mengetahui nilai rata-rata konsentrasi polutan selama periode pengamatan.

### Rumus

$$\bar{x} = \frac{\sum_{i=1}^{n} x_i}{n}$$

**Keterangan:**

- $\bar{x}$ = nilai mean atau rata-rata
- $x_i$ = nilai data ke-$i$
- $n$ = jumlah data
- $\sum$ = operasi penjumlahan

Mean menunjukkan rata-rata konsentrasi polutan selama periode pengamatan.
Mean dapat digunakan untuk membandingkan rata-rata konsentrasi antarpolutan atau melihat kondisi umum konsentrasi suatu polutan.
Namun, mean dapat dipengaruhi oleh nilai ekstrem atau _outlier_. Oleh karena itu, mean sebaiknya dianalisis bersama dengan median, standar deviasi, _skewness_, dan _kurtosis_.

# 4. Median

**Median** merupakan nilai tengah dari sekumpulan data setelah data diurutkan dari nilai terkecil hingga terbesar.  
Median digunakan untuk mengetahui posisi tengah dari distribusi data.  
Median memiliki kelebihan karena relatif tidak mudah dipengaruhi oleh nilai ekstrem atau _outlier_ dibandingkan dengan mean.

### Rumus

**1. Rumus untuk jumlah data ganjil ($n$ ganjil):**

$$\text{Median} = x_{\frac{n+1}{2}}$$

**2. Rumus untuk jumlah data genap ($n$ genap):**

$$\text{Median} = \frac{x_{\frac{n}{2}} + x_{\frac{n}{2}+1}}{2}$$

---

### Contoh Perhitungan

#### A. Jumlah Data Ganjil

Misalkan terdapat data:

- 0.050
- 0.020
- 0.080
- 0.030
- 0.040

Urutkan data dari yang terkecil:

- 0.020
- 0.030
- 0.040
- 0.050
- 0.080

Jumlah data:  
$$n = 5$$

Posisi median:  
$$\frac{5+1}{2} = 3$$

Maka:  
$$\text{Median} = 0.040$$

#### B. Jumlah Data Genap

Misalkan terdapat data:

- 0.020
- 0.030
- 0.040
- 0.080

Jumlah data:  
$$n = 4$$

Dua nilai yang berada di tengah adalah:  
**0.030** dan **0.040**

Maka:  
$$\text{Median} = \frac{0.030 + 0.040}{2} = 0.035$$

Median menunjukkan nilai tengah dari data. Perbandingan antara mean dan median juga dapat memberikan gambaran awal mengenai bentuk distribusi data:

- **Mean $\approx$ Median** $\rightarrow$ data cenderung lebih simetris.
- **Mean > Median** $\rightarrow$ data dapat memiliki kecenderungan miring ke kanan (_skewed right_).
- **Mean < Median** $\rightarrow$ data dapat memiliki kecenderungan miring ke kiri (_skewed left_).

# 5. Max

**Max (Maximum)** menunjukkan nilai terbesar yang terdapat pada suatu kolom.  
Nilai maksimum digunakan untuk mengetahui konsentrasi polutan paling tinggi yang tercatat selama periode pengamatan.

### Rumus

$$\text{Max}(X) = \max(x_1, x_2, x_3, \ldots, x_n)$$

**Keterangan:**

- $X$ = kumpulan data
- $x_i$ = nilai data ke-$i$
- $n$ = jumlah data
- $\max$ = fungsi untuk mencari nilai terbesar

---

### Contoh Perhitungan

Misalkan terdapat data $\text{O}_3$:

- 0.100
- 0.120
- 0.085
- 0.150
- 0.110

Nilai terbesar adalah:  
$$\text{Max} = 0.150$$

Jadi nilai $\text{Max O}_3 = \mathbf{0.150}$.

### Interpretasi

- Nilai Max menunjukkan konsentrasi polutan paling tinggi yang tercatat pada dataset.
- Nilai maksimum juga dapat digunakan sebagai pemeriksaan awal terhadap kemungkinan adanya nilai ekstrem atau _outlier_.

# 6. Standar Deviasi

**Std. Dev. (Standard Deviation)** atau standar deviasi merupakan ukuran yang digunakan untuk mengetahui tingkat penyebaran data terhadap nilai rata-ratanya.  
Standar deviasi menunjukkan seberapa jauh nilai-nilai data cenderung menyebar dari mean.

### Rumus Standar Deviasi Sampel

$$s = \sqrt{\frac{\sum_{i=1}^{n}(x_i - \bar{x})^2}{n - 1}}$$

**Keterangan:**

- $s$ = standar deviasi sampel
- $x_i$ = nilai data ke-$i$
- $\bar{x}$ = mean (rata-rata)
- $n$ = jumlah data
- $n - 1$ = derajat kebebasan (_degree of freedom_)

---

### Contoh Perhitungan

Misalkan terdapat data:

- 2
- 4
- 6

**Langkah 1: Menghitung Mean ($\bar{x}$)**  
$$\bar{x} = \frac{2 + 4 + 6}{3} = \frac{12}{3} = 4$$

**Langkah 2: Menghitung Selisih Setiap Data dengan Mean ($x_i - \bar{x}$)**

- $2 - 4 = -2$
- $4 - 4 = 0$
- $6 - 4 = 2$

**Langkah 3: Mengkuadratkan Selisih ($(x_i - \bar{x})^2$)**

- $(-2)^2 = 4$
- $(0)^2 = 0$
- $(2)^2 = 4$

**Langkah 4: Menjumlahkan Hasil Kuadrat Selisih**  
$$\sum = 4 + 0 + 4 = 8$$

**Langkah 5: Membagi dengan $n - 1$**  
$$\frac{8}{3 - 1} = \frac{8}{2} = 4$$

**Langkah 6: Mengambil Akar Kuadrat**  
$$s = \sqrt{4} = 2$$

Jadi, nilai standar deviasinya adalah:  
$$\text{Std. Dev.} = \mathbf{2}$$

---

### Interpretasi

- **Standar deviasi kecil** $\rightarrow$ data cenderung berkumpul di sekitar mean.
- **Standar deviasi besar** $\rightarrow$ data memiliki penyebaran yang lebih besar dari mean.
- Dalam data kualitas udara, standar deviasi dapat menunjukkan tingkat variasi konsentrasi polutan selama periode pengamatan.

# 7. Kurtosis

**Kurtosis** merupakan ukuran statistik yang digunakan untuk menggambarkan karakteristik distribusi data, khususnya berkaitan dengan bentuk ekor (_tail_) distribusi dan kecenderungan munculnya nilai ekstrem.  
Kurtosis menggunakan momen keempat dari distribusi data.

---

### Rumus Dasar Kurtosis

$$K = \frac{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^4}{\left[\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2\right]^2}$$

**Keterangan:**

- $K$ = nilai kurtosis
- $x_i$ = nilai data ke-$i$
- $\bar{x}$ = mean
- $n$ = jumlah data
- $(x_i - \bar{x})^4$ = selisih data terhadap mean yang dipangkatkan empat

> **Catatan:** Pangkat empat menyebabkan kurtosis sangat sensitif terhadap nilai yang jauh dari mean.

---

### Excess Kurtosis

Kurtosis juga sering dinyatakan sebagai _excess kurtosis_:

$$K_{\text{excess}} = K - 3$$

Pada **distribusi normal**:

- $K = 3$
- atau jika menggunakan _excess kurtosis_: $K_{\text{excess}} = 0$

### Interpretasi

- **Kurtosis tinggi** $\rightarrow$ menunjukkan distribusi memiliki ekor yang relatif berat (_heavy-tailed_) dan cenderung memiliki lebih banyak nilai ekstrem.
- **Kurtosis rendah** $\rightarrow$ menunjukkan distribusi memiliki ekor yang relatif ringan (_light-tailed_).
- **Excess kurtosis mendekati 0** $\rightarrow$ menunjukkan karakteristik distribusi yang mendekati distribusi normal.

> **Catatan Tambahan:** Rumus kurtosis dapat memiliki beberapa bentuk perhitungan (kurtosis populasi, sampel, dan excess kurtosis). Oleh karena itu, interpretasi angka kurtosis harus disesuaikan dengan definisi yang digunakan oleh perangkat lunak/software yang dipakai.

# 8. Skewness

**Skewness** merupakan ukuran statistik yang menunjukkan tingkat kemiringan atau ketidaksimetrisan distribusi data terhadap nilai rata-ratanya.  
Skewness menggunakan momen ketiga dari distribusi data.

### Rumus Dasar Skewness

$$\text{Skewness} = \frac{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^3}{\left[\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2\right]^{3/2}}$$

**Keterangan:**

- $x_i$ = nilai data ke-$i$
- $\bar{x}$ = mean
- $n$ = jumlah data
- $(x_i - \bar{x})^3$ = selisih data terhadap mean yang dipangkatkan tiga

### Interpretasi Skewness

1. **Skewness $\approx$ 0**  
   Distribusi data cenderung **relatif simetris**.

2. **Skewness > 0 (Positif)**  
   Distribusi cenderung **miring ke kanan** (_positively skewed_). Menunjukkan adanya ekor distribusi ke arah nilai yang lebih besar.

3. **Skewness < 0 (Negatif)**  
   Distribusi cenderung **miring ke kiri** (_negatively skewed_). Menunjukkan adanya ekor distribusi ke arah nilai yang lebih kecil.

#### Contoh:

- Jika $\text{Skewness} = 1.25$ $\rightarrow$ data mempunyai distribusi miring ke kanan.
- Jika $\text{Skewness} = -0.80$ $\rightarrow$ data cenderung miring ke kiri.

#### Interpretasi pada Data Polutan:

Skewness dapat digunakan untuk mengetahui distribusi konsentrasi $\text{O}_3$, $\text{CO}$, $\text{NO}_2$, dan $\text{SO}_2$. Misal, jika skewness $\text{CO}$ bernilai positif, berarti sebagian besar nilai $\text{CO}$ cenderung berada pada konsentrasi lebih rendah, tetapi terdapat beberapa pengamatan dengan konsentrasi yang sangat tinggi.

## 9. Metrik Kualitas / Anomali Data

Kelompok metrik ini memegang peranan krusial saat melakukan ekstraksi data mentah melalui API atau dari citra satelit, karena rentan terhadap kegagalan saat proses perekaman nilai.

- **No. missings:** Menunjukkan jumlah sel yang kosong (NULL / NA) akibat data tidak berhasil terekam pada periode waktu tertentu.
- **No. NaNs (Not a Number):** Menunjukkan jumlah entri yang dapat dibaca tetapi nilainya tidak terdefinisi secara matematis (contohnya 0/0).
- **No. +infs / No. -infs:** Menunjukkan adanya nilai batas tak terhingga.
- **Perhitungan Manual:** Menghitung frekuensi (N) kemunculan baris yang memuat nilai-nilai khusus tersebut.

# **Langkah-Langkah Analisis Data Polutan Lamongan: Dari Database Cloud PosstgreSQL ke KNIME**

Berikut tahapan-tahapan untuk menghubungkan database PostgreSQL di platform Aiven serta mengekstraksi metrik statistika deskriptif memanfaatkan KNIME Analytics Platform.

## Langkah 1: Memmbuat Service PostgreSQL

Pertama, buka platform Aiven melalui browser dan login menggunakan akun yang telah dibuat. Setelah berhasil login, masuk ke halaman Console Aiven untuk membuat layanan database cloud. Setelah itu waktunya kita buat service PostgreSQL.

Pada halaman Aiven:

1. Pilih Create service.
2. Pilih database PostgreSQL.
3. Tentukan nama service.
4. Pilih cloud/region yang tersedia.
5. Pilih paket/plan yang digunakan.
6. Kemudian buat service.

Service PostgreSQL yang digunakan dalam proyek adalah:

```{code-cell}
Service : pg-f512d5
Database: PostgreSQL
```

Setelah proses pembuatan selesai, status service berubah menjadi Running.

---

## Langkah 2: Memperoleh Kredensial Database dari Aiven

Sebelum menyambungkan koneksi melalui aplikasi apa pun, kita membutuhkan informasi kredensial server.

1. Buka tab **Overview** pada layanan (_service_) PostgreSQL yang sedang beroperasi (`pg-c4fbe52`).
2. Pada bagian **Connection information**, catat parameter-parameter berikut ini:
   - **Host:** `pg-f512d5-irwandwi712-14a9.e.aivencloud.com`
   - **Port:** `24781`
   - **User:** `avnadmin`
   - **Password:** (Klik ikon mata atau opsi _copy_ untuk menyalin kata sandi rahasia)
   - **SSL mode:** `require`
3. Pastikan Anda telah mengunduh sertifikat SSL (klik **Show** pada bagian _CA certificate_ kemudian unduh) apabila _client_ yang Anda gunakan mensyaratkannya.

![Aiven PostgreSQL Console](../../img/aiven.png)

---

## Langkah 3: Menyiapkan Data dan Upload di Aiven

1. Data hasil pengolahan data polutan disimpan dalam format CSV. Data yang digunakan terdiri dari beberapa polutan yaitu `CO`,`NO2`,`O3`, dan`SO2`.
2. Menyiapkan Python untuk Upload Data. Karena `psql` belum tersedia pada komputer, proses upload data dilakukan menggunakan Python. Library yang digunakan yaitu :
   **pandas** → membaca dan mengolah file CSV, **sqlalchemy** → membuat koneksi ke database PostgreSQL, **psycopg2-binary** → driver PostgreSQL untuk Python
3. Membuat Program Upload CSV ke Aiven. Program ini membaca seluruh file CSV pada folder `data`, kemudian mengirimkan data tersebut ke database PostgreSQL Aiven.

Kode Program (`upload.py`):

```python
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://avnadmin:PASSWORD@"
    "pg-f512d5-irwandwi712-14a9.e.aivencloud.com:24781/"
    "defaultdb?sslmode=require"
)

engine = create_engine(DATABASE_URL)
folder = Path("data")
files = list(folder.glob("*.csv"))

for file in files:
    df = pd.read_csv(file)

    # Mengubah nama file menjadi nama tabel (lowercase & replace spasi dengan underscore)
    table_name = file.stem.lower().replace(" ", "_")

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )
```

> **Catatan:** Bagian `PASSWORD` pada `DATABASE_URL` diganti dengan password Aiven milik sendiri.

## ![Aiven PostgreSQL Console](../../dataset.png)

## Langkah 4: Menyusun Alur Kerja (Workflow) di KNIME

Beralih menuju KNIME Analytics Platform guna menarik data dari database dan melakukan perhitungan statistiknya secara otomatis.

1. Jalankan **KNIME Analytics Platform** lalu buatlah _workflow_ (alur kerja) yang baru.
2. Tarik (_drag-and-drop_) _node_ di bawah ini dari _Node Repository_ menuju ke _workspace_:
   - **PostgreSQL Connector:** Berfungsi menghubungkan KNIME dengan server Aiven.
   - **DB Table Selector:** Berfungsi untuk menyeleksi tabel di dalam database.
   - **DB Reader:** Berfungsi untuk memuat tabel ke dalam memori KNIME.
   - **Statistics:** Berfungsi untuk menghitung metrik-metrik statistik.
3. Hubungkan setiap _node_ tersebut mengikuti urutan yang telah disebutkan di atas.
4. **Konfigurasi Node:**
   - Lakukan klik ganda pada **PostgreSQL Connector**, lalu isikan _Hostname_, _Port_, _Database name_ (`psd_polutan_lamongan`), serta _Credentials_ (User & Password) yang identik dengan langkah 2.
   - Lakukan klik ganda pada **DB Table Selector**, kemudian pilih skema `public` serta tabel `psd_polutan_lamongan`.
5. Klik kanan pada **DB Reader** lalu pilih opsi **Execute**. Jika prosesnya berhasil, lampu indikator di bagian bawah _node_ akan berubah menjadi hijau.

![Alur Kerja Database dan Statistik di KNIME](../../img/knime_node.png)

---

## Langkah 5: Membaca Output Statistika Deskriptif

Setelah data berhasil dimuat ke dalam KNIME, tahapan yang terakhir adalah menjalankan perhitungan analitiknya.

1. Klik kanan pada node **Statistics** kemudian pilih **Execute**.
2. Bila lampu indikator telah berwarna hijau, klik kanan kembali pada node **Statistics** lalu pilih menu **Statistics View** (atau ikon bergambar kaca pembesar).
3. Tabel metrik statistik akan ditampilkan, yang memuat:
   - **Min, Max, Mean:** Guna mengamati rentang serta nilai rata-rata dari masing-masing polutan.
   - **Std. deviation & Variance:** Guna meninjau tingkat fluktuasi nilai gas di udara.
   - **Skewness & Kurtosis:** Guna melihat bentuk asimetri dan tingkat keberadaan nilai-nilai yang ekstrem (_outlier_).
   - **No. missings:** Menyatakan jumlah data yang kosong.
   - **Histogram:** Menyajikan visualisasi mengenai sebaran datanya.

![Tabel Hasil Output Node Statistics](../../img/knime_statistik.png)

## Perhitungan Manual Statistik O3

Berdasarkan dataset kolom O3 memiliki 391 baris data, dengan 380 data valid dan 11 data missing.

## 1. Perhitungan Minimum (Min)

Minimum merupakan nilai paling kecil yang terdapat dalam dataset.

### Rumus

$$
Min = \min(x_1,x_2,x_3,\ldots,x_n)
$$

Dari seluruh 380 data O3 yang valid, diperoleh nilai terkecil:

$$
Min = 0.1085283992
$$

### Hasil

$$
\boxed{Min = 0.1085283992}
$$

Dengan demikian, nilai O3 terendah pada dataset adalah **0.1085283992**.

---

## 2. Perhitungan Mean

Mean atau rata-rata merupakan jumlah seluruh nilai dibagi dengan jumlah data yang valid.

### Rumus

$$
\bar{x} = \frac{\sum_{i=1}^{n}x_i}{n}
$$

Keterangan:

- $\bar{x}$ = nilai rata-rata
- $x_i$ = setiap nilai O3
- $n$ = jumlah data valid
- $\sum x_i$ = jumlah seluruh nilai O3

Diketahui:

$$
n = 380
$$

Jumlah seluruh nilai O3:

$$
\sum x_i = 43.6027481776
$$

Kemudian nilai tersebut dimasukkan ke dalam rumus:

$$
\bar{x} =
\frac{43.6027481776}{380}
$$

Sehingga diperoleh:

$$
\bar{x} = 0.1147440742
$$

### Hasil

$$
\boxed{Mean = 0.1147440742}
$$

Jadi, rata-rata nilai O3 dari 380 data valid adalah **0.1147440742**.

---

## 3. Perhitungan Median

Median merupakan nilai tengah setelah seluruh data diurutkan dari nilai terkecil hingga terbesar.

Jumlah data valid adalah:

$$
n = 380
$$

Karena jumlah data merupakan bilangan genap, maka median dihitung menggunakan dua nilai tengah.

### Rumus

$$
Median =
\frac{x_{\frac{n}{2}} + x_{\frac{n}{2}+1}}{2}
$$

Substitusi jumlah data:

$$
Median =
\frac{x_{190}+x_{191}}{2}
$$

Artinya, setelah seluruh 380 data O3 diurutkan:

1. Ambil data ke-190.
2. Ambil data ke-191.
3. Jumlahkan kedua nilai tersebut.
4. Bagi hasilnya dengan 2.

Dari data yang telah diurutkan diperoleh:

$$
Median = 0.1145598377
$$

### Hasil

$$
\boxed{Median = 0.1145598377}
$$

Jadi, nilai tengah dari data O3 adalah **0.1145598377**.

---

## 4. Perhitungan Standard Deviation

Standard deviation atau standar deviasi digunakan untuk mengetahui seberapa besar penyebaran data terhadap nilai rata-ratanya.

Dalam perhitungan ini digunakan standar deviasi sampel.

### Rumus

$$
s =
\sqrt{
\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}
}
$$

Keterangan:

- $s$ = standar deviasi
- $x_i$ = setiap nilai O3
- $\bar{x}$ = mean
- $n$ = jumlah data valid
- $n-1$ = derajat kebebasan

Diketahui:

$$
\bar{x} = 0.1147440742
$$

dan:

$$
n = 380
$$

### Langkah 1: Menghitung selisih setiap data dengan mean

Contoh nilai pertama:

$$
x_1 = 0.117016
$$

Maka:

$$
x_1-\bar{x}
=
0.117016-0.1147440742
$$

$$
=0.0022719258
$$

Contoh nilai kedua:

$$
x_2 = 0.116607
$$

$$
x_2-\bar{x}
=
0.116607-0.1147440742
$$

$$
=0.0018629258
$$

Contoh nilai ketiga:

$$
x_3 = 0.115195
$$

$$
x_3-\bar{x}
=
0.115195-0.1147440742
$$

$$
=0.0004509258
$$

### Langkah 2: Menguadratkan hasil selisih

Untuk data pertama:

$$
(0.0022719258)^2
=
0.0000051616
$$

Untuk data kedua:

$$
(0.0018629258)^2
=
0.0000034705
$$

Untuk data ketiga:

$$
(0.0004509258)^2
=
0.0000002033
$$

Proses tersebut dilakukan pada seluruh 380 data.

### Langkah 3: Menjumlahkan seluruh hasil kuadrat

Dari seluruh data diperoleh:

$$
\sum(x_i-\bar{x})^2
=
0.0023875018
$$

### Langkah 4: Membagi dengan $n-1$

Karena:

$$
n = 380
$$

maka:

$$
n-1 = 379
$$

Sehingga:

$$
\frac{0.0023875018}{379}
=
0.0000062997
$$

### Langkah 5: Menghitung akar kuadrat

$$
s =
\sqrt{0.0000062997}
$$

Sehingga:

$$
s = 0.0025098759
$$

### Hasil

$$
\boxed{Std.Dev. = 0.0025098759}
$$

Jadi, standar deviasi O3 adalah **0.0025098759**.

Nilai ini menunjukkan tingkat penyebaran nilai O3 terhadap nilai rata-ratanya.

---

## 5. Perhitungan Skewness

Skewness digunakan untuk mengetahui bentuk kemencengan distribusi data.

Interpretasi umum:

- $Skewness \approx 0$ → distribusi relatif simetris
- $Skewness > 0$ → distribusi miring ke kanan
- $Skewness < 0$ → distribusi miring ke kiri

### Rumus

Skewness sampel dihitung dengan:

$$
Skewness =
\frac{n}{(n-1)(n-2)}
\frac{\sum(x_i-\bar{x})^3}{s^3}
$$

Diketahui:

$$
n = 380
$$

$$
\bar{x} = 0.1147440742
$$

$$
s = 0.0025098759
$$

### Langkah 1: Menghitung selisih data dengan mean

Contoh data pertama:

$$
x_1 = 0.117016
$$

Maka:

$$
x_1-\bar{x}
=
0.117016-0.1147440742
$$

$$
=0.0022719258
$$

### Langkah 2: Pangkat tiga hasil selisih

$$
(0.0022719258)^3
\approx 0.00000001172
$$

Contoh data kedua:

$$
x_2 = 0.116607
$$

$$
x_2-\bar{x}
=
0.0018629258
$$

Kemudian:

$$
(0.0018629258)^3
\approx 0.00000000646
$$

Proses tersebut dilakukan pada seluruh 380 data.

### Langkah 3: Menjumlahkan hasil pangkat tiga

Diperoleh:

$$
\sum(x_i-\bar{x})^3
=
0.0000024603
$$

### Langkah 4: Menghitung $s^3$

Diketahui:

$$
s = 0.0025098759
$$

Maka:

$$
s^3 =
(0.0025098759)^3
$$

### Langkah 5: Memasukkan ke dalam rumus

$$
Skewness =
\frac{380}{(379)(378)}
\times
\frac{0.0000024603}
{(0.0025098759)^3}
$$

Sehingga diperoleh:

$$
Skewness = 0.4127468630
$$

### Hasil

$$
\boxed{Skewness = 0.4127468630}
$$

Karena nilai skewness bernilai positif:

$$
0.4127468630
$$

maka distribusi data O3 **cenderung miring ke kanan (positively skewed)**.
