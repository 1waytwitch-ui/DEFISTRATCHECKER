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

# ---- HEADER ----
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
    font-size: 18px;
    font-weight: 600;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 12px;
    margin-left: 10px;
}
.krystal-btn {
    background-color: #06b6d4;
}
.plusvalue-btn {
    background-color: #10b981;
}
.lp-btn {
    background-color: #a17fff;
}
.telegram-btn {
    background-color: #6c5ce7;
}
.formation-btn {
    background-color: #f59e0b;
}
</style>

<div class="deFi-banner">
    <div class="deFi-title-text">DEFI WALLET BACKTEST</div>
    <div class="deFi-buttons">
        <a href="https://defi.krystal.app/referral?r=3JwR8YRQCRJT" target="_blank" class="krystal-btn">
            Krystal
        </a>
        <a href="https://plusvalueimposable.streamlit.app/" target="_blank" class="plusvalue-btn">
            Plus-value imposable
        </a>
        <a href="https://backtestenginelp.streamlit.app/" target="_blank" class="lp-btn">
            LP BACKTEST ENGINE
        </a>
        <a href="https://t.me/Pigeonchanceux" target="_blank" class="telegram-btn">
            <img src="https://t.me/i/userpic/320/Pigeonchanceux.jpg" style="width:30px;height:30px;border-radius:50%; vertical-align: middle; margin-right:5px;">
            Mon Telegram
        </a>
        <a href="https://shorturl.at/X3sYt" target="_blank" class="formation-btn">
            Formation code DEFI
        </a>
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
        padding: 14px 18px;
        border-radius: 8px;
        color: #000;
        margin-bottom: 25px;
        font-size: 14.5px;
        line-height: 1.35;
    ">
    <b>⚠️ DISCLAIMER IMPORTANT</b><br>
    L’accès au backtest est réservé aux membres de la <b>Team Élite KBOUR Crypto</b>. Le code d’accès est disponible dans le canal privé <b>« DEFI Académie »</b>.<br>
    <b>🔐 Confidentialité & données</b> — Les valeurs du wallet sont traitées <b>uniquement en local dans le navigateur</b> durant la session. Aucune donnée personnelle, adresse de wallet ou information sensible n’est enregistrée, transmise ou exploitée sur un serveur externe.<br>
    <b>Nature de l’analyse</b> — L’analyse est <b>purement statistique et indicative</b>, basée uniquement sur la répartition SAFE / MID / DEGEN. Les résultats ne tiennent pas compte de la situation personnelle, des conditions de marché en temps réel ou de paramètres externes et <b>ne constituent en aucun cas un conseil financier ou une recommandation d’investissement</b>.
    </div>
    """, unsafe_allow_html=True)


# -----------------------
# CODE SECRET
# -----------------------
SECRET_CODE = "2026"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    # HTML + CSS overlay + bouton
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
    .login-title { font-size: 28px; font-weight: 700; color: white !important; margin-bottom: 6px; }
    .login-subtitle { font-size: 14px; color: #d1d5db; margin-bottom: 18px; }
    .elite-btn {
        display: inline-block;
        background-color: #facc15;
        color: #111827 !important;
        font-size: 16px;
        font-weight: 700;
        text-decoration: none !important;
        padding: 10px 18px;
        border-radius: 14px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        margin-bottom: 18px;
    }
    .elite-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(250,204,21,0.4);
    }
    </style>

    <div class="login-card">
        <div class="login-title">Accès sécurisé</div>
        <div class="login-subtitle">
            Réservé aux membres de la <b>Team Élite KBOUR Crypto</b><br>
            Code disponible dans <b>DEFI Académie</b>
        </div>
        <!-- BOUTON EXTERNE -->
        <a href="https://www.youtube.com/channel/UCZL_vS9bsLI4maA4Oja9zyg/join" 
           target="_blank" class="elite-btn">
           Rejoindre la Team Élite
        </a>
    </div>
    """, unsafe_allow_html=True)

    # INPUT STREAMLIT séparé pour que ce soit cliquable
    st.text_input("Code d'accès", key="secret_code", type="password")
    if st.button("Valider", use_container_width=True):
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
        "targets": {
            "BTC NATIF": 0.40,
            "lending": 0.30,
            "borrowing": 0.05,
            "hodl": 0.15,
            "Pool de liquidité": 0.10
        },
        "threshold": 0.05
    },
    "MID": {
        "description": "Rendement équilibré",
        "targets": {
            "BTC NATIF": 0.25,
            "lending": 0.30,
            "borrowing": 0.15,
            "hodl": 0.10,
            "Pool de liquidité": 0.20
        },
        "threshold": 0.05
    },
    "DEGEN": {
        "description": "Rendement agressif et risques très élevés",
        "targets": {
            "BTC NATIF": 0.10,
            "lending": 0.15,
            "borrowing": 0.25,
            "hodl": 0.05,
            "Pool de liquidité": 0.45
        },
        "threshold": 0.10
    }
}

