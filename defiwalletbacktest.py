import streamlit as st
import requests

# =======================
# CONFIG
# =======================

st.set_page_config(
    page_title="DEFI WALLET BACKTEST",
    layout="wide"
)

# =======================
# GLOBAL STYLES
# =======================

st.markdown("""
<style>

/* ----- Global ----- */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #ffffff !important;
    color: #0f172a !important;
}

h1, h2, h3, h4 {
    color: #0f172a !important;
}

/* Inputs */
.stTextInput input,
.stNumberInput input {
    background-color: #f8fafc !important;
    color: #0f172a !important;
    border: 1px solid #d1d5db !important;
    border-radius: 10px;
}

/* Buttons (CTA GOLD) */
.stButton button {
    background: linear-gradient(135deg, #facc15, #f59e0b) !important;
    color: #000000 !important;
    font-weight: 700;
    border-radius: 14px;
    padding: 0.6em 1.6em;
    border: none;
    box-shadow: 0px 6px 20px rgba(250,204,21,0.35);
}

/* Cards */
.card {
    background: #ffffff;
    border-radius: 18px;
    padding: 26px;
    box-shadow: 0px 10px 30px rgba(15, 23, 42, 0.12);
    margin-bottom: 20px;
    border: 1px solid #e5e7eb;
}

/* Titles overlay like header */
.section-title {
    background: linear-gradient(135deg, #0a0f1f 0%, #1e2761 40%, #4b1c7d 100%);
    padding: 12px 18px;
    border-radius: 12px;
    color: white;
    font-weight: 700;
    margin-bottom: 15px;
    font-size: 20px;
}

.gauge-container {
    width: 100%;
    height: 25px;
    background: #e5e7eb;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 10px;
    display: flex;
}

.gauge-segment {
    height: 100%;
}

.safe { background-color: #16a34a; }
.mid { background-color: #f97316; }
.degen { background-color: #dc2626; }

</style>
""", unsafe_allow_html=True)

# =======================
# HEADER BANNER (avec boutons)
# =======================

st.markdown("""
<style>
.deFi-banner {
    background: linear-gradient(135deg, #0a0f1f 0%, #1e2761 40%, #4b1c7d 100%);
    padding: 25px 30px;
    border-radius: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0px 4px 18px rgba(0,0,0,0.45);
    margin-bottom: 25px;
}

.deFi-title-text {
    font-size: 36px;
    font-weight: 700;
    color: white !important;
}

.deFi-buttons a {
    color: white;
    font-size: 15px;
    font-weight: 600;
    text-decoration: none;
    padding: 8px 14px;
    border-radius: 12px;
    margin-left: 8px;
}

.krystal-btn { background-color: #06b6d4; }
.plusvalue-btn { background-color: #10b981; }
.telegram-btn { background-color: #6c5ce7; }
.formation-btn { background-color: #f59e0b; }
</style>

<div class="deFi-banner">
    <div class="deFi-title-text">DEFI WALLET BACKTEST</div>
    <div class="deFi-buttons">
        <a href="https://defi.krystal.app/referral?r=3JwR8YRQCRJT" target="_blank" class="krystal-btn">Krystal</a>
        <a href="https://plusvalueimposable.streamlit.app/" target="_blank" class="plusvalue-btn">Plus-value</a>
        <a href="https://t.me/Pigeonchanceux" target="_blank" class="telegram-btn">Telegram</a>
        <a href="https://shorturl.at/X3sYt" target="_blank" class="formation-btn">Formation</a>
    </div>
</div>
""", unsafe_allow_html=True)

# =======================
# DISCLAIMER
# =======================

if "show_disclaimer" not in st.session_state:
    st.session_state.show_disclaimer = True

