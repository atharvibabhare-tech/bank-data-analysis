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

st.title("Bank Marketing Analytics Dashboard")
st.markdown("Interactive analysis of customer subscription behavior")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return df = pd.read_csv("Bank.csv")

try:
    df = load_data()
except:
    st.error("Bank.csv not found. Make sure it is in the repo root.")
    st.stop()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

job_filter = st.sidebar.multiselect(
    "Select Job",
    df["job"].unique(),
    default=df["job"].unique()
)

edu_filter = st.sidebar.multiselect(
    "Education",
    df["education"].unique(),
    default=df["education"].unique()
)

filtered_df = df[
    (df["job"].isin(job_filter)) &
    (df["education"].isin(edu_filter))
]

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df.head())

# -----------------------------
# KPI SECTION
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", len(filtered_df))
col2.metric("Avg Call Duration", round(filtered_df["duration"].mean(), 2))
col3.metric("Campaign Avg", round(filtered_df["campaign"].mean(), 2))

# -----------------------------
# SUBSCRIPTION BY CATEGORY
# -----------------------------
st.subheader("Subscription by Demographics")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

a = filtered_df.groupby("job")["y"].sum()
sb.barplot(x=a.index, y=a.values, ax=axes[0, 0])
axes[0, 0].set_title("By Job")
axes[0, 0].tick_params(axis='x', rotation=45)

b = filtered_df.groupby("education")["y"].sum()
sb.barplot(x=b.index, y=b.values, ax=axes[0, 1])
axes[0, 1].set_title("By Education")
axes[0, 1].tick_params(axis='x', rotation=45)

c = filtered_df.groupby("marital")["y"].sum()
sb.barplot(x=c.index, y=c.values, ax=axes[1, 0])
axes[1, 0].set_title("By Marital Status")

d = filtered_df.groupby("default")["y"].sum()
sb.barplot(x=d.index, y=d.values, ax=axes[1, 1])
axes[1, 1].set_title("By Default")

st.pyplot(fig)

# -----------------------------
# BOX PLOTS
# -----------------------------
st.subheader("Campaign Behavior")

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    sb.boxplot(x="y", y="duration", data=filtered_df, ax=ax1)
    ax1.set_title("Duration vs Subscription")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    sb.boxplot(x="y", y="campaign", data=filtered_df, ax=ax2)
    ax2.set_title("Campaign vs Subscription")
    st.pyplot(fig2)

# -----------------------------
# TIME ANALYSIS
# -----------------------------
st.subheader("Time Trends")

col1, col2 = st.columns(2)

with col1:
    month = filtered_df.groupby("month")["y"].mean()
    fig3, ax3 = plt.subplots()
    sb.barplot(x=month.index, y=month.values, ax=ax3)
    ax3.set_title("Monthly Subscription Rate")
    st.pyplot(fig3)

with col2:
    day = filtered_df.groupby("day_of_week")["y"].mean()
    fig4, ax4 = plt.subplots()
    sb.barplot(x=day.index, y=day.values, ax=ax4)
    ax4.set_title("Day-wise Subscription Rate")
    st.pyplot(fig4)

# -----------------------------
# CORRELATION HEATMAP
# -----------------------------
st.subheader("Correlation Heatmap")

corr = filtered_df[['age','duration','pdays','campaign','y']].corr()

fig5, ax5 = plt.subplots()
sb.heatmap(corr, annot=True, cmap="coolwarm", ax=ax5)
st.pyplot(fig5)

# -----------------------------
# FOOTER
# -----------------------------
st.success("Dashboard Loaded Successfully")
st.caption("Built with Streamlit + Data Analytics")
