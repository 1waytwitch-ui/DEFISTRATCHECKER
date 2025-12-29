import streamlit as st

# -----------------------
# CONFIG
# -----------------------

DEFAULT_STRATEGY = {
    "cash": 0.20,
    "lending": 0.50,
    "liquidity_pool": 0.30,
    "rebalance_threshold": 0.05
}

# -----------------------
# MOCK EVM READER
# (remplaçable par DeBank / Zapper)
# -----------------------

def get_portfolio_from_evm(address: str):
    """
    Mock simple : retourne un portefeuille fictif.
    Plus tard : brancher une vraie API.
    """
    if not address or len(address) < 10:
        return None

    return {
        "cash": 1500,
        "lending": 6200,
        "liquidity_pool": 2300,
        "total_usd": 10000
    }

# -----------------------
# LOGIQUE METIER
# -----------------------

def normalize_portfolio(portfolio):
    total = portfolio["total_usd"]
    return {
        "cash": portfolio["cash"] / total,
        "lending": portfolio["lending"] / total,
        "liquidity_pool": portfolio["liquidity_pool"] / total
    }

def detect_actions(strategy, current):
    actions = []
    threshold = strategy["rebalance_threshold"]

    for asset in ["cash", "lending", "liquidity_pool"]:
        target = strategy[asset]
        actual = current.get(asset, 0)
        delta = actual - target

        if delta > threshold:
            actions.append(
                f"REDUIRE {asset.upper()} de {delta:.1%}"
            )
        elif delta < -threshold:
            actions.append(
                f"AUGMENTER {asset.upper()} de {-delta:.1%}"
            )

    return actions

# -----------------------
# UI STREAMLIT
# -----------------------

st.set_page_config(page_title="DeFi Strategy Checker", layout="centered")

st.title("DeFi Strategy Checker")
st.subheader("Lecture seule – stratégie vs portefeuille réel")

# ---- Adresse EVM ----
address = st.text_input(
    "Adresse EVM",
    placeholder="0x..."
)

# ---- Stratégie ----
st.markdown("### Stratégie cible")

cash_pct = st.slider("Cash / Stablecoins", 0.0, 1.0, DEFAULT_STRATEGY["cash"], 0.05)
lending_pct = st.slider("Lending", 0.0, 1.0, DEFAULT_STRATEGY["lending"], 0.05)
lp_pct = st.slider("Liquidity Pool", 0.0, 1.0, DEFAULT_STRATEGY["liquidity_pool"], 0.05)

threshold = st.slider(
    "Seuil de rééquilibrage",
    0.01,
    0.20,
    DEFAULT_STRATEGY["rebalance_threshold"],
    0.01
)

total = cash_pct + lending_pct + lp_pct

if abs(total - 1.0) > 0.001:
    st.error("La somme des allocations doit être égale à 100 %")
    st.stop()

strategy = {
    "cash": cash_pct,
    "lending": lending_pct,
    "liquidity_pool": lp_pct,
    "rebalance_threshold": threshold
}

# ---- Analyse ----
if st.button("Analyser le portefeuille"):
    portfolio = get_portfolio_from_evm(address)

    if portfolio is None:
        st.error("Adresse EVM invalide")
        st.stop()

    current_pct = normalize_portfolio(portfolio)
    actions = detect_actions(strategy, current_pct)

    st.markdown("### Portefeuille détecté (en %)")

    st.table({
        "Actif": ["Cash", "Lending", "Liquidity Pool"],
        "Actuel": [
            f"{current_pct['cash']:.1%}",
            f"{current_pct['lending']:.1%}",
            f"{current_pct['liquidity_pool']:.1%}",
        ],
        "Cible": [
            f"{strategy['cash']:.1%}",
            f"{strategy['lending']:.1%}",
            f"{strategy['liquidity_pool']:.1%}",
        ],
    })

    st.markdown("### Actions recommandées")

    if not actions:
        st.success("Le portefeuille est aligné avec la stratégie")
    else:
        for action in actions:
            st.warning(action)

    st.caption("Aucune transaction n’est exécutée. Lecture seule.")