ASSETS = ["BTC NATIF", "lending", "borrowing", "hodl", "Pool de liquidité"]

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
# CHECKLIST UTILISATEUR
# =======================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Checklist de sécurité avant utilisation</div>', unsafe_allow_html=True)

checklist_items = [
    "Wallet BITCOIN sur la blockchain et sécurisé par coldwallet",
    "Wallet EVM sécurisé par coldwallet",
    "Je sauvegarde mes clés privées et mes seedphrases de manière sécurisée",
    "Utilisation DEFI et crypto sur PC dédié",
    "Utilisation de protocoles reconnus",
    "Utilisation de blockchain de layer 2 (base, arbitrum, etc.) pour limiter les frais",
    "Propres recherches faites avant de me lancer et tests effectué avec des petits montants",
    "Je maîtrise les swaps et bridges"
]

user_check = []
for item in checklist_items:
    user_check.append(st.checkbox(item, key=item))

score = sum(user_check)
st.write(f"Score de sécurité : {score}/{len(checklist_items)}")

if score <= 4:
    prof_color = "red"
    prof_text = "Risque élevé"
elif score <= 6:
    prof_color = "orange"
    prof_text = "Risque moyen"
else:
    prof_color = "green"
    prof_text = "Sécurisé"

st.markdown(f"<div style='font-weight:700; color:{prof_color}; font-size:20px'>Profil de sécurité : {prof_text}</div>", unsafe_allow_html=True)
st.progress(int(score/len(checklist_items)*100))

if prof_text == "Risque élevé":
    st.warning("⚠️ Votre profil est à risque élevé. Vous ne pouvez pas utiliser l'outil tant que la checklist n'est pas améliorée.")
    st.stop()
else:
    st.success("✅ Profil suffisant, vous pouvez continuer l'analyse.")

st.markdown('</div>', unsafe_allow_html=True)

# =======================
# UI PRINCIPAL
# =======================

