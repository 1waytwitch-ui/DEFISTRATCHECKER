import streamlit as st
import requests
import pandas as pd

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
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background-color: #ffffff !important;
    color: #0f172a !important;
}
.card {
    background: #ffffff;
    border-radius: 18px;
    padding: 26px;
    box-shadow: 0px 10px 30px rgba(15, 23, 42, 0.12);
    margin-bottom: 20px;
    border: 1px solid #e5e7eb;
}
.section-banner {
    background: linear-gradient(135deg, #0a0f1f 0%, #1e2761 40%, #4b1c7d 100%);
    padding: 16px 24px;
    border-radius: 16px;
    margin: 35px 0 20px 0;
}
.section-title {
    font-size: 24px;
    font-weight: 700;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =======================
# HEADER
# =======================

st.markdown("""
<div style="
    background: linear-gradient(135deg, #0a0f1f 0%, #1e2761 40%, #4b1c7d 100%);
    padding: 25px 30px;
    border-radius: 18px;
    margin-bottom: 25px;
    color:white;
    font-size:36px;
    font-weight:700;">
    DEFI WALLET BACKTEST
</div>
""", unsafe_allow_html=True)

# =======================
# SECTION TITLE FUNCTION
# =======================

def section_title(title):
    st.markdown(f"""
    <div class="section-banner">
        <div class="section-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)

# =======================
# STRATEGIES
# =======================

STRATEGIES = {
    "SAFE": {
        "description": "Préservation du capital",
        "targets": {"hodl": 0.15, "lending": 0.70, "liquidity_pool": 0.10, "borrowing": 0.05},
        "threshold": 0.05
    },
    "MID": {
        "description": "Rendement équilibré",
        "targets": {"hodl": 0.10, "lending": 0.50, "liquidity_pool": 0.25, "borrowing": 0.15},
        "threshold": 0.05
    },
    "DEGEN": {
        "description": "Rendement agressif et risques élevés",
        "targets": {"hodl": 0.05, "lending": 0.25, "liquidity_pool": 0.50, "borrowing": 0.20},
        "threshold": 0.10
    }
}

ASSETS = ["hodl", "lending", "liquidity_pool", "borrowing"]

def normalize(portfolio):
    total = sum(portfolio[a] for a in ASSETS)
    return {a: portfolio[a]/total if total > 0 else 0 for a in ASSETS}

def detect_actions(strategy, current):
    actions = []
    for asset in ASSETS:
        delta = current[asset] - strategy["targets"][asset]
        if delta > strategy["threshold"]:
            actions.append(f"REDUIRE {asset.upper()} de {delta:.1%}")
        elif delta < -strategy["threshold"]:
            actions.append(f"AUGMENTER {asset.upper()} de {-delta:.1%}")
    return actions

# =======================
# WALLET BACKTEST
# =======================

section_title("Analyse du wallet")

left, right = st.columns([1, 2])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Valeurs du wallet")
    portfolio = {}
    for asset in ASSETS:
        portfolio[asset] = st.number_input(asset.upper(), 0.0, step=100.0)
    strategy_choice = st.radio("Profil de risque", list(STRATEGIES.keys()), horizontal=True)
    strategy = STRATEGIES[strategy_choice]
    st.info(strategy["description"])
    analyze = st.button("Analyser")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    if analyze:
        current = normalize(portfolio)
        actions = detect_actions(strategy, current)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Répartition du portefeuille")
        st.table({
            "Catégorie": [a.upper() for a in ASSETS],
            "Actuel": [f"{current[a]:.1%}" for a in ASSETS],
            "Cible": [f"{strategy['targets'][a]:.1%}" for a in ASSETS]
        })

        st.subheader("Actions recommandées")
        if actions:
            for a in actions:
                st.warning(a)
        else:
            st.success("Portefeuille aligné avec la stratégie")
        st.markdown('</div>', unsafe_allow_html=True)

# =======================
# BUSINESS PLAN & SCORING
# =======================

section_title("Business plan et scoring du wallet")

st.markdown('<div class="card">', unsafe_allow_html=True)

btc = st.number_input("BTC Treasury", 0.0, step=500.0)
eth = st.number_input("ETH Treasury", 0.0, step=500.0)
stable = st.number_input("Stablecoins", 0.0, step=500.0)
other = st.number_input("Autres actifs", 0.0, step=500.0)

total = btc + eth + stable + other
st.metric("Valeur totale", f"${total:,.0f}")

ltv = st.slider("LTV global", 0, 80, 30)
apr = st.slider("APR moyen estimé", 0.0, 30.0, 8.0)

monthly = total * apr / 100 / 12 if total > 0 else 0
st.metric("Cashflow mensuel estimé", f"${monthly:,.0f}")

# =======================
# SCORING ENGINE (FIX + EXTENSION)
# =======================

stable_ratio = stable / total if total > 0 else 0
non_stable_ratio = 1 - stable_ratio if total > 0 else 0

stability_score = min(100, (stable_ratio * 70) + max(0, 50 - ltv))
risk_score = max(0, 100 - ltv * 1.2)
yield_score = min(100, (apr * 2) + (non_stable_ratio * 40))

global_score = int((stability_score + risk_score + yield_score) / 3)

# =======================
# PROFILE DETECTION
# =======================

if stability_score >= 70 and ltv < 40:
    profile = "SAFE"
elif yield_score >= 65 or ltv > 55:
    profile = "DEGEN"
else:
    profile = "MID"

# =======================
# DISPLAY
# =======================

st.subheader("Score global du wallet")
st.progress(global_score / 100)
st.metric("Score total", f"{global_score}/100")

c1, c2, c3 = st.columns(3)
c1.metric("🛡 Stability", f"{int(stability_score)}/100")
c2.metric("⚠️ Risk", f"{int(risk_score)}/100")
c3.metric("🚀 Yield", f"{int(yield_score)}/100")

st.subheader("Profil détecté")
if profile == "SAFE":
    st.success("Profil SAFE — capital préservé")
elif profile == "MID":
    st.warning("Profil MID — équilibre rendement / risque")
else:
    st.error("Profil DEGEN — rendement élevé, risque élevé")

st.markdown('</div>', unsafe_allow_html=True)