if st.session_state.show_disclaimer:
    st.markdown("""
    <div style="
        background-color: #fff3cd;
        border-left: 6px solid #ffca2c;
        padding: 15px 20px;
        border-radius: 8px;
        color: #000;
        margin-bottom: 25px;
        font-size: 15px;
    ">
    <b>⚠️ DISCLAIMER IMPORTANT</b><br><br>
    L’accès au backtest est exclusivement réservé aux membres de la Team Élite de la chaîne KBOUR Crypto.
    Le code d’accès est disponible dans le canal privé <b>« DEFI Académie »</b>.
    <br><br>
    </div>
    """, unsafe_allow_html=True)

# =======================
# AUTHENTIFICATION
# =======================

SECRET_CODE = "WALLET"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.text_input("Code d'accès", key="secret_code", type="password")
    if st.button("Valider"):
        if st.session_state.secret_code == SECRET_CODE:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Code incorrect")
    st.stop()

# =======================
# STRATEGIES
# =======================

STRATEGIES = {
    "SAFE": {
        "description": "Préservation du capital",
        "targets": {"BTC NATIF": 0.50, "lending": 0.70, "borrowing": 0.05, "hodl": 0.15, "liquidity_pool": 0.10},
        "threshold": 0.05
    },
    "MID": {
        "description": "Rendement équilibré",
        "targets": {"BTC NATIF": 0.30, "lending": 0.50, "borrowing": 0.15, "hodl": 0.10, "liquidity_pool": 0.25},
        "threshold": 0.05
    },
    "DEGEN": {
        "description": "Rendement agressif et risques très élevés",
        "targets": {"BTC NATIF": 0.10, "lending": 0.25, "borrowing": 0.20, "hodl": 0.05, "liquidity_pool": 0.50},
        "threshold": 0.10
    }
}

ASSETS = ["BTC NATIF", "lending", "borrowing", "hodl", "liquidity_pool"]

def normalize(portfolio):
    total = sum(portfolio[a] for a in ASSETS)
    return {a: portfolio[a]/total if total > 0 else 0 for a in ASSETS}

def detect_actions(composite_targets, current, threshold):
    actions = []
    for asset in ASSETS:
        delta = current[asset] - composite_targets[asset]
        if delta > threshold:
            actions.append(f"REDUIRE {asset.upper()} de {delta:.1%}")
        elif delta < -threshold:
            actions.append(f"AUGMENTER {asset.upper()} de {-delta:.1%}")
    return actions

# =======================
# UI PRINCIPAL
# =======================

left, right = st.columns([1,2])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Valeurs du wallet</div>', unsafe_allow_html=True)

    portfolio = {}
    for asset in ASSETS:
        portfolio[asset] = st.number_input(asset.upper(), min_value=0.0, value=0.0, step=100.0, format="%.2f")

    st.markdown('<div class="section-title">Répartition SAFE / MID / DEGEN (cible)</div>', unsafe_allow_html=True)
    safe_pct = st.slider("SAFE", 0, 100, 40)
    mid_pct = st.slider("MID", 0, 100, 60)
    degen_pct = st.slider("DEGEN", 0, 100, 0)

    total_pct = safe_pct + mid_pct + degen_pct
    if total_pct > 0:
        safe_pct /= total_pct
        mid_pct /= total_pct
        degen_pct /= total_pct

    analyze = st.button("Analyser")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    if analyze:
        current = normalize(portfolio)

        composite_targets = {
            a:
            STRATEGIES["SAFE"]["targets"][a]*safe_pct +
            STRATEGIES["MID"]["targets"][a]*mid_pct +
            STRATEGIES["DEGEN"]["targets"][a]*degen_pct
            for a in ASSETS
        }

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Répartition du portefeuille</div>', unsafe_allow_html=True)

        total_exposure = sum(portfolio[a] for a in ASSETS)
        st.write(f"Exposition totale : ${total_exposure:,.2f}")

        st.table({
            "Catégorie": [a.upper() for a in ASSETS],
            "Actuel": [f"{current[a]:.1%}" for a in ASSETS],
            "Cible (profil sélectionné)": [f"{composite_targets[a]:.1%}" for a in ASSETS]
        })

        st.markdown('</div>', unsafe_allow_html=True)
