import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Analisis Penyewaan Sepeda 🚴‍♂️")

dataset_choice = st.sidebar.selectbox("Pilih Dataset", ["data_1.csv", "data_2.csv"])

df = pd.read_csv(f"data/{dataset_choice}")

if "dteday" in df.columns:
    df["dteday"] = pd.to_datetime(df["dteday"])

st.write(f"### Data Awal ({dataset_choice})")
st.dataframe(df.head())

if "dteday" in df.columns:
    st.write("### Tren Penyewaan Sepeda dari Waktu ke Waktu")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=df["dteday"], y=df["cnt"], ax=ax)
    plt.xlabel("Tanggal")
    plt.ylabel("Jumlah Penyewaan")
    plt.title("Tren Penyewaan Sepeda dari Waktu ke Waktu")
    fig.tight_layout()
    st.pyplot(fig)

if "season" in df.columns:
    st.write("### Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=df["season"], y=df["cnt"], errorbar=None, ax=ax)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
    plt.xlabel("Musim")
    plt.ylabel("Jumlah Penyewaan")
    plt.title("Penyewaan Sepeda Berdasarkan Musim")
    fig.tight_layout()
    st.pyplot(fig)

if "workingday" in df.columns:
    st.write("### Perbandingan Penyewaan Sepeda pada Hari Kerja dan Akhir Pekan")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x=df["workingday"], y=df["cnt"], ax=ax)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Akhir Pekan / Libur", "Hari Kerja"])
    plt.xlabel("Jenis Hari")
    plt.ylabel("Jumlah Penyewaan")
    plt.title("Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
    fig.tight_layout()
    st.pyplot(fig)

st.write("### Sumber Data")
st.write("Data diambil dari sistem Bike Sharing Washington D.C. (2011-2012).")