import json
import matplotlib.pyplot as plt
import streamlit as st

# --- Ladda in data från full analysfil ---
with open("full_analysis_result.json", "r") as f:
    full_analysis = json.load(f)

balance_data = full_analysis.get("balance_sheet_and_cash_flow_analysis", [])
income_data = full_analysis.get("income_statement_analysis", [])

# --- Skapa lista över alla nyckeltal och deras etiketter ---
nyckeltal = {
    # Balansräkning och kassaflöde
    "Soliditet (%)": "Procent",
    "Skuldsättningsgrad": "Tal",
    "Kassalikviditet": "Tal",
    "Rörelsekapital (MUSD)": "Miljoner USD",
    "Net Debt / Equity": "Tal",
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

st.title("📊 Fundamental analys – Apple Inc.")

# Dropdown för att välja nyckeltal
val = st.selectbox("Välj nyckeltal att visa:", list(nyckeltal.keys()))

# --- Funktion för att plocka ut data för valt nyckeltal ---
def get_metric_values(metric_name):
    # Försök hitta värden i balansdata först
    values = []
    years = []
    for entry in balance_data:
        year = entry.get("År")
        val = entry.get(metric_name)
        if val is not None:
            years.append(year)
            values.append(val)

    # Om inte hittade något där, kolla i income_data
    if not values:
        for entry in income_data:
            year = entry.get("År")
            val = entry.get(metric_name)
            if val is not None:
                years.append(year)
                values.append(val)

    return years, values

years, values = get_metric_values(val)

# Rita diagram
def plot_metric(years, values, metric_name, ylabel):
    fig, ax = plt.subplots()
    ax.plot(years, values, marker='o', linestyle='-', color='teal')
    ax.set_title(f"{metric_name} över tid")
    ax.set_xlabel("År")
    ax.set_ylabel(ylabel)
    ax.grid(True)
    return fig

if years and values:
    fig = plot_metric(years, values, val, nyckeltal[val])
    st.pyplot(fig)
else:
    st.warning(f"Inga data tillgängliga för '{val}'.")
