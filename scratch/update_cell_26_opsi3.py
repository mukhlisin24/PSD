import json

with open("uts/klasifikasi tutupan lahan jatim.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

full_src = "".join(nb['cells'][26]['source'])

# Pastikan import median_filter ada
if "median_filter" not in full_src:
    full_src = full_src.replace(
        "from scipy.ndimage import distance_transform_edt",
        "from scipy.ndimage import distance_transform_edt, median_filter"
    )

# Ganti blok post-processing dengan kombinasi buffer spasial + majority/median filter
old_block_marker = "# POST-PROCESSING SPASIAL: FILTER BUFFER MANGROVE PESISIR"
# Cari posisi blok lama
idx_start = full_src.find(old_block_marker)

new_block = """# ==============================================================================
# POST-PROCESSING SPASIAL: KOMBINASI FILTER BUFFER (OPSI 1) & MAJORITY FILTER (OPSI 3)
# 1. Filter Buffer: Mangrove secara biologis hanya hidup di dekat perairan/pesisir.
#    Mangrove di pedalaman (> 1000m dari air) direklasifikasi ke Lahan Pertanian (2).
# 2. Majority / Median Filter (3x3): Menghilangkan salt-and-pepper noise (bintik-bintik
#    piksel mangrove terisolasi yang nyasar di tengah pemukiman/sawah).
# ==============================================================================
JARAK_MAKS_MANGROVE = 1000  # meter dari badan air terdekat
is_air = (grid_klasifikasi == 4)

if is_air.sum() > 0:
    # 1. Koreksi Jarak Spasial (Pesisir vs Pedalaman)
    jarak_ke_air = distance_transform_edt(~is_air) * resolusi_m
    mangrove_pedalaman = (grid_klasifikasi == 5) & (jarak_ke_air > JARAK_MAKS_MANGROVE)
    jml_pedalaman = int(mangrove_pedalaman.sum())
    if jml_pedalaman > 0:
        grid_klasifikasi[mangrove_pedalaman] = 2  # Reklasifikasi ke Pertanian
        print(f'[POST-PROCESSING] Koreksi {jml_pedalaman} piksel mangrove pedalaman (> {JARAK_MAKS_MANGROVE}m) menjadi Lahan Pertanian.')

    # 2. Majority / Median Filter (Hilangkan bintik-bintik terisolasi / Salt-and-Pepper)
    grid_tetangga = median_filter(grid_klasifikasi, size=3)
    mangrove_terisolasi = (grid_klasifikasi == 5) & (grid_tetangga != 5)
    jml_terisolasi = int(mangrove_terisolasi.sum())
    if jml_terisolasi > 0:
        # Ganti piksel bintik mangrove yang salah dengan kelas dominan di sekitarnya (pemukiman/sawah)
        grid_klasifikasi[mangrove_terisolasi] = grid_tetangga[mangrove_terisolasi]
        print(f'[POST-PROCESSING] Koreksi {jml_terisolasi} bintik piksel mangrove terisolasi menggunakan Majority Filter.')
"""

# Cari posisi '# Visualisasi Peta Tematik'
idx_end = full_src.find("# Visualisasi Peta Tematik")
if idx_start != -1 and idx_end != -1:
    full_src = full_src[:idx_start] + new_block + "\n" + full_src[idx_end:]

lines = [l + "\n" for l in full_src.split("\n")]
if lines and lines[-1] == "\n":
    lines = lines[:-1]
nb['cells'][26]['source'] = lines

with open("uts/klasifikasi tutupan lahan jatim.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Berhasil memperbarui Cell 26 notebook dengan Opsi 1 + Opsi 3.")
