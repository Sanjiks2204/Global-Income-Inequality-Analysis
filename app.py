import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from streamlit_option_menu import option_menu

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Global Income Inequality Explorer", page_icon="🌐", layout="wide")

# ---------------- AUTH ----------------
def login_ui():
    st.markdown("### 🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign in", type="primary"):
        creds = st.secrets["credentials"]
        if username in creds["usernames"]:
            idx = creds["usernames"].index(username)
            if password == creds["passwords"][idx]:
                st.session_state.auth = {
                    "is_auth": True,
                    "user": creds["names"][idx],
                    "role": creds["roles"][idx],
                }
                st.success(f"Welcome, {creds['names'][idx]}!")
            else:
                st.error("Invalid password")
        else:
            st.error("Invalid username")

def require_auth():
    if "auth" not in st.session_state or not st.session_state.auth.get("is_auth"):
        login_ui()
        st.stop()

# ---------------- HEADER / THEME / FOOTER ----------------
def header():
    left, _, right = st.columns([3,3,2])
    with left:
        st.markdown("## 🌐 Inequality Explorer")
        st.caption("Distinct socio‑economic insights, comparisons, trends, and smart narratives")
    with right:
        user = st.session_state.auth.get("user", "User")
        role = st.session_state.auth.get("role", "analyst")
        st.write(f"👤 {user}")
        st.caption(f"Role: {role}")

def theme_toggle():
    mode = st.toggle("Dark mode", value=False)
    if mode:
        st.markdown("""
        <style>
            .stApp { background-color: #121212; color: #E0E0E0; }
            .stMetric { background: #1E1E1E; border-radius: 8px; padding: 6px; }
            .stTextInput input, .stTextArea textarea, div[data-baseweb="select"] { background-color: #1E1E1E !important; color: #E0E0E0 !important; }
        </style>
        """, unsafe_allow_html=True)

def footer():
    st.markdown("---")
    st.caption(f"© {datetime.datetime.now().year} Global Income Inequality Explorer | Built by Sanjana")

# ---------------- NAVIGATION ----------------
def nav_bar():
    return option_menu(
        menu_title=None,
        options=["Overview", "Analytics", "Country Compare", "Trends", "Smart Insights"],
        icons=["grid", "bar-chart-line", "people", "activity", "lightbulb"],
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#1c1c1c", "border-radius": "12px"},
            "icon": {"color": "#00BFA5", "font-size": "18px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "center",
                "margin": "0px",
                "padding": "10px 20px",
                "color": "#E0E0E0",
                "border-radius": "12px",
            },
            "nav-link-selected": {
                "background-color": "#00BFA5",
                "color": "black",
                "font-weight": "600",
                "border-radius": "12px",
            },
        },
    )

# ---------------- UTILITIES ----------------
def powerbi_iframe(url, height=750):
    components.iframe(url, height=height, width=1200, scrolling=True)

