import json
import matplotlib.pyplot as plt
import streamlit as st

# --- Ladda in data från full analysfil ---
with open("full_analysis_result.json", "r") as f:
    full_analysis = json.load(f)

balance_data = full_analysis.get("balance_sheet_and_cash_flow_analysis", [])
income_data = full_analysis.get("income_statement_analysis", [])

# --- Lista över nyckeltal och etiketter ---
nyckeltal = {
    # Balansräkning och kassaflöde
    "Soliditet (%)": "Procent",
    "Skuldsättningsgrad": "Tal",
    "Kassalikviditet": "Tal",
    "Rörelsekapital (MUSD)": "Miljoner USD",
    "Net Debt / Equity": "Tal",
    "Net Debt / EBITDA": "Tal",
    "Investeringar / Tillgångar (%)": "Procent",
    "ROE (%)": "Procent",
    "ROA (%)": "Procent",
    "FCF-marginal (%)": "Procent",
    "CapEx / OCF (%)": "Procent",

    # Resultaträkning
    "Omsättning (USD)": "USD",
    "Bruttomarginal (%)": "Procent",
    "Rörelsemarginal (%)": "Procent",
    "Nettomarginal (%)": "Procent",
    "EPS (USD)": "USD"
}

# --- Hälsobedömningar för nyckeltal ---
def bedom_nyckeltal(namn, varde):
    if varde is None:
        return "⚠️ Ej tillgängligt"

    match namn:
        case "Soliditet (%)":
            return "✅ Hälsosamt" if varde >= 30 else "❌ Lågt"
        case "Skuldsättningsgrad":
            return "✅ Hälsosamt" if varde <= 1.0 else "❌ Högt"
        case "Kassalikviditet":
            return "✅ Hälsosamt" if varde >= 1.0 else "❌ Under 1.0"
        case "Net Debt / Equity":
            return "✅ Hälsosamt" if varde < 1.0 else "❌ Högt"
        case "Net Debt / EBITDA":
            return "✅ Hälsosamt" if varde <= 2.0 else "❌ Över 2.0"
        case "ROE (%)":
            return "✅ Bra" if varde >= 15 else "⚠️ Lågt"
        case "ROA (%)":
            return "✅ Bra" if varde >= 5 else "⚠️ Lågt"
        case "FCF-marginal (%)":
            return "✅ Stark" if varde >= 10 else "⚠️ Svag"
        case "CapEx / OCF (%)":
            return "✅ Rimlig" if 10 <= varde <= 30 else "⚠️ Avvikande"
        case "Bruttomarginal (%)":
            return "✅ Bra" if varde >= 30 else "❌ Låg"
        case "Rörelsemarginal (%)":
            return "✅ Stark" if varde >= 15 else "⚠️ Låg"
        case "Nettomarginal (%)":
            return "✅ Bra" if varde >= 10 else "⚠️ Låg"
        case _:
            return "ℹ️ Ingen bedömning"

# --- Titel och val ---
st.title("📊 Fundamental analys – Apple Inc.")
val = st.selectbox("Välj nyckeltal att visa:", list(nyckeltal.keys()))

# --- Hämta data för valt nyckeltal ---
def get_metric_values(metric_name):
    values = []
    years = []
    for entry in balance_data:
        year = entry.get("År")
        val = entry.get(metric_name)
        if val is not None:
            years.append(year)
            values.append(val)

    if not values:
        for entry in income_data:
            year = entry.get("År")
            val = entry.get(metric_name)
            if val is not None:
                years.append(year)
                values.append(val)

    return years, values

years, values = get_metric_values(val)

# --- Rita diagram ---
def plot_metric(years, values, metric_name, ylabel):
    fig, ax = plt.subplots()
    ax.plot(years, values, marker='o', linestyle='-', color='teal')
    ax.set_title(f"{metric_name} över tid")
    ax.set_xlabel("År")
    ax.set_ylabel(ylabel)
    ax.grid(True)
    return fig

# --- Visa resultat ---
if years and values:
    fig = plot_metric(years, values, val, nyckeltal[val])
    st.pyplot(fig)

    # Visa senaste värde med bedömning
    senaste_ar = years[-1]
    senaste_varde = values[-1]
    bedomning = bedom_nyckeltal(val, senaste_varde)

    st.markdown(f"### 📌 Senaste värde ({senaste_ar}): `{senaste_varde:.2f}` → {bedomning}")
else:
    st.warning(f"Inga data tillgängliga för '{val}'.")
