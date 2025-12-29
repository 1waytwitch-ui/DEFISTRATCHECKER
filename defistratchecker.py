import streamlit as st
import requests
import datetime
import yfinance as yf

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
.stTextInput input, .stNumberInput input {
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

/* Tables */
table {
    background-color: #ffffff !important;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
}
thead tr th {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
}
tbody tr td {
    color: #0f172a !important;
}

</style>
""", unsafe_allow_html=True)

# =======================
# HEADER BANNER
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
    Cet outil est réservé aux membres de la Team Élite KBOUR Crypto.
    Il ne constitue en aucun cas un conseil en investissement.
    </div>
    """, unsafe_allow_html=True)

# =======================
# AUTHENTIFICATION
# =======================

SECRET_CODE = "WALLET"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    st.markdown("""
    <style>
    .login-card {
        background: linear-gradient(135deg, #0a0f1f 0%, #1e2761 40%, #4b1c7d 100%);
        padding: 28px 30px;
        border-radius: 18px;
        max-width: 420px;
        margin: 3rem auto;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0px 4px 18px rgba(0,0,0,0.45);
        text-align: center;
    }
    .login-title { font-size: 28px; font-weight: 700; color: white; }
    .login-subtitle { font-size: 14px; color: #d1d5db; margin-bottom: 18px; }
    </style>

    <div class="login-card">
        <div class="login-title">Accès sécurisé</div>
        <div class="login-subtitle">
            Réservé aux membres de la <b>Team Élite</b><br>
            Code disponible dans <b>DEFI Académie</b>
        </div>
        <a href="https://www.youtube.com/channel/UCZL_vS9bsLI4maA4Oja9zyg/join"
           target="_blank"
           style="background:#facc15;color:#111827;
           padding:10px 18px;border-radius:14px;
           font-weight:700;display:inline-block;">
           Rejoindre la Team Élite
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.text_input("Code d'accès", key="secret_code", type="password")
    if st.button("Valider", use_container_width=True):
        if st.session_state.secret_code == SECRET_CODE:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Code incorrect")

    st.stop()

# =======================
# DEFI STRATEGY ANALYZER
# =======================

STRATEGIES = {
    "SAFE": {
        "description": "Préservation du capital",
        "targets": {"hodl": 0.45, "lending": 0.45, "liquidity_pool": 0.10, "borrowing": 0.00},
        "threshold": 0.05
    },
    "MID": {
        "description": "Rendement équilibré, levier modéré",
        "targets": {"hodl": 0.20, "lending": 0.45, "liquidity_pool": 0.25, "borrowing": 0.10},
        "threshold": 0.05
    },
    "DEGEN": {
        "description": "Rendement agressif, levier élevé",
        "targets": {"hodl": 0.05, "lending": 0.35, "liquidity_pool": 0.40, "borrowing": 0.20},
        "threshold": 0.10
    }
}

ASSETS = ["hodl", "lending", "liquidity_pool", "borrowing"]

def get_portfolio_from_evm(address):
    if not address or not address.startswith("0x"):
        return None
    seed = int(address[-4:], 16) % 100
    hodl = 2500 + seed * 10
    lending = 3500 + seed * 15
    lp = 2500 + seed * 10
    borrowing = 1000 + seed * 5
    return {
        "hodl": hodl,
        "lending": lending,
        "liquidity_pool": lp,
        "borrowing": borrowing,
        "total_exposure": hodl + lending + lp
    }

def normalize(p):
    t = p["total_exposure"]
    return {k: p[k] / t for k in ASSETS}

def detect_actions(strategy, current):
    actions = []
    for asset in ASSETS:
        delta = current[asset] - strategy["targets"][asset]
        if delta > strategy["threshold"]:
            actions.append(f"REDUIRE {asset.upper()} de {delta:.1%}")
        elif delta < -strategy["threshold"]:
            actions.append(f"AUGMENTER {asset.upper()} de {-delta:.1%}")
    return actions

left, right = st.columns([1, 2])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    address = st.text_input("Adresse EVM", placeholder="0x...")
    strategy_choice = st.radio("Profil de risque", list(STRATEGIES.keys()), horizontal=True)
    strategy = STRATEGIES[strategy_choice]
    st.info(strategy["description"])
    analyze = st.button("Analyser")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    if analyze:
        p = get_portfolio_from_evm(address)
        if not p:
            st.error("Adresse invalide")
            st.stop()
        current = normalize(p)
        actions = detect_actions(strategy, current)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Répartition du portefeuille")
        st.write(f"Exposition totale : ${p['total_exposure']:,.0f}")
        st.table({
            "Catégorie": ["HODL", "LENDING", "LP", "BORROWING"],
            "Actuel": [f"{current[a]:.1%}" for a in ASSETS],
            "Cible": [f"{strategy['targets'][a]:.1%}" for a in ASSETS],
        })
        st.subheader("Actions recommandées")
        if actions:
            for a in actions:
                st.warning(a)
        else:
            st.success("Portefeuille aligné avec la stratégie")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center;opacity:0.5;margin-top:30px;">© KBOUR Crypto • LP Backtest</div>', unsafe_allow_html=True)
