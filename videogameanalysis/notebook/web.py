import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # MANDATORY FOR CLOUD SERVERS: Forces non-interactive background engine
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="🎮 Video Game Sales Analytics Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
.main-title{
    font-size:42px;
    font-weight:700;
    color:#2563EB;
}
.sub-title{
    font-size:18px;
    color:#555;
}
.metric-card{
    background:#f8fafc;
    border-radius:12px;
    padding:20px;
    text-align:center;
    border-left:6px solid #2563EB;
    box-shadow:0 3px 10px rgba(0,0,0,0.08);
}
.metric-value{
    font-size:32px;
    font-weight:bold;
    color:#2563EB;
}
.metric-label{
    color:#444;
    font-size:15px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data():
    possible_paths = [
        "vgsales.csv",
        "data/vgsales.csv",
        "../vgsales.csv"
    ]
    df = None

    for path in possible_paths:
        if Path(path).exists():
            df = pd.read_csv(path)
            break

    if df is None:
        st.warning("vgsales.csv not found. Showing demo dataset.")
        np.random.seed(42)
        n = 16327
        genres = ['Action','Sports','Misc','Role-Playing','Shooter','Adventure','Racing','Platform','Simulation','Fighting','Strategy','Puzzle']
        publishers = ['Nintendo','Electronic Arts','Ubisoft','Activision','Konami','Namco Bandai']
        platforms = ['PS2','PS3','PS4','Xbox','X360','Wii','DS','PC']

        sales = np.random.lognormal(-1.5, 1.1, n)
        sales = np.clip(sales, 0.01, 82.74)

        df = pd.DataFrame({
            "Rank": range(1, n+1),
            "Name": [f"Game {i}" for i in range(n)],
            "Platform": np.random.choice(platforms, n),
            "Year": np.random.randint(1980, 2017, n),
            "Genre": np.random.choice(genres, n),
            "Publisher": np.random.choice(publishers, n),
            "NA_Sales": sales*0.45,
            "EU_Sales": sales*0.30,
            "JP_Sales": sales*0.15,
            "Other_Sales": sales*0.10,
            "Global_Sales": sales
        })

    df = df.dropna(subset=["Year", "Publisher"]).copy()
    df["Year"] = df["Year"].astype(int)
    df["Western_Sales"] = df["NA_Sales"] + df["EU_Sales"]
    df["Era"] = pd.cut(
        df["Year"],
        bins=[1970, 2000, 2010, 2030],
        labels=["Retro Era", "Modern Era", "Current Era"]
    )
    df["Title_Length"] = df["Name"].astype(str).str.len()

    def strategy(row):
        # Prevent zero-division evaluation edge cases
        denom = max(row["Global_Sales"], 0.01)
        if row["JP_Sales"] / denom > 0.7:
            return "Japan Exclusive"
        elif row["Western_Sales"] / denom > 0.8:
            return "Western Focus"
        else:
            return "Global"

    df["Market_Strategy"] = df.apply(strategy, axis=1)
    return df

df = load_data()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("🎮 Dashboard")
mode = st.sidebar.radio(
    "Choose Section",
    [
        "📋 Overview",
        "🛠️ Schema Integrity",
        "💾 SQL Analysis",
        "📈 Statistical Analysis",
        "🌍 Regional Analysis",
        "🚀 Feature Engineering"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Dataset Summary")
st.sidebar.write(f"Rows : **{len(df):,}**")
st.sidebar.write(f"Columns : **{df.shape[1]}**")
st.sidebar.write(f"Platforms : **{df['Platform'].nunique()}**")
st.sidebar.write(f"Publishers : **{df['Publisher'].nunique()}**")
st.sidebar.write(f"Years : **{df['Year'].min()} - {df['Year'].max()}**")

# --------------------------------------------------
# OVERVIEW PAGE
# --------------------------------------------------
if mode == "📋 Overview":
    st.markdown('<p class="main-title">🎮 Video Game Sales Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Interactive Business Intelligence Dashboard built with Python, Pandas, SQL, Matplotlib, Seaborn & Streamlit</p>', unsafe_allow_html=True)
    st.divider()

    total_games = len(df)
    total_sales = df["Global_Sales"].sum()
    western_share = (df["Western_Sales"].sum() / max(total_sales, 1.0)) * 100
    total_platforms = df["Platform"].nunique()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total_games:,}</div><div class="metric-label">Games</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{western_share:.1f}%</div><div class="metric-label">Western Market Share</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total_sales:,.0f} M</div><div class="metric-label">Global Sales</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total_platforms}</div><div class="metric-label">Platforms</div></div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("📌 Business Insights")
    st.success("""
✅ **Western markets dominate** global revenue, contributing the majority of total sales.

✅ **Median sales are much lower than the mean**, indicating a highly right-skewed distribution where only a few blockbuster games generate massive revenue.

✅ **Nintendo, Sony, and Microsoft platforms** consistently produce the highest-selling titles.

✅ **Action, Sports, and Shooter** genres contribute a major share of worldwide sales.
""")

# --------------------------------------------------
# SCHEMA INTEGRITY
# --------------------------------------------------
elif mode == "🛠️ Schema Integrity":
    st.title("🛠️ Dataset Integrity Report")
    st.write("This section validates the dataset structure, identifies missing values, examines data types, and provides a quick overview before analysis.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dataset Shape")
        shape_df = pd.DataFrame({"Metric": ["Rows", "Columns"], "Value": [df.shape[0], df.shape[1]]})
        st.dataframe(shape_df, use_container_width=True)
    with col2:
        st.subheader("Data Types")
        dtype_df = pd.DataFrame({"Column": df.columns, "Datatype": df.dtypes.astype(str)})
        st.dataframe(dtype_df, use_container_width=True)

    st.divider()
    st.subheader("Missing Values")
    missing = df.isnull().sum().reset_index()
    missing.columns = ["Column", "Missing Values"]
    st.dataframe(missing, use_container_width=True)

    st.divider()
    st.subheader("Statistical Summary")
    st.dataframe(df.describe(), use_container_width=True)

    st.divider()
    st.subheader("First 10 Records")
    st.dataframe(df.head(10), use_container_width=True)

# --------------------------------------------------
# SQL ANALYSIS
# --------------------------------------------------
elif mode == "💾 SQL Analysis":
    st.title("💾 SQL Business Intelligence")
    query = st.selectbox(
        "Select Business Query",
        ["Top 10 Best Selling Games", "Top Publishers", "Top Platforms", "Genre Performance", "Yearly Sales", "Publisher Revenue"]
    )

    if query == "Top 10 Best Selling Games":
        st.code("SELECT Name, Platform, Global_Sales FROM VideoGames ORDER BY Global_Sales DESC LIMIT 10;")
        top_games = df.sort_values("Global_Sales", ascending=False)[["Name", "Platform", "Genre", "Publisher", "Global_Sales"]].head(10)
        st.dataframe(top_games, use_container_width=True)

    elif query == "Top Publishers":
        st.code("SELECT Publisher, COUNT(*) AS Total_Games FROM VideoGames GROUP BY Publisher ORDER BY Total_Games DESC;")
        publisher_df = df.groupby("Publisher").size().reset_index(name="Games Released").sort_values("Games Released", ascending=False)
        st.dataframe(publisher_df, use_container_width=True)

    elif query == "Top Platforms":
        st.code("SELECT Platform, SUM(Global_Sales) FROM VideoGames GROUP BY Platform ORDER BY SUM(Global_Sales) DESC;")
        platform_sales = df.groupby("Platform")["Global_Sales"].sum().reset_index().sort_values("Global_Sales", ascending=False)
        st.dataframe(platform_sales, use_container_width=True)

    elif query == "Genre Performance":
        st.code("SELECT Genre, AVG(Global_Sales) FROM VideoGames GROUP BY Genre;")
        genre = df.groupby("Genre")["Global_Sales"].agg(["count", "mean", "sum"]).round(2).reset_index()
        genre.columns = ["Genre", "Games", "Average Sales", "Total Sales"]
        st.dataframe(genre, use_container_width=True)

    elif query == "Yearly Sales":
        st.code("SELECT Year, SUM(Global_Sales) FROM VideoGames GROUP BY Year;")
        yearly = df.groupby("Year")["Global_Sales"].sum().reset_index()
        st.dataframe(yearly, use_container_width=True)

    elif query == "Publisher Revenue":
        st.code("SELECT Publisher, SUM(Global_Sales) FROM VideoGames GROUP BY Publisher ORDER BY SUM(Global_Sales) DESC;")
        revenue = df.groupby("Publisher")["Global_Sales"].sum().reset_index().sort_values("Global_Sales", ascending=False)
        st.dataframe(revenue, use_container_width=True)

    st.divider()
    st.info("These analyses demonstrate how SQL aggregation functions can be replicated efficiently using the Pandas library.")