def export_pdf(kpis, filters, notes):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, 27*cm, "Inequality Explorer Summary")
    y = 26*cm
    c.setFont("Helvetica", 11)
    c.drawString(2*cm, y, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 1*cm
    c.setFont("Helvetica-Bold", 12); c.drawString(2*cm, y, "Filters"); y -= 0.5*cm
    for k, v in filters.items():
        c.drawString(2*cm, y, f"- {k}: {v}"); y -= 0.5*cm
    y -= 0.5*cm
    c.setFont("Helvetica-Bold", 12); c.drawString(2*cm, y, "KPIs"); y -= 0.5*cm
    for k, v in kpis.items():
        c.drawString(2*cm, y, f"- {k}: {v}"); y -= 0.5*cm
    y -= 0.5*cm
    c.setFont("Helvetica-Bold", 12); c.drawString(2*cm, y, "Notes"); y -= 0.5*cm
    for line in notes.split("\n"):
        c.drawString(2*cm, y, line); y -= 0.5*cm
    c.showPage(); c.save(); buf.seek(0)
    return buf.read()

# ---------------- DATA & SIDEBAR ----------------
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is None:
        return None
    return pd.read_csv(uploaded_file)

def sidebar_filters():
    st.sidebar.markdown("## 🎛️ Filters")
    uploaded = st.sidebar.file_uploader("Upload CSV (optional)", type=["csv"])
    df = load_data(uploaded)
    year = st.sidebar.slider("Year", 2010, 2025, 2021)
    continent = st.sidebar.selectbox("Continent", ["All", "Africa", "America", "Asia", "Europe", "Oceania"])
    country = st.sidebar.text_input("Country")
    notes = st.sidebar.text_area("Notes", height=100)
    filters = {"Year": year, "Continent": continent, "Country": country or "All"}
    return df, filters, notes

# ---------------- KPI CARDS ----------------
def kpi_cards():
    st.markdown("### 📈 Key Indicators")
    c1, c2, c3 = st.columns(3)
    c1.metric("🌍 Avg Gini", "23.23")
    c2.metric("💼 Unemployment (%)", "7.78")
    c3.metric("⏳ Life Expectancy", "73 yrs")
    c4, c5, c6 = st.columns(3)
    c4.metric("📖 Literacy Rate", "86.65%")
    c5.metric("💰 GDP", "$19.01K")
    c6.metric("👥 Population", "38.18M")

# ---------------- PAGES ----------------
def page_overview():
    header(); theme_toggle()
    st.markdown("## 🌐 Welcome to Inequality Explorer")
    st.caption("Your personalized hub for socio‑economic insight")
    col1, col2, col3 = st.columns(3)
    with col1: st.info("📊 Explore analytics\nDive into KPIs and dashboards")
    with col2: st.success("🤝 Country comparisons\nSide‑by‑side inequality metrics")
    with col3: st.warning("💡 Smart insights\nNarratives and simple forecasts")
    st.markdown("---")
    st.write("### What makes this platform unique")
    st.write("- Clean, modern design\n- Personalized filters\n- Exportable summaries\n- Insight narratives")
    footer()

def page_analytics(url, filters, notes):
    header(); theme_toggle()
    st.markdown("### Analytics")
    kpi_cards()
    st.markdown("### Power BI Dashboard")
    powerbi_iframe(url, height=780)
    pdf_bytes = export_pdf(
        {"Gini": 23.23, "Unemployment": 7.78, "LifeExp": 73, "Literacy": 86.65, "GDP": "19.01K", "Pop": "38.18M"},
        filters, notes
    )
    st.download_button("Download KPI Summary (PDF)", pdf_bytes, "kpi_summary.pdf", "application/pdf")
    footer()

def compute_country_stats(df, countries):
    if df is None or "country" not in df.columns or "gini" not in df.columns:
        return pd.DataFrame({
            "country_name": ["China", "United States"],
            "Average": [26.33, 25.16],
            "Min": [23.22, 23.22],
            "Max": [27.39, 26.02],
        })
    dff = df[df["country"].isin(countries)].copy()
    rows = []
    for c in countries:
        s = dff[dff["country"] == c]["gini"]
        rows.append({
            "country_name": c,
            "Average": round(s.mean(), 2) if not s.empty else None,
            "Min": round(s.min(), 2) if not s.empty else None,
            "Max": round(s.max(), 2) if not s.empty else None,
        })
    return pd.DataFrame(rows)

def page_country_compare(url, df):
    header(); theme_toggle()
    st.markdown("### Country Comparison")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### View A")
        powerbi_iframe(url, height=700)
    with col2:
        st.markdown("#### View B")
        powerbi_iframe(url, height=700)

    st.markdown("### Statistics")
    options = sorted(df["country"].unique()) if df is not None and "country" in df.columns else ["United States", "China"]
    sel = st.multiselect("Select countries", options, default=options[:2])
    stats = compute_country_stats(df, sel)
    st.dataframe(stats, use_container_width=True)
    footer()

def simple_forecast(series, window=3, steps=3):
    if len(series) < window:
        return []
    ma = series.rolling(window).mean()
    last = ma.dropna().iloc[-1]
    return [round(float(last), 2)] * steps

def page_trends(df):
    header(); theme_toggle()
    st.markdown("### Trends")
    if df is None or not {"country", "year", "gini"}.issubset(df.columns):
        st.warning("Upload a CSV with columns: country, year, gini to enable interactive trends.")
        footer(); return
    country = st.selectbox("Select country", sorted(df["country"].unique()))
    dff = df[df["country"] == country].sort_values("year")
    st.line_chart(dff.set_index("year")[["gini"]], height=350)
    st.markdown("#### Forecast (naive moving average)")
    forecast_vals = simple_forecast(dff["gini"], window=3, steps=3)
    st.write(f"Projected Gini (next 3): {forecast_vals if forecast_vals else 'Not enough data'}")
    footer()

def ai_country_insights(df, country):
    if df is None or "gini" not in df.columns:
        return [
            f"{country}: Overall inequality appears moderate.",
            "Recommendation: Strengthen education and employment; track GDP vs. Gini."
        ]
    dff = df[df["country"] == country].sort_values("year")
    if dff.empty:
        return [f"No data for {country}. Please upload a dataset including this country."]
    gini_avg = round(dff["gini"].mean(), 2)
    trend_dir = "rising" if dff["gini"].diff().mean() > 0 else "falling"
    lines = [
        f"{country}: Average Gini ≈ {gini_avg} with a {trend_dir} tendency.",
        "If GDP rises while Gini worsens, growth may be unequal—pair with unemployment and literacy context.",
    ]
    if "unemployment" in dff.columns:
        unemp_avg = round(dff["unemployment"].mean(), 2)
        lines.append(f"Unemployment averages ~ {unemp_avg}%. Consider targeted job creation.")
    if "life_expectancy" in dff.columns:
        le = round(dff["life_expectancy"].mean(), 1)
        lines.append(f"Life expectancy averages ~ {le} years. Public health correlates with lower inequality.")
    lines.append("Policy ideas: social protection, progressive taxation, equitable education access.")
    return lines

def page_smart_insights(df):
    header(); theme_toggle()
    st.markdown("### Smart Insights")
    tab1, tab2, tab3, tab4 = st.tabs(["Country analysis", "Compare countries", "Trend prediction", "Assistant"])
    with tab1:
        st.markdown("#### Deep dive country analysis")
        options = sorted(df["country"].unique()) if df is not None and "country" in df.columns else ["Afghanistan"]
        country = st.selectbox("Select a country to analyze", options)
        if st.button("Generate analysis", type="primary"):
            for line in ai_country_insights(df, country):
                st.write(f"- {line}")
    with tab2:
        st.markdown("#### Quick compare")
        options = sorted(df["country"].unique()) if df is not None and "country" in df.columns else ["United States", "China"]
        cc = st.multiselect("Select countries", options, default=options[:2])
        stats = compute_country_stats(df, cc)
        st.dataframe(stats, use_container_width=True)
    with tab3:
        st.markdown("#### Trend prediction (moving average)")
        if df is None or "country" not in df.columns:
            st.info("Upload data to enable prediction.")
        else:
            ctry = st.selectbox("Country for prediction", sorted(df["country"].unique()))
            dff = df[df["country"] == ctry].sort_values("year")
            st.line_chart(dff.set_index("year")[["gini"]], height=300)
            fc = simple_forecast(dff["gini"], window=3, steps=3)
            st.write(f"Forecast next 3 points: {fc if fc else 'Not enough data'}")
    with tab4:
        st.info("Assistant placeholder. Integrate your preferred model or Q&A later.")
    footer()

# ---------------- MAIN ----------------
def main():
    require_auth()
    df, filters, notes = sidebar_filters()
    url = st.secrets["app"]["primary_dashboard_url"]
    selected = nav_bar()

    if selected == "Overview":
        page_overview()
    elif selected == "Analytics":
        page_analytics(url, filters, notes)
    elif selected == "Country Compare":
        page_country_compare(url, df)
    elif selected == "Trends":
        page_trends(df)
    elif selected == "Smart Insights":
        page_smart_insights(df)

if __name__ == "__main__":
    main()    