import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Bank Marketing Dashboard",
    layout="wide"
)

st.title("📊 Bank Marketing Analytics Dashboard")
st.markdown("Interactive analysis of customer subscription behavior")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    try:
        return pd.read_csv("bank_data/Bank.csv")
    except:
        return None

df = load_data()

if df is None:
    st.error("❌ Bank.csv not found. Make sure it is inside the 'bank_data' folder.")
    st.stop()

st.success("✅ Data loaded successfully!")

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.subheader("Dataset Preview")
st.dataframe(df.head())

# -----------------------------
# SECTION 1 — CATEGORY ANALYSIS
# -----------------------------
st.header("📌 Subscription Analysis by Category")

fig1, axes = plt.subplots(2, 2, figsize=(14, 10))

sb.barplot(
    x=df.groupby('job')['y'].sum().index,
    y=df.groupby('job')['y'].sum().values,
    ax=axes[0, 0]
)
axes[0, 0].set_title("By Job")
axes[0, 0].tick_params(axis='x', rotation=45)

sb.barplot(
    x=df.groupby('education')['y'].sum().index,
    y=df.groupby('education')['y'].sum().values,
    ax=axes[0, 1]
)
axes[0, 1].set_title("By Education")
axes[0, 1].tick_params(axis='x', rotation=45)

sb.barplot(
    x=df.groupby('marital')['y'].sum().index,
    y=df.groupby('marital')['y'].sum().values,
    ax=axes[1, 0]
)
axes[1, 0].set_title("By Marital Status")

sb.barplot(
    x=df.groupby('default')['y'].sum().index,
    y=df.groupby('default')['y'].sum().values,
    ax=axes[1, 1]
)
axes[1, 1].set_title("By Default")

st.pyplot(fig1)

# -----------------------------
# SECTION 2 — CORRELATION
# -----------------------------
st.header("📌 Correlation Analysis")

corr = df[['age', 'duration', 'campaign', 'pdays', 'y']].corr()

fig2, ax = plt.subplots(figsize=(8, 6))
sb.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

st.pyplot(fig2)

# -----------------------------
# SECTION 3 — CAMPAIGN BEHAVIOR
# -----------------------------
st.header("📌 Campaign Behavior")

col1, col2 = st.columns(2)

with col1:
    fig3, ax = plt.subplots()
    sb.boxplot(x=df['y'], y=df['duration'], ax=ax)
    ax.set_title("Call Duration vs Subscription")
    st.pyplot(fig3)

with col2:
    fig4, ax = plt.subplots()
    sb.boxplot(x=df['y'], y=df['campaign'], ax=ax)
    ax.set_title("Campaign Contacts vs Subscription")
    st.pyplot(fig4)

# -----------------------------
# SECTION 4 — TIME ANALYSIS
# -----------------------------
st.header("Time-based Subscription Trends")

fig5, axes = plt.subplots(1, 2, figsize=(14, 5))

month = df.groupby('month')['y'].mean()
sb.barplot(x=month.index, y=month.values, ax=axes[0])
axes[0].set_title("By Month")

day = df.groupby('day_of_week')['y'].mean()
sb.barplot(x=day.index, y=day.values, ax=axes[1])
axes[1].set_title("By Day")

st.pyplot(fig5)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("✨ Built with Streamlit | Bank Marketing Analysis")


