from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

df = pd.read_csv(BASE_DIR / "No2_lamongan.csv")

print("Data berhasil dibaca!")
print(df.head())
print("Jumlah baris:", len(df))
print("Kolom:", df.columns.tolist())