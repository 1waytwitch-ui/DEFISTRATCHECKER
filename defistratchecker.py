import streamlit as st

# =======================
# CONFIG UI
# =======================

st.set_page_config(
    page_title="DeFi Strategy Analyzer",
    layout="wide"
)

# =======================
# STRATEGIES PREDEFINIES
# =======================

STRATEGIES = {
    "SAFE": {
        "description": "Préservation du capital, faible levier, faible volatilité",
        "targets": {
            "hodl": 0.45,
            "lending": 0.45,
            "liquidity_pool": 0.10,
            "borrowing": 0.00
        },
        "rebalance_threshold": 0.05
    },
    "MID": {
        "description": "Équilibre rendement / risque, levier modéré",
        "targets": {
            "hodl": 0.20,
            "lending": 0.45,
            "liquidity_pool": 0.25,
            "borrowing": 0.10
        },
        "rebalance_threshold": 0.05
    },
    "DEGEN": {
        "description": "Rendement maximal, levier élevé, forte volatilité",
        "targets": {
            "hodl": 0.05,
            "lending": 0.35,
            "liquidity_pool": 0.40,
            "borrowing": 0.20
        },
        "rebalance_threshold": 0.10
    }
}

# =======================
# MOCK LECTURE EVM
# =======================

def get_portfolio_from_evm(address: str):
    """
    Mock simple par adresse.
    Les montants sont en USD.
    """
    if not address or not address.startswith("0x"):
        return None

    seed = int(address[-4:], 16) % 100

    hodl = 2000 + seed * 10
    lending = 3500 + seed * 20
    lp = 2500 + seed * 15
    borrowing = 1200 + seed * 5  # dette

    total_exposure = hodl + lending + lp

    return {
        "hodl": hodl,
        "lending": lending,
        "liquidity_pool": lp,
        "borrowing": borrowing,
        "total_usd": total_exposure
    }

# =======================
# LOGIQUE METIER
# =======================

def normalize_portfolio(portfolio):
    total = portfolio["total_usd"]
    return {
        "hodl": portfolio["hodl"] / total,
        "lending": portfolio["lending"] / total,
        "liquidity_pool": portfolio["liquidity_pool"] / total,
        "borrowing": portfolio["borrowing"] / total
    }

def detect_actions(strategy, current):
    actions = []
    threshold = strategy["rebalance_threshold"]
    targets = strategy["targets"]

    for asset, target in targets.items():
        actual = current.get(asset, 0)
        delta = actual - target

        if delta > threshold:
            actions.append(f"REDUIRE {asset.upper()} de {delta:.1%}")
        elif delta < -threshold:
            actions.append(f"AUGMENTER {asset.upper()} de {-delta:.1%}")

    return actions

# =======================
# UI
# =======================

st.title("DeFi Strategy Analyzer")
st.caption("Analyse lecture seule • Une adresse EVM • Stratégies prédéfinies")

left, right = st.columns([1, 2])

# =======================
# COLONNE GAUCHE — INPUTS
# =======================

with left:
    st.subheader("Adresse EVM")

    address = st.text_input(
        "Colle une adresse EVM",
        placeholder="0x..."
    )

    st.subheader("Profil de stratégie")

    strategy_name = st.selectbox(
        "Choisis un profil",
        ["SAFE", "MID", "DEGEN"]
    )

    strategy = STRATEGIES[strategy_name]

    st.info(strategy["description"])

    analyze = st.button("Analyser la stratégie")

# =======================
# COLONNE DROITE — RESULTATS
# =======================

with right:
    if analyze:
        portfolio = get_portfolio_from_evm(address)

        if portfolio is None:
            st.error("Adresse EVM invalide")
            st.stop()

        current_pct = normalize_portfolio(portfolio)
        actions = detect_actions(strategy, current_pct)

        # -----------------------
        # RESUME
        # -----------------------

        st.subheader("Résumé du portefeuille")

        st.write(f"Valeur totale (hors dette) : ${portfolio['total_usd']:,.0f}")
        st.write(f"Dette (Borrowing) : ${portfolio['borrowing']:,.0f}")

        st.table({
            "Position": ["HODL", "LENDING", "LIQUIDITY POOL", "BORROWING"],
            "Actuel": [
                f"{current_pct['hodl']:.1%}",
                f"{current_pct['lending']:.1%}",
                f"{current_pct['liquidity_pool']:.1%}",
                f"{current_pct['borrowing']:.1%}",
            ],
            "Cible": [
                f"{strategy['targets']['hodl']:.1%}",
                f"{strategy['targets']['lending']:.1%}",
                f"{strategy['targets']['liquidity_pool']:.1%}",
                f"{strategy['targets']['borrowing']:.1%}",
            ],
        })

        # -----------------------
        # ACTIONS
        # -----------------------

        st.subheader("Actions recommandées")

        if not actions:
            st.success("Le portefeuille est aligné avec la stratégie")
        else:
            for a in actions:
                st.warning(a)

        st.caption("Aucune transaction exécutée • Pas de gestion de wallet")