# --------------------------------------------------
# STATISTICAL ANALYSIS
# --------------------------------------------------
elif mode == "📈 Statistical Analysis":
    st.title("📈 Statistical Analysis")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Mean Sales", f"{df['Global_Sales'].mean():.2f} M")
        st.metric("Median Sales", f"{df['Global_Sales'].median():.2f} M")
        st.metric("Maximum Sales", f"{df['Global_Sales'].max():.2f} M")
    with c2:
        st.metric("Minimum Sales", f"{df['Global_Sales'].min():.2f} M")
        st.metric("Standard Deviation", f"{df['Global_Sales'].std():.2f}")
        st.metric("Skewness", f"{df['Global_Sales'].skew():.2f}")

    st.divider()
    st.subheader("Distribution of Global Sales")
    
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.histplot(data=df, x="Global_Sales", bins=50, kde=True, ax=ax1)
    ax1.set_xlim(0, 3)
    st.pyplot(fig1)
    plt.close(fig1)  # MEMORY FIX: Explicit close handle for cloud execution

    st.divider()
    st.subheader("Sales Distribution by Genre")
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x="Genre", y="Global_Sales", ax=ax2)
    plt.xticks(rotation=45)
    ax2.set_ylim(0, 2)
    st.pyplot(fig2)
    plt.close(fig2)  # MEMORY FIX

    st.success("The dataset is highly right-skewed. A few blockbuster games generate exceptionally high sales while the majority have relatively low sales.")

# --------------------------------------------------
# REGIONAL ANALYSIS
# --------------------------------------------------
elif mode == "🌍 Regional Analysis":
    st.title("🌍 Regional Sales Analysis")

    regional = df.groupby("Genre")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].sum().sort_values("NA_Sales", ascending=False)

    st.subheader("Regional Sales by Genre")
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    regional.plot(kind="bar", ax=ax3)
    plt.xticks(rotation=45)
    ax3.set_ylabel("Sales (Millions)")
    st.pyplot(fig3)
    plt.close(fig3)  # MEMORY FIX

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("North America", f"{df['NA_Sales'].sum():,.0f} M")
    with c2:
        st.metric("Europe", f"{df['EU_Sales'].sum():,.0f} M")
    with c3:
        st.metric("Japan", f"{df['JP_Sales'].sum():,.0f} M")

    st.info("""
North America contributes the highest overall sales.

Europe is the second-largest market.

Japan strongly favors Role-Playing games compared to Western markets.
""")

# --------------------------------------------------
# FEATURE ENGINEERING
# --------------------------------------------------
elif mode == "🚀 Feature Engineering":
    st.title("🚀 Feature Engineering")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Average Sales by Era")
        era_df = df.groupby("Era", observed=False)["Global_Sales"].mean().reset_index()
        st.dataframe(era_df, use_container_width=True)
    with c2:
        st.subheader("Market Strategy")
        strategy_df = df["Market_Strategy"].value_counts().rename_axis("Strategy").reset_index(name="Games")
        st.dataframe(strategy_df, use_container_width=True)

    st.divider()
    st.subheader("Title Length vs Global Sales")
    
    sample_df = df.sample(min(600, len(df)), random_state=42)
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=sample_df, x="Title_Length", y="Global_Sales", alpha=0.6, ax=ax4)
    st.pyplot(fig4)
    plt.close(fig4)  # MEMORY FIX

    correlation = df["Title_Length"].corr(df["Global_Sales"])
    st.metric("Correlation", f"{correlation:.3f}")
    st.success("The correlation is extremely weak, indicating that game title length has virtually no relationship with commercial success.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.markdown("""
### 👨‍💻 About this Project
This dashboard demonstrates practical **Data Analytics** skills using:
- Python, Pandas, NumPy, SQL-style Analysis, Matplotlib, Seaborn, Feature Engineering, Business Intelligence, Streamlit

---
**Developed by Roshan Kumar Sah**
Chemical Engineering • NIT Durgapur
Aspiring Data Scientist | Machine Learning Enthusiast | Data Analyst
""")
