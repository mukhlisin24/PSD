import json

with open("uts/klasifikasi tutupan lahan jatim.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

cell_26_src = nb['cells'][26]['source']
full_src = "".join(cell_26_src)

# Sisipkan import scipy distance_transform_edt jika belum ada
if "distance_transform_edt" not in full_src:
    full_src = full_src.replace(
        "import matplotlib.patches as mpatches",
        "import matplotlib.patches as mpatches\nfrom scipy.ndimage import distance_transform_edt"
    )

# Pastikan resolusi_m dibaca saat load raster tersimpan
target_load = "crs_raster = src_saved.crs"
replacement_load = "crs_raster = src_saved.crs\n        resolusi_m = src_saved.res[0]"
if target_load in full_src and "resolusi_m = src_saved.res[0]" not in full_src:
    full_src = full_src.replace(target_load, replacement_load)

# Pastikan resolusi_m juga ada saat prediksi baru
target_new = "crs_raster = src.crs"
replacement_new = "crs_raster = src.crs\n            resolusi_m = src.res[0] * step"
if target_new in full_src and "resolusi_m = src.res[0] * step" not in full_src:
    full_src = full_src.replace(target_new, replacement_new)

# Tambahkan blok post-processing sebelum simpan GeoTIFF / visualisasi
post_processing_block = """
# ==============================================================================
# POST-PROCESSING SPASIAL: FILTER BUFFER MANGROVE PESISIR (1500 Meter)
# Mangrove secara biologis hanya tumbuh di pesisir/intertidal (< 1500m dari air).
# Piksel mangrove di pedalaman/daratan (> 1500m) otomatis dialihkan ke Pertanian (2).
# ==============================================================================
JARAK_MAKS_MANGROVE = 1500  # meter
is_air = (grid_klasifikasi == 4)
if is_air.sum() > 0:
    jarak_ke_air = distance_transform_edt(~is_air) * resolusi_m
    mangrove_pedalaman = (grid_klasifikasi == 5) & (jarak_ke_air > JARAK_MAKS_MANGROVE)
    jml_dikoreksi = int(mangrove_pedalaman.sum())
    if jml_dikoreksi > 0:
        grid_klasifikasi[mangrove_pedalaman] = 2  # Reklasifikasi ke Pertanian
        print(f'[POST-PROCESSING] Berhasil mengoreksi {jml_dikoreksi} piksel mangrove pedalaman (> {JARAK_MAKS_MANGROVE}m dari air) menjadi Lahan Pertanian.')
"""

if "POST-PROCESSING SPASIAL: FILTER BUFFER MANGROVE" not in full_src:
    target_insert = "# Visualisasi Peta Tematik Tutupan Lahan"
    full_src = full_src.replace(target_insert, post_processing_block.strip() + "\n\n" + target_insert)

# Simpan kembali ke cell
lines = [l + "\n" for l in full_src.split("\n")]
if lines and lines[-1] == "\n":
    lines = lines[:-1]
nb['cells'][26]['source'] = lines

with open("uts/klasifikasi tutupan lahan jatim.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Berhasil mengupdate Cell 26 notebook dengan filter jarak 1500m.")
