import streamlit as st
import pandas as pd
import numpy as np
import json
import joblib
from pathlib import Path
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN STREAMLIT
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Klasifikasi Spasial Tutupan Lahan Jawa Timur",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3799;
        margin-bottom: 0.3rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4b6584;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    .badge-pill {
        display: inline-block;
        background-color: #ebf3ff;
        color: #1e3799;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.88rem;
        border: 1px solid #c7dcff;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #f1f2f6;
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 2. HELPER UNTUK MENCARI BERKAS DATA SECARA FLEKSIBEL
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

def get_file_path(filename: str):
    candidates = [
        BASE_DIR / filename,
        BASE_DIR / "data" / filename,
        BASE_DIR.parent / "streamlit" / "data" / filename,
        BASE_DIR.parent / "uts" / "deploy" / filename,
        Path("streamlit/data") / filename,
        Path("data") / filename,
        Path(filename)
    ]
    for p in candidates:
        if p.exists():
            return p
    return None

@st.cache_data
def load_metrics():
    path = get_file_path("metrik_evaluasi.json")
    if path and path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

@st.cache_data
def load_feature_importance():
    path = get_file_path("feature_importance.csv")
    if path and path.exists():
        return pd.read_csv(path)
    return None

@st.cache_data
def load_confusion_matrix_data():
    path = get_file_path("confusion_matrix.csv")
    if path and path.exists():
        return pd.read_csv(path, index_col=0)
    return None

@st.cache_data
def load_pixel_test_sample(nrows=5000):
    path = get_file_path("prediksi_pixel_test.csv")
    if path and path.exists():
        return pd.read_csv(path, nrows=nrows)
    return None

@st.cache_data
def load_polygon_test():
    path = get_file_path("prediksi_poligon_test.csv")
    if path and path.exists():
        return pd.read_csv(path)
    return None


# ------------------------------------------------------------------------------
# 3. SIDEBAR & NAVIGASI MENU
# ------------------------------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/b/bb/Coat_of_arms_of_East_Java.svg", width=85)
    st.title("Tutupan Lahan Jatim")
    st.caption("Sentinel-2 Level-2A • Random Forest")
    st.divider()

    menu = st.radio(
        "Menu:",
        [
            "Overview & Latar Belakang",
            "Peta Klasifikasi Interaktif",
            "Evaluasi & Performa Model",
            "Eksplorasi Data Uji",
            "Tentang & Metodologi"
        ],
        index=0
    )

    st.divider()



# ------------------------------------------------------------------------------
# MENU 1: OVERVIEW & LATAR BELAKANG
# ------------------------------------------------------------------------------
if menu == "Overview & Latar Belakang":
    st.markdown('<div class="main-title">Klasifikasi Spasial Tutupan Lahan Jawa Timur</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Visualisasi spasial berbasis citra satelit Sentinel-2 Level-2A dan algoritma Random Forest untuk pemetaan 5 kelas tutupan lahan di seluruh wilayah Provinsi Jawa Timur.</div>', unsafe_allow_html=True)
    st.markdown('<div class="badge-pill">Sentinel-2 Level-2A BOA • Random Forest Classifier</div>', unsafe_allow_html=True)

    metrics = load_metrics() or {}
    df_poly = load_polygon_test()

    # Hitung nilai metrik secara dinamis dari file data
    if df_poly is not None and not df_poly.empty:
        n_poly_test = len(df_poly)
        n_poly_benar = int((df_poly["status"] == "BENAR").sum())
        n_poly_salah = int((df_poly["status"] == "SALAH").sum())
        akurasi_poly_pct = (n_poly_benar / n_poly_test) * 100
        error_poly_pct = (n_poly_salah / n_poly_test) * 100
    else:
        n_poly_test = int(metrics.get("jumlah_poligon_test", 46))
        akurasi_poly_pct = float(metrics.get("akurasi_poligon", 0.760869)) * 100
        n_poly_benar = int(round(n_poly_test * (akurasi_poly_pct / 100)))
        n_poly_salah = n_poly_test - n_poly_benar
        error_poly_pct = 100.0 - akurasi_poly_pct

    akurasi_pixel_pct = float(metrics.get("akurasi_pixel", 0.899955)) * 100
    n_pixel_test = int(metrics.get("jumlah_pixel_test", 8996))
    n_pixel_train = int(metrics.get("jumlah_pixel_train", 27313))
    total_pixel = n_pixel_test + n_pixel_train

    report = metrics.get("classification_report", {})
    f1_weighted = float(report.get("weighted avg", {}).get("f1-score", 0.9019))

    # 4 KARTU METRIK UTAMA DENGAN DATA SEBENARNYA (BERBASIS POLIGON)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 5px solid #2ecc71;">
            <div style="color: #636e72; font-size: 0.88rem; font-weight: 600;">Akurasi Data Uji</div>
            <div style="font-size: 2.1rem; font-weight: 700; color: #2d3436; margin: 4px 0;">{akurasi_poly_pct:.1f}%</div>
            <div style="color: #27ae60; font-weight: 600; font-size: 0.85rem; margin-bottom: 4px;">▲ {n_poly_benar}/{n_poly_test} Poligon</div>
            <div style="color: #7f8c8d; font-size: 0.78rem;">Evaluasi Stratified Test Set (Random Forest)</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 5px solid #3498db;">
            <div style="color: #636e72; font-size: 0.88rem; font-weight: 600;">F1-Score Macro</div>
            <div style="font-size: 2.1rem; font-weight: 700; color: #2d3436; margin: 4px 0;">0.754</div>
            <div style="color: #2980b9; font-weight: 600; font-size: 0.85rem; margin-bottom: 4px;">● Seimbang</div>
            <div style="color: #7f8c8d; font-size: 0.78rem;">Rata-rata harmonik seluruh 5 kelas tutupan lahan</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 5px solid #9b59b6;">
            <div style="color: #636e72; font-size: 0.88rem; font-weight: 600;">Poligon Ground Truth</div>
            <div style="font-size: 2.1rem; font-weight: 700; color: #2d3436; margin: 4px 0;">250</div>
            <div style="color: #8e44ad; font-weight: 600; font-size: 0.85rem; margin-bottom: 4px;">■ 5 Kategori (50/kelas)</div>
            <div style="color: #7f8c8d; font-size: 0.78rem;">Total {total_pixel:,} piksel Sentinel-2 terekstraksi</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 5px solid #e74c3c;">
            <div style="color: #636e72; font-size: 0.88rem; font-weight: 600;">Salah Klasifikasi</div>
            <div style="font-size: 2.1rem; font-weight: 700; color: #2d3436; margin: 4px 0;">{n_poly_salah}</div>
            <div style="color: #c0392b; font-weight: 600; font-size: 0.85rem; margin-bottom: 4px;">▼ Error {error_poly_pct:.1f}%</div>
            <div style="color: #7f8c8d; font-size: 0.78rem;">{n_poly_salah} dari {n_poly_test} poligon salah voting mayoritas</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("📌 Latar Belakang & Urgensi")
        st.write("""
        Provinsi Jawa Timur memiliki luas wilayah daratan mencapai lebih dari 47.000 km² dengan bentang alam yang sangat beragam — mulai dari pesisir pantai utara & selatan, kawasan persawahan lumbung pangan nasional, pusat metropolitan, hingga pegunungan vulkanik.

        Pemantauan berkala terhadap tutupan lahan (*land cover*) sangat penting untuk:
        1. **Tata Ruang & Tata Guna Lahan**: Mengawasi perkembangan kawasan permukiman dan zona terbangun.
        2. **Perlindungan Lingkungan**: Memantau luasan hutan daratan dan ekosistem mangrove di pesisir pantai.
        3. **Ketahanan Pangan**: Mendeteksi penyusutan lahan pertanian produktif akibat alih fungsi lahan.
        4. **Mitigasi Bencana**: Memberikan gambaran spasial untuk mitigasi banjir dan tanah longsor.
        """)

        st.subheader("🔬 5 Kategori Tutupan Lahan Jawa Timur (250 Poligon)")
        kelas_info = [
            ("🔴 Pemukiman (Built-up)", "#e74c3c", "50 poligon", "Area terbangun, kawasan perumahan, gedung komersial, jalan raya, dan infrastruktur fisik."),
            ("🟡 Lahan Pertanian (Sawah)", "#f1c40f", "50 poligon", "Area persawahan irigasi, ladang budidaya, dan tanaman semusim."),
            ("🔵 Perairan (Water Body)", "#0984e3", "50 poligon", "Sungai besar, waduk, danau alami, dan badan air terbuka."),
            ("🟢 Hutan Biasa", "#27ae60", "50 poligon", "Hutan tropis daratan, perbukitan, dan kawasan vegetasi lebat alami pegunungan."),
            ("🟣 Hutan Mangrove", "#8e44ad", "50 poligon", "Ekosistem hutan pantai pasang-surut di kawasan pesisir pantai.")
        ]
        for nama, warna, jml, ket in kelas_info:
            st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 12px 16px; border-left: 5px solid {warna}; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); border: 1px solid #e1e8ed;">
                <div style="color: #1e272e; font-size: 0.95rem; font-weight: 700; margin-bottom: 4px;">{nama} <span style="color: #576574; font-size: 0.85rem; font-weight: 500;">({jml})</span></div>
                <div style="color: #2f3542; font-size: 0.88rem; line-height: 1.4;">{ket}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.subheader("🎯 Strategi Bebas Kebocoran Spasial")
        st.info("""
        **Polygon-Based Train/Test Split (80:20)**
        
        Klasifikasi spasial sangat rentan terhadap *spatial autocorrelation leakage* apabila piksel diacak secara bebas.
        
        Pada evaluasi ini:
        - Pembagian data dilakukan pada **tingkat poligon**:
          - **Train (80%):** 184 poligon (27.313 piksel)
          - **Test (20%):** 46 poligon (8.996 piksel)
        - Piksel dari satu poligon **hanya** masuk ke kelompok train ATAU kelompok test.
        - Model diuji pada wilayah poligon yang sama sekali belum pernah dilihat saat pelatihan!
        """)

        st.subheader("🛰️ Spesifikasi Citra Sentinel-2")
        st.markdown("""
        - **Sensor:** Sentinel-2 Level-2A (Surface Reflectance / BOA)
        - **Katalog:** Microsoft Planetary Computer STAC
        - **Band Spektral:** B02 (Blue), B03 (Green), B04 (Red), B08 (NIR), B8A (Narrow NIR), B11 (SWIR)
        - **Indeks Turunan:** NDVI, MNDWI, NDBI, Ratio B8A/B11
        - **Resolusi Spasial:** ~60 meter
        - **Model Machine Learning:** Random Forest (`n_estimators=200`, `class_weight='balanced'`)
        """)


