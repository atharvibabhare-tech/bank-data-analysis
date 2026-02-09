import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

st.title("Bank Marketing Dashboard")

df = pd.read_csv("Bank.csv")

job = st.sidebar.selectbox("Select Job", df["job"].unique())

filtered = df[df["job"] == job]

st.write(filtered.head())

fig, ax = plt.subplots()
sb.countplot(x="y", data=filtered, ax=ax)
st.pyplot(fig)
