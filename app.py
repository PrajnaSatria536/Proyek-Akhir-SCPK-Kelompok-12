import streamlit as st
import pandas as pd
import numpy as np

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Klasifikasi Tanaman – Weighted Product",
    page_icon="🌱",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3 { font-family: 'Lora', serif; }

.stApp {
    background: linear-gradient(160deg, #fafdf7 0%, #f0f7eb 40%, #e8f5e0 100%);
    min-height: 100vh;
}

.hero-section {
    background: linear-gradient(135deg, #1a4731 0%, #2d6a4f 50%, #40916c 100%);
    border-radius: 24px;
    padding: 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(116,198,130,0.2) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-section::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: 20%;
    width: 250px;
    height: 250px;
    background: radial-gradient(circle, rgba(180,240,150,0.1) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-title {
    font-family: 'Lora', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: white;
    margin: 0 0 8px 0;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.75);
    margin: 0;
    letter-spacing: 0.3px;
}

.hero-badge {
    display: inline-block;
    background: rgba(116,198,130,0.25);
    border: 1px solid rgba(116,198,130,0.4);
    color: #b7e4c7;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 16px;
}

.card {
    background: white;
    border-radius: 20px;
    padding: 28px 32px;
    box-shadow: 0 2px 20px rgba(45,106,79,0.08);
    border: 1px solid rgba(45,106,79,0.06);
    margin-bottom: 20px;
    position: relative;
}

.card-title {
    font-family: 'Lora', serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: #1a4731;
    margin: 0 0 6px 0;
}

.card-desc {
    font-size: 0.83rem;
    color: #6b8f71;
    margin: 0 0 24px 0;
}

.section-divider {
    border: none;
    border-top: 1.5px solid #e8f0ea;
    margin: 24px 0;
}

.weight-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
    padding: 8px 12px;
    border-radius: 10px;
    background: #f6fbf7;
    border: 1px solid #d8eedd;
}

.weight-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #2d6a4f;
    min-width: 160px;
}

.weight-type {
    font-size: 0.72rem;
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: 600;
}

.benefit-badge {
    background: #d1fae5;
    color: #065f46;
}

.cost-badge {
    background: #fee2e2;
    color: #991b1b;
}

.result-hero {
    background: linear-gradient(135deg, #1a4731 0%, #2d6a4f 60%, #52b788 100%);
    border-radius: 20px;
    padding: 36px;
    text-align: center;
    color: white;
    box-shadow: 0 12px 40px rgba(26,71,49,0.35);
    position: relative;
    overflow: hidden;
    margin-bottom: 20px;
}

.result-hero::before {
    content: '🌿';
    position: absolute;
    top: -10px;
    right: 20px;
    font-size: 80px;
    opacity: 0.12;
    transform: rotate(15deg);
}

.result-plant-name {
    font-family: 'Lora', serif;
    font-size: 2.6rem;
    font-weight: 700;
    margin: 8px 0 4px;
    letter-spacing: 0.5px;
}

.result-label {
    font-size: 0.8rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.7;
    margin-bottom: 4px;
}

.result-score {
    font-size: 1.1rem;
    font-weight: 600;
    background: rgba(255,255,255,0.15);
    display: inline-block;
    padding: 6px 20px;
    border-radius: 30px;
    margin-top: 12px;
}

.rank-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 8px;
    border: 1px solid #e8f0ea;
    background: white;
    transition: all 0.2s;
}

.rank-item.rank-1 {
    background: linear-gradient(90deg, #f0fdf4, #dcfce7);
    border-color: #86efac;
}

.rank-number {
    font-family: 'Lora', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #2d6a4f;
    min-width: 32px;
    text-align: center;
}

.rank-name {
    font-weight: 600;
    color: #1a4731;
    flex: 1;
    font-size: 0.95rem;
}

.rank-score {
    font-size: 0.82rem;
    color: #6b8f71;
    font-weight: 600;
}

.rank-bar-wrap {
    flex: 1;
    height: 6px;
    background: #e8f0ea;
    border-radius: 3px;
    overflow: hidden;
}

.rank-bar {
    height: 100%;
    background: linear-gradient(90deg, #52b788, #2d6a4f);
    border-radius: 3px;
}

.metric-row {
    display: flex;
    gap: 12px;
    margin-top: 16px;
}

.metric-tile {
    flex: 1;
    background: #f6fbf7;
    border: 1px solid #d8eedd;
    border-radius: 14px;
    padding: 14px 16px;
    text-align: center;
}

.metric-tile .val {
    font-family: 'Lora', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #1a4731;
}

.metric-tile .lbl {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #52b788;
    font-weight: 600;
    margin-top: 2px;
}

.step-box {
    background: #f6fbf7;
    border-left: 4px solid #52b788;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    margin-bottom: 12px;
}

.step-title {
    font-weight: 700;
    color: #2d6a4f;
    font-size: 0.88rem;
    margin-bottom: 4px;
}

.step-desc {
    font-size: 0.82rem;
    color: #4a7c59;
}

.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 12px;
}

.info-chip {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.8rem;
    color: #166534;
}

.info-chip strong {
    display: block;
    font-weight: 700;
    margin-bottom: 2px;
}

.plant-icon {
    font-size: 3.5rem;
    margin-bottom: 8px;
    display: block;
}

.stButton > button {
    background: linear-gradient(135deg, #2d6a4f, #40916c) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 4px 16px rgba(45,106,79,0.35) !important;
    width: 100%;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(45,106,79,0.45) !important;
}

div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label {
    font-weight: 600 !important;
    color: #2d6a4f !important;
    font-size: 0.88rem !important;
}

.stDataFrame { border-radius: 14px; overflow: hidden; }

/* ── Tab styling – hijau tua ── */
div[data-testid="stTabs"] [role="tablist"] {
    background: #1a4731 !important;
    border-radius: 14px 14px 0 0 !important;
    padding: 6px 8px 0 8px !important;
    gap: 4px !important;
    border-bottom: none !important;
}

div[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: rgba(183, 228, 199, 0.75) !important;
    border: none !important;
    border-radius: 10px 10px 0 0 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 8px 18px !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stTabs"] [role="tab"]:hover {
    background: rgba(82,183,136,0.2) !important;
    color: #b7e4c7 !important;
}

div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #2d6a4f !important;
    color: white !important;
    border-bottom: 3px solid #52b788 !important;
}

div[data-testid="stTabs"] [role="tabpanel"] {
    background: white !important;
    border: 2px solid #1a4731 !important;
    border-radius: 0 0 14px 14px !important;
    padding: 24px !important;
}

/* ── Tabel panduan pH – hijau tua ── */
div[data-testid="stTabs"] table {
    width: 100% !important;
    border-collapse: collapse !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    font-size: 0.88rem !important;
}

div[data-testid="stTabs"] thead tr {
    background: #1a4731 !important;
    color: white !important;
}

div[data-testid="stTabs"] thead th {
    padding: 12px 16px !important;
    text-align: left !important;
    font-weight: 700 !important;
    letter-spacing: 0.4px !important;
    border: none !important;
}

div[data-testid="stTabs"] tbody tr {
    border-bottom: 1px solid #d8eedd !important;
    transition: background 0.15s ease !important;
}

div[data-testid="stTabs"] tbody tr:nth-child(even) {
    background: #f0fdf4 !important;
}

div[data-testid="stTabs"] tbody tr:hover {
    background: #d1fae5 !important;
}

div[data-testid="stTabs"] tbody td {
    padding: 10px 16px !important;
    color: #1a4731 !important;
    border: none !important;
}

div[data-testid="stTabs"] tbody td:first-child {
    font-weight: 700 !important;
    color: #2d6a4f !important;
}

/* ── Caption di tab3 ── */
div[data-testid="stTabs"] .stCaption {
    color: #4a7c59 !important;
    font-size: 0.8rem !important;
    margin-top: 12px !important;
}

/* ── result-hero: merah saat hover ── */
.result-hero {
    transition: background 0.3s ease, box-shadow 0.3s ease !important;
}

.result-hero:hover {
    background: linear-gradient(135deg, #7f1d1d 0%, #b91c1c 50%, #ef4444 100%) !important;
    box-shadow: 0 16px 48px rgba(185,28,28,0.45) !important;
}

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)



PLANT_INFO = {
    "Rice":         {"icon": "🌾", "desc": "Tanaman pangan utama, tumbuh optimal di lahan basah dengan pH netral."},
    "Singkong":     {"icon": "🥔", "desc": "Tanaman umbi tahan kering, adaptif di tanah agak asam."},
    "maize":       {"icon": "🌽", "desc": "Serealia serbaguna, cocok di lahan kering dengan sinar matahari penuh."},
    "Tomat":        {"icon": "🍅", "desc": "Sayuran buah bernilai ekonomi tinggi, butuh drainase baik."},
    "Kentang":      {"icon": "🥔", "desc": "Umbi pegunungan yang menyukai suhu dingin dan tanah gembur."},
    "Kedelai":      {"icon": "🌿", "desc": "Sumber protein nabati, tumbuh baik di pH agak basa."},
    "coffee":         {"icon": "☕", "desc": "Tanaman perkebunan bernilai tinggi, optimal di lereng pegunungan."},
    "Tebu":         {"icon": "🎋", "desc": "Sumber gula utama, butuh sinar matahari dan curah hujan cukup."},
    "Cabai":        {"icon": "🌶️", "desc": "Komoditas hortikultura penting, butuh kondisi kering dengan nutrisi tinggi."},
    "coconut":       {"icon": "🥥", "desc": "Tanaman pantai tropis, tahan kelembaban tinggi dan curah hujan lebat."},
    "chickpea": {"icon": "🥜", "desc": "Legum penghasil minyak, adaptif di tanah pH agak basa dengan drainase baik."},
    "kidneybeans": {"icon": "🥜", "desc": "Legum penghasil minyak, adaptif di tanah pH agak basa dengan drainase baik."},
    "pigeonbeans": {"icon": "🥜", "desc": "Legum penghasil minyak, adaptif di tanah pH agak basa dengan drainase baik."},
    "mothbeans": {"icon": "🥜", "desc": "Legum penghasil minyak, adaptif di tanah pH agak basa dengan drainase baik."},
}

KRITERIA = [
    ("ph_tanah",    "pH Tanah",          "benefit",  5),
    ("curah_hujan", "Curah Hujan (mm)",  "benefit",  4),
    ("suhu",        "Suhu (°C)",         "benefit",  3),
    ("kelembaban",  "Kelembaban (%)",    "benefit",  3),
    ("nitrogen",    "Kadar Nitrogen (N)","benefit",  4),
]

@st.cache_data
def load_data():
    df = pd.read_csv("tanaman.csv")
    return df


def weighted_product(df, input_vals, bobot_raw):
    """
    Algoritma Weighted Product (WP) berbasis KEDEKATAN INPUT ke profil tanaman.

    Pendekatan:
    - Untuk setiap tanaman, hitung rasio kemiripan per kriteria:
        rasio_j = min(input_j, profil_j) / max(input_j, profil_j)
      Nilai rasio = 1.0 berarti sempurna cocok, mendekati 0 berarti jauh.
    - Skor WP: S_i = prod( rasio_j ^ w_j )
    - Ranking: tanaman dengan S_i tertinggi paling cocok dengan input user.

    Dengan cara ini ranking BERUBAH sesuai input — bukan ranking statis
    berdasarkan nilai absolut profil yang selalu menguntungkan tanaman
    dengan nilai besar (Kelapa/Kopi karena curah hujan tinggi).
    """
    kolom = [k[0] for k in KRITERIA]

    total_bobot = sum(bobot_raw)
    bobot = [b / total_bobot for b in bobot_raw]

    # Profil rata-rata per tanaman dari dataset
    profil = df.groupby("tanaman")[kolom].mean().reset_index()

    # Step 2: Hitung skor kemiripan tiap tanaman terhadap input user
    input_arr = np.array(input_vals, dtype=float)
    S = []
    for _, row in profil.iterrows():
        s = 1.0
        for j, (col, _label, tp, _default) in enumerate(KRITERIA):
            inp = input_arr[j]
            ref = float(row[col])
            # Rasio kemiripan: selalu antara 0–1, nilai 1 = identik
            if max(inp, ref) > 0:
                rasio = min(inp, ref) / max(inp, ref)
            else:
                rasio = 1.0
            # Semua kriteria di sini adalah benefit (semakin mirip semakin baik)
            # Untuk kriteria cost, balik bobotnya: rasio^(-w)
            w = bobot[j] if tp == "benefit" else -bobot[j]
            s *= (rasio ** w)
        S.append(s)

    profil["S"] = S
    total_S = sum(S)

    # Step 3: Vektor V (proporsi relatif)
    profil["V"] = profil["S"] / total_S if total_S > 0 else 0

    # Ranking dari V tertinggi
    hasil = profil.sort_values("V", ascending=False).reset_index(drop=True)
    hasil["Rank"] = hasil.index + 1

    # user_V: skor sempurna (input dibanding dirinya sendiri = 1.0^w = 1.0)
    user_V = 1.0

    return hasil, bobot, user_V


def get_recommendation(hasil, input_vals):
    """Cari tanaman yang paling cocok berdasarkan jarak ke profil rata-rata."""
    kolom = [k[0] for k in KRITERIA]
    df = load_data()
    profil = df.groupby("tanaman")[kolom].mean()

    # Hitung jarak Euclidean ternormalisasi
    input_arr = np.array(input_vals, dtype=float)
    min_dist = float("inf")
    best = hasil.iloc[0]["tanaman"]

    for tanaman, row in profil.iterrows():
        dist = np.linalg.norm(input_arr - row.values)
        if dist < min_dist:
            min_dist = dist
            best = tanaman

    return best


# ═══════════════════════════════════════════════════════════════
# LAYOUT
# ═══════════════════════════════════════════════════════════════

# ── Hero Header ──────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">🌿 Sistem Pendukung Keputusan Pertanian</div>
    <p class="hero-title">Klasifikasi Tanaman<br>Berdasarkan pH Tanah</p>
    <p class="hero-subtitle">Menggunakan Algoritma <strong style="color:#b7e4c7;">Weighted Product (WP)</strong>
    — analisis multi-kriteria untuk rekomendasi tanaman yang tepat dan akurat.</p>
</div>
""", unsafe_allow_html=True)

# ── Main Layout ───────────────────────────────────────────────
col_kiri, col_kanan = st.columns([1.1, 0.9], gap="large")

with col_kiri:

    # ─ Kartu Input Kriteria ─
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">📋 Parameter Input Lahan</p>', unsafe_allow_html=True)
    st.markdown('<p class="card-desc">Masukkan kondisi lahan Anda untuk mendapatkan rekomendasi tanaman terbaik.</p>', unsafe_allow_html=True)

    ph     = st.number_input("🌡️ pH Tanah",           min_value=3.0, max_value=10.0, value=6.5, step=0.1,
                              help="Tingkat keasaman tanah (3 = sangat asam, 7 = netral, 10 = sangat basa)")
    curah  = st.number_input("🌧️ Curah Hujan (mm/tahun)", min_value=100, max_value=4000, value=1200, step=50,
                              help="Total curah hujan tahunan di lokasi lahan")
    suhu   = st.number_input("🌡️ Suhu Rata-rata (°C)",  min_value=10.0, max_value=40.0, value=27.0, step=0.5,
                              help="Suhu udara rata-rata harian di lokasi lahan")
    lembab = st.number_input("💧 Kelembaban (%)",        min_value=20, max_value=100, value=65, step=1,
                              help="Persentase kelembaban udara rata-rata")
    nitro  = st.number_input("🧪 Kadar Nitrogen (N)",   min_value=10, max_value=200, value=80, step=5,
                              help="Kandungan nitrogen tanah dalam ppm")
    st.markdown('</div>', unsafe_allow_html=True)

    # ─ Kartu Bobot Kriteria ─
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">⚖️ Bobot Kriteria (WP)</p>', unsafe_allow_html=True)
    st.markdown('<p class="card-desc">Atur tingkat kepentingan setiap kriteria (1–10). Bobot akan dinormalisasi otomatis.</p>', unsafe_allow_html=True)

    bobot_vals = []
    # ── FIX: unpack 4 elemen tuple dengan benar ──
    for col_key, label, tipe, default in KRITERIA:
        badge_class = "benefit-badge" if tipe == "benefit" else "cost-badge"
        badge_text  = "Benefit" if tipe == "benefit" else "Cost"
        st.markdown(f"""
        <div class="weight-row">
            <span class="weight-label">{label}</span>
            <span class="weight-type {badge_class}">{badge_text}</span>
        </div>
        """, unsafe_allow_html=True)
        w = st.slider(f"Bobot – {label}", min_value=1, max_value=10, value=default,
                      label_visibility="collapsed", key=f"w_{col_key}")
        bobot_vals.append(w)

    st.markdown('</div>', unsafe_allow_html=True)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        hitung_btn = st.button("🔍 Hitung & Rekomendasikan", use_container_width=True)
    with col_b2:
        reset_btn = st.button("🔄 Reset Input", use_container_width=True)

with col_kanan:

    if hitung_btn:
        df = load_data()
        input_vals = [ph, curah, suhu, lembab, nitro]

        hasil, bobot_norm, user_v = weighted_product(df, input_vals, bobot_vals)
        terbaik = hasil.iloc[0]["tanaman"]
        skor_terbaik = hasil.iloc[0]["V"]
        info = PLANT_INFO.get(terbaik, {"icon": "🌱", "desc": ""})

        # ─ Hasil Utama ─
        st.markdown(f"""
        <div class="result-hero">
            <div class="result-label">Rekomendasi Terbaik</div>
            <span class="plant-icon">{info["icon"]}</span>
            <div class="result-plant-name">{terbaik}</div>
            <div style="font-size:0.85rem; opacity:0.8; margin:6px 0;">{info["desc"]}</div>
            <div class="result-score">Skor WP: {skor_terbaik:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

        # ─ Ringkasan Input ─
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">📊 Ringkasan Parameter</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-grid">
            <div class="info-chip"><strong>pH Tanah</strong>{ph}</div>
            <div class="info-chip"><strong>Curah Hujan</strong>{curah} mm/thn</div>
            <div class="info-chip"><strong>Suhu</strong>{suhu}°C</div>
            <div class="info-chip"><strong>Kelembaban</strong>{lembab}%</div>
            <div class="info-chip"><strong>Nitrogen</strong>{nitro} ppm</div>
            <div class="info-chip"><strong>Alternatif Dievaluasi</strong>{len(hasil)} tanaman</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ─ Ranking Semua Tanaman ─
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">🏆 Ranking Seluruh Tanaman</p>', unsafe_allow_html=True)
        max_v = hasil["V"].max()
        for _, row in hasil.iterrows():
            rank = int(row["Rank"])
            name = row["tanaman"]
            v    = row["V"]
            pct  = (v / max_v * 100) if max_v > 0 else 0
            icon = PLANT_INFO.get(name, {}).get("icon", "🌱")
            cls  = "rank-item rank-1" if rank == 1 else "rank-item"
            st.markdown(f"""
            <div class="{cls}">
                <div class="rank-number">#{rank}</div>
                <div style="font-size:1.4rem;">{icon}</div>
                <div class="rank-name">{name}</div>
                <div class="rank-bar-wrap">
                    <div class="rank-bar" style="width:{pct:.1f}%;"></div>
                </div>
                <div class="rank-score">{v:.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif reset_btn:
        st.info("✅ Input telah direset. Silakan masukkan nilai baru.")

    else:
        # Placeholder saat belum dihitung
        st.markdown("""
        <div style="background:white; border-radius:20px; padding:48px 36px; text-align:center;
                    box-shadow:0 2px 20px rgba(45,106,79,0.08); border:1px solid rgba(45,106,79,0.06);">
            <div style="font-size:4.5rem; margin-bottom:16px;">🌱</div>
            <h3 style="color:#1a4731; font-family:'Lora',serif; margin-bottom:8px;">Siap Menganalisis</h3>
            <p style="color:#6b8f71; font-size:0.9rem; margin:0;">
                Masukkan data kondisi lahan di panel kiri,<br>lalu klik <strong>Hitung & Rekomendasikan</strong>
                untuk melihat<br>hasil klasifikasi menggunakan metode WP.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PENJELASAN ALGORITMA WP + DATASET
# ═══════════════════════════════════════════════════════════════
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📐 Cara Kerja Algoritma WP", "📊 Dataset Tanaman", "📌 Panduan pH Tanah"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="step-box">
            <div class="step-title">Langkah 1 – Normalisasi Bobot</div>
            <div class="step-desc">Bobot setiap kriteria dibagi dengan total bobot: <em>w_j = W_j / ΣW</em>. Ini memastikan total bobot = 1.</div>
        </div>
        <div class="step-box">
            <div class="step-title">Langkah 2 – Hitung Vektor S</div>
            <div class="step-desc">Setiap alternatif dihitung: <em>S_i = ∏ (x_ij ^ w_j)</em> untuk kriteria benefit, dan <em>x_ij ^ -w_j</em> untuk kriteria cost.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="step-box">
            <div class="step-title">Langkah 3 – Hitung Vektor V</div>
            <div class="step-desc">Preferensi relatif: <em>V_i = S_i / ΣS</em>. Nilai V lebih besar berarti alternatif lebih baik.</div>
        </div>
        <div class="step-box">
            <div class="step-title">Langkah 4 – Ranking</div>
            <div class="step-desc">Alternatif diurutkan dari nilai V tertinggi. Tanaman dengan V tertinggi adalah rekomendasi terbaik.</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:16px 20px; font-size:0.85rem; color:#166534; margin-top:8px;">
    💡 <strong>Keunggulan WP:</strong> Metode Weighted Product memberikan bobot eksponensial pada setiap kriteria sehingga lebih sensitif terhadap perbedaan nilai dibanding metode additive biasa. Hasilnya lebih diskriminatif dan akurat untuk SPK pertanian.
    </div>
    """, unsafe_allow_html=True)

with tab2:
    df_show = load_data()
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1: st.metric("Total Data", f"{len(df_show)} baris")
    with col_i2: st.metric("Jenis Tanaman", df_show["tanaman"].nunique())
    with col_i3: st.metric("Jumlah Kriteria", 5)
    st.dataframe(df_show, use_container_width=True, height=320)
    dist = df_show["tanaman"].value_counts().reset_index()
    dist.columns = ["Tanaman", "Jumlah Data"]
    st.bar_chart(dist.set_index("Tanaman"))

with tab3:
    st.markdown("""
    <table>
        <thead>
            <tr>
                <th>Rentang pH</th>
                <th>Klasifikasi</th>
                <th>Tanaman yang Cocok</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>&lt; 5.5</td><td>Sangat Asam</td><td>Singkong, Tebu</td></tr>
            <tr><td>5.5 &ndash; 6.0</td><td>Asam</td><td>Kentang, Kopi, Kelapa</td></tr>
            <tr><td>6.0 &ndash; 6.5</td><td>Agak Asam</td><td>Padi, Jagung, Cabai, Singkong</td></tr>
            <tr><td>6.5 &ndash; 7.0</td><td>Netral Cenderung Asam</td><td>Padi, Jagung, Tomat, Kopi</td></tr>
            <tr><td>7.0 &ndash; 7.5</td><td>Netral</td><td>Jagung, Tomat, Kedelai</td></tr>
            <tr><td>7.5 &ndash; 8.0</td><td>Agak Basa</td><td>Kedelai, Kacang Tanah</td></tr>
            <tr><td>&gt; 8.0</td><td>Basa</td><td>Kedelai, Kacang Tanah</td></tr>
        </tbody>
    </table>
    <p style="color:#4a7c59; font-size:0.8rem; margin-top:14px;">
        ⚠️ <strong>Catatan:</strong> pH tanah bukan satu-satunya faktor &mdash; curah hujan, suhu, kelembaban, dan kandungan nitrogen juga sangat berpengaruh.
    </p>
    """, unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center; color:#aaa; font-size:0.78rem; margin-top:24px;'>"
    "Sistem Klasifikasi Tanaman · Algoritma Weighted Product (WP) · Projek Akhir</p>",
    unsafe_allow_html=True
)