left, right = st.columns([1,2])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Valeurs du wallet ($)</div>', unsafe_allow_html=True)
    portfolio = {}
    for asset in ASSETS:
        portfolio[asset] = st.number_input(asset.upper(), min_value=0.0, value=0.0, step=100.0, format="%.2f")

    st.markdown('<div class="section-title">Répartition SAFE / MID / DEGEN</div>', unsafe_allow_html=True)
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

        # Calcul portefeuille par stratégie
        composite_targets = {}
        for asset in ASSETS:
            composite_targets[asset] = (
                STRATEGIES["SAFE"]["targets"][asset]*safe_pct +
                STRATEGIES["MID"]["targets"][asset]*mid_pct +
                STRATEGIES["DEGEN"]["targets"][asset]*degen_pct
            )

        threshold = (STRATEGIES["SAFE"]["threshold"]*safe_pct +
                     STRATEGIES["MID"]["threshold"]*mid_pct +
                     STRATEGIES["DEGEN"]["threshold"]*degen_pct)
        actions = detect_actions(composite_targets, current, threshold)

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Répartition du portefeuille</div>', unsafe_allow_html=True)
        total_exposure = sum(portfolio[a] for a in ASSETS)
        st.write(f"Exposition totale : ${total_exposure:,.2f}")
        st.table({
            "Catégorie": [a.upper() for a in ASSETS],
            "Actuel": [f"{current[a]:.1%}" for a in ASSETS],
            "Cible": [
                f"{composite_targets[a]:.1%}"
                for a in ASSETS
            ]
        })


        # =======================
        # Répartition du profil de risque avec jauge calculée sur wallet actuel
        # =======================
        st.markdown('<div class="section-title">Répartition du profil de risque actuel</div>', unsafe_allow_html=True)
        # Calcul SAFE/MID/DEGEN réels selon la composition cible
        safe_val = sum(current[a]*STRATEGIES["SAFE"]["targets"][a] for a in ASSETS)
        mid_val = sum(current[a]*STRATEGIES["MID"]["targets"][a] for a in ASSETS)
        degen_val = sum(current[a]*STRATEGIES["DEGEN"]["targets"][a] for a in ASSETS)
        total_val = safe_val + mid_val + degen_val
        safe_ratio = safe_val/total_val if total_val>0 else 0
        mid_ratio = mid_val/total_val if total_val>0 else 0
        degen_ratio = degen_val/total_val if total_val>0 else 0

        st.markdown(f"""
        <div class="gauge-container">
            <div class="gauge-segment safe" style="width:{safe_ratio*100}%"></div>
            <div class="gauge-segment mid" style="width:{mid_ratio*100}%"></div>
            <div class="gauge-segment degen" style="width:{degen_ratio*100}%"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-weight:700;">
            <span>SAFE</span><span>MID</span><span>DEGEN</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">Répartition par stratégie</div>', unsafe_allow_html=True)
        for asset in ASSETS:
            st.progress(int(composite_targets[asset]*100), text=asset.upper())

        st.markdown('<div class="section-title">Actions recommandées</div>', unsafe_allow_html=True)
        if actions:
            for a in actions:
                st.warning(a)
        else:
            st.success("Portefeuille aligné avec la stratégie et le profil de risque")

        st.markdown('</div>', unsafe_allow_html=True)

# ======================
# APR
# ======================

def calculate_clmm_apr(
    fees_usd_period: float,
    active_liquidity_usd_avg: float,
    period_days: int
) -> float:
    """
    Calcule un APR annualisé basé uniquement sur l'active liquidity.
    """

    if active_liquidity_usd_avg <= 0 or period_days <= 0:
        return 0.0

    return (
        fees_usd_period
        / active_liquidity_usd_avg
        * (365 / period_days)
        * 100
    )


# ======================
# Interface
# ======================

st.title("APR indicatif – Pool de liquidité concentrée")

st.markdown("""
Ce calculateur estime un **APR observé** pour un pool de liquidité
concentrée à partir des **fees historiques** et de l'**active liquidity**
uniquement.

Il ne représente pas le rendement réel d'une position LP individuelle.
""")

st.header("Paramètres d'entrée")

fees_usd_period = st.number_input(
    "Total des fees générées sur la période (USD)",
    min_value=0.0,
    value=125000.0,
    step=1000.0
)

active_liquidity_usd_avg = st.number_input(
    "Active liquidity moyenne sur la période (USD)",
    min_value=0.0,
    value=4800000.0,
    step=10000.0
)

period_days = st.number_input(
    "Durée de la période (en jours)",
    min_value=1,
    value=7,
    step=1
)

# ======================
# Calcul
# ======================

apr = calculate_clmm_apr(
    fees_usd_period,
    active_liquidity_usd_avg,
    period_days
)

st.header("Résultat")

st.metric(
    label="APR annualisé estimé",
    value=f"{apr:.2f} %"
)

st.markdown("""
**Notes importantes**

- Les fees sont historiques et peuvent ne pas se répéter
- Seule l'active liquidity (in-range) est prise en compte
- Cette métrique sert à comparer des pools, pas à prédire un rendement
""")