# ------------------------------------------------------------------------------
# MENU 2: PETA KLASIFIKASI INTERAKTIF
# ------------------------------------------------------------------------------
elif menu == "Peta Klasifikasi Interaktif":
    st.markdown('<div class="main-title">🗺️ Visualisasi Peta Spasial Interaktif</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Eksplorasi peta evaluasi pengujian poligon dan peta tematik tutupan lahan se-Jawa Timur</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📍 Peta Evaluasi Poligon (Train vs Test)", "🌍 Peta Klasifikasi Tutupan Lahan Se-Jatim"])

    with tab1:
        st.write("""
        Peta ini menampilkan sebaran poligon digitasi se-Jawa Timur, pemisahan data uji, serta indikator poligon yang diprediksi **Benar** maupun **Salah Klasifikasi**.
        """)
        peta_gabungan = get_file_path("peta_gabungan_jatim.html")
        if peta_gabungan and peta_gabungan.exists():
            with open(peta_gabungan, "r", encoding="utf-8") as f:
                html_data = f.read()
            components.html(html_data, height=650, scrolling=True)
        else:
            st.warning("Berkas `peta_gabungan_jatim.html` tidak ditemukan di folder data.")

    with tab2:
        st.write("""
        Peta raster interaktif menampilkan hasil klasifikasi spasial model Random Forest untuk seluruh cakupan citra satelit Provinsi Jawa Timur.
        """)
        peta_raster = get_file_path("peta_klasifikasi_tutupan_lahan_jatim.html")
        if peta_raster and peta_raster.exists():
            with open(peta_raster, "r", encoding="utf-8") as f:
                html_data_raster = f.read()
            components.html(html_data_raster, height=650, scrolling=True)
        else:
            st.warning("Berkas `peta_klasifikasi_tutupan_lahan_jatim.html` tidak ditemukan di folder data.")


# ------------------------------------------------------------------------------
# MENU 3: EVALUASI & PERFORMA MODEL
# ------------------------------------------------------------------------------
elif menu == "Evaluasi & Performa Model":
    st.markdown('<div class="main-title">📈 Evaluasi & Metrik Kinerja Model</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Analisis akurasi, confusion matrix, classification report, dan feature importance</div>', unsafe_allow_html=True)

    metrics = load_metrics()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Classification Report (Tingkat Piksel)")
        if metrics and "classification_report" in metrics:
            report_dict = metrics["classification_report"]
            rows = []
            for k, v in report_dict.items():
                if isinstance(v, dict):
                    rows.append({
                        "Kelas": k,
                        "Precision": round(v.get("precision", 0), 4),
                        "Recall": round(v.get("recall", 0), 4),
                        "F1-Score": round(v.get("f1-score", 0), 4),
                        "Support": int(v.get("support", 0))
                    })
            df_report = pd.DataFrame(rows)
            st.dataframe(df_report, use_container_width=True, hide_index=True)

            st.caption("""
            **Interpretasi Metrik:**
            - **Hutan Biasa & Hutan Mangrove** memiliki Precision & Recall sangat tinggi (> 80% - 98%).
            - **Pemukiman** memperoleh Recall tinggi dengan identifikasi spektral SWIR dan NDBI yang kuat.
            - **Lahan Pertanian** memiliki tantangan kemiripan spektral musiman dengan pemukiman dan perairan saat penggenangan sawah.
            """)
        else:
            st.info("Data classification report tidak tersedia.")

    with col2:
        st.subheader("🎯 Confusion Matrix")
        cm_png = get_file_path("confusion_matrix.png")
        if cm_png and cm_png.exists():
            st.image(str(cm_png), caption="Confusion Matrix Model Random Forest pada Data Uji", use_container_width=True)
        else:
            df_cm = load_confusion_matrix_data()
            if df_cm is not None:
                st.dataframe(df_cm, use_container_width=True)

    st.divider()

    st.subheader("🌟 Feature Importance (Kepentingan Fitur Spektral)")
    col_feat1, col_feat2 = st.columns([3, 2])

    df_feat = load_feature_importance()
    with col_feat1:
        feat_png = get_file_path("feature_importance.png")
        if feat_png and feat_png.exists():
            st.image(str(feat_png), caption="Peringkat Kontribusi Fitur Spektral", use_container_width=True)
        elif df_feat is not None:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.barh(df_feat["fitur"][::-1], df_feat["persentase"][::-1], color="#2980b9")
            ax.set_xlabel("Kepentingan Fitur (%)")
            ax.set_title("Feature Importance - Random Forest")
            st.pyplot(fig)

    with col_feat2:
        if df_feat is not None:
            st.write("**Daftar Kontribusi Fitur (%):**")
            st.dataframe(df_feat[["fitur", "persentase"]], use_container_width=True, hide_index=True)
            st.info("""
            **Insight Fitur Spektral:**
            - **Ratio_B8A_B11 (14.27%)** menjadi fitur paling krusial dalam membedakan vegetasi darat vs vegetasi mangrove.
            - **MNDWI (13.44%)** dan **NDVI (12.78%)** sangat efektif membedakan badan air dan kehijauan klorofil.
            - **Band Biru (B02 - 12.63%)** berperan penting memisahkan area terbangun dan air.
            """)


# ------------------------------------------------------------------------------
# MENU 4: EKSPLORASI DATA UJI
# ------------------------------------------------------------------------------
elif menu == "Eksplorasi Data Uji":
    st.markdown('<div class="main-title">📋 Eksplorasi Data Uji & Hasil Prediksi</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Pemeriksaan detail hasil klasifikasi pada tingkat piksel dan tingkat poligon</div>', unsafe_allow_html=True)

    sub_tab1, sub_tab2 = st.tabs(["🔍 Prediksi Tingkat Piksel", "🏷️ Evaluasi Tingkat Poligon"])

    with sub_tab1:
        df_pixels = load_pixel_test_sample(nrows=10000)
        if df_pixels is not None:
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                filter_status = st.multiselect("Filter Status Prediksi:", ["BENAR", "SALAH"], default=["BENAR", "SALAH"])
            with col_f2:
                semua_kelas = sorted(df_pixels["kelas_nama"].unique())
                filter_kelas = st.multiselect("Filter Kelas Aktual:", semua_kelas, default=semua_kelas)
            with col_f3:
                max_tampil = st.slider("Jumlah Baris Ditampilkan:", min_value=10, max_value=500, value=50, step=10)

            filtered = df_pixels[
                (df_pixels["status_prediksi"].isin(filter_status)) &
                (df_pixels["kelas_nama"].isin(filter_kelas))
            ]

            st.write(f"Menampilkan **{min(len(filtered), max_tampil)}** dari total **{len(filtered):,}** piksel yang sesuai filter:")
            kolom_tampil = ["poligon_id", "kelas_nama", "kelas_prediksi", "status_prediksi", "B02", "B03", "B04", "B08", "B8A", "B11", "NDVI", "MNDWI", "NDBI", "Ratio_B8A_B11"]
            kolom_ada = [c for c in kolom_tampil if c in filtered.columns]
            st.dataframe(filtered[kolom_ada].head(max_tampil), use_container_width=True, hide_index=True)
        else:
            st.warning("File `prediksi_pixel_test.csv` tidak ditemukan.")

    with sub_tab2:
        df_poly = load_polygon_test()
        if df_poly is not None:
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                total_benar = (df_poly["status"] == "BENAR").sum()
                total_poligon = len(df_poly)
                st.metric("Total Poligon Diuji", f"{total_poligon} poligon")
            with col_p2:
                st.metric("Poligon Klasifikasi Benar", f"{total_benar} ({total_benar/total_poligon*100:.1f}%)")

            st.dataframe(df_poly, use_container_width=True, hide_index=True)
        else:
            st.warning("File `prediksi_poligon_test.csv` tidak ditemukan.")


# ------------------------------------------------------------------------------
# MENU 5: TENTANG & METODOLOGI
# ------------------------------------------------------------------------------
elif menu == "Tentang & Metodologi":
    st.markdown('<div class="main-title">ℹ️ Tentang & Metodologi Proyek</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Detail teknis alur sains data, sumber data, dan struktur repositori</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 🔄 Alur Kerja Proyek (Workflow)
    1. **Persiapan Direktori & Pustaka**: Integrasi GeoPandas, Rasterio, Scikit-learn, Folium, dan Streamlit.
    2. **Pembacaan Sampel Poligon**: 250 poligon hasil digitasi representatif di Jawa Timur (50 poligon per kelas tutupan lahan).
    3. **Akuisisi Citra Sentinel-2**: Citra Sentinel-2 Level-2A (BOA) resolusi ~60m diunduh melalui Planetary Computer STAC catalog.
    4. **Ekstraksi Fitur Spektral Multi-Pixel**: Mengekstraksi seluruh piksel di dalam poligon sampel hingga diperoleh **36.309 piksel**.
    5. **Pemisahan Train-Test Berbasis Poligon**: Mencegah kebocoran spasial (*spatial autocorrelation leakage*) dengan membagi sampel pada tingkat poligon:
       - **Train (80%):** 184 poligon (27.313 piksel)
       - **Test (20%):** 46 poligon (8.996 piksel)
    6. **Pelatihan Random Forest**: Menggunakan 200 estimator dengan pembobotan seimbang (`class_weight='balanced'`).
    7. **Evaluasi Dua Tingkat**: Evaluasi independen pada tingkat piksel (90.00% akurasi) dan voting mayoritas poligon (76.09% akurasi).
    8. **Klasifikasi Raster Penuh & Ekspor**: Menghasilkan peta spasial GeoTIFF dan peta interaktif berbasis Leaflet/Folium.
    9. **Hosting Streamlit**: Menampilkan metrik, visualisasi peta tematik, dan eksplorasi data secara terpusat.

    ---

    ### 👨‍💻 Pengembang Proyek
    - **Nama**: Irwan Dwi Mukhlisin
    - **NIM**: 240411100010
    - **Mata Kuliah**: Proyek Sains Data
    - **Repositori GitHub**: [github.com/mukhlisin24/PSD](https://github.com/mukhlisin24/PSD)
    """)
