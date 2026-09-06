# import pandas as pd
# from sqlalchemy import create_engine
# from pathlib import Path

# # ==========================================
# # Koneksi Aiven PostgreSQL
# # ==========================================

# DATABASE_URL = (
#     "postgresql://avnadmin:Pw@"
#     "pg-f512d5-irwandwi712-14a9.e.aivencloud.com:24781/"
#     "defaultdb?sslmode=require"
# )

# engine = create_engine(DATABASE_URL)

# # ==========================================
# # Folder CSV
# # ==========================================

# folder = Path("data")

# files = list(folder.glob("*.csv"))

# print(f"Ditemukan {len(files)} file CSV\n")

# # ==========================================
# # Upload semua CSV
# # ==========================================

# for file in files:

#     print(f"Membaca: {file.name}")

#     # Baca CSV
#     df = pd.read_csv(file)

#     # Nama tabel berdasarkan nama file
#     table_name = file.stem.lower().replace(" ", "_")

#     print(f"  Jumlah data : {len(df)}")
#     print(f"  Kolom       : {list(df.columns)}")
#     print(f"  Tabel Aiven : {table_name}")

#     # Upload ke Aiven
#     df.to_sql(
#         table_name,
#         engine,
#         if_exists="replace",
#         index=False
#     )

#     print(f"  ✓ Berhasil upload ke tabel '{table_name}'\n")

# print("================================")
# print("SEMUA DATA BERHASIL DIUPLOAD")
# print("================================")

import os
import pandas as pd
from sqlalchemy import create_engine

# Konfigurasi Aiven
host = os.getenv("AIVEN_HOST")
port = os.getenv("AIVEN_PORT")
database = os.getenv("AIVEN_DATABASE")
user = os.getenv("AIVEN_USER")
password = os.getenv("AIVEN_PASSWORD")

if not all([host, port, database, user, password]):
    raise ValueError("Konfigurasi Aiven belum lengkap.")

# Koneksi PostgreSQL Aiven
engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
)

# Folder CSV
csv_folder = "data"

# Cari file CSV
csv_files = [
    os.path.join(csv_folder, file)
    for file in os.listdir(csv_folder)
    if file.endswith(".csv")
]

print(f"Ditemukan {len(csv_files)} file CSV.")

for csv_file in csv_files:
    df = pd.read_csv(csv_file)

    filename = os.path.basename(csv_file)
    table_name = os.path.splitext(filename)[0].lower()

    print(f"\nMengupload: {filename}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Berhasil upload ke tabel: {table_name}")

print("\nSEMUA DATA BERHASIL DIUPLOAD")