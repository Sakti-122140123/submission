import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Analisis Penyewaan Sepeda 🚴‍♂️")

df_day = pd.read_csv("data/data_1.csv")
df_hour = pd.read_csv("data/data_2.csv")

df_day["dteday"] = pd.to_datetime(df_day["dteday"])
df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])
df = pd.concat([df_day, df_hour], ignore_index=True)

st.sidebar.header("Filter Data")
filter_type = st.sidebar.radio("Pilih Jenis Filter", ["Tanggal", "Musim", "Cuaca"])

if filter_type == "Tanggal":
    start_date = st.sidebar.date_input("Pilih Tanggal Mulai", df["dteday"].min())
    end_date = st.sidebar.date_input("Pilih Tanggal Akhir", df["dteday"].max())
    df_filtered = df[(df["dteday"] >= pd.to_datetime(start_date)) & (df["dteday"] <= pd.to_datetime(end_date))]

elif filter_type == "Musim":
    selected_season = st.sidebar.selectbox("Pilih Musim", ["Spring", "Summer", "Fall", "Winter"])
    season_mapping = {"Spring": 1, "Summer": 2, "Fall": 3, "Winter": 4}
    df_filtered = df[df["season"] == season_mapping[selected_season]]

elif filter_type == "Cuaca":
    selected_weathersit = st.sidebar.selectbox("Pilih Kondisi Cuaca", ["Cerah", "Berawan", "Hujan Ringan", "Hujan Lebat"])
    weather_mapping = {"Cerah": 1, "Berawan": 2, "Hujan Ringan": 3, "Hujan Lebat": 4}
    df_filtered = df[df["weathersit"] == weather_mapping[selected_weathersit]]

else:
    df_filtered = df.copy()

st.write("### Data Setelah Filter")
st.dataframe(df_filtered.head())

st.write("### Tren Penyewaan Sepeda dari Waktu ke Waktu")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=df_filtered["dteday"], y=df_filtered["cnt"], ax=ax)
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.title("Tren Penyewaan Sepeda dari Waktu ke Waktu")
plt.xticks(rotation=45)
fig.tight_layout()
st.pyplot(fig)

st.write("### Pengaruh Musim terhadap Jumlah Penyewaan Sepeda")
season_agg = df_filtered.groupby("season")["cnt"].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=season_agg["season"], y=season_agg["cnt"], ax=ax, palette="coolwarm")
ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
plt.xlabel("Musim")
plt.ylabel("Rata-rata Penyewaan Sepeda")
plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
fig.tight_layout()
st.pyplot(fig)

st.write("### Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda")
weather_agg = df_filtered.groupby("weathersit")["cnt"].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=weather_agg["weathersit"], y=weather_agg["cnt"], ax=ax, palette="viridis")
ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(["Cerah", "Berawan", "Hujan Ringan", "Hujan Lebat"])
plt.xlabel("Kondisi Cuaca")
plt.ylabel("Rata-rata Penyewaan Sepeda")
plt.title("Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
fig.tight_layout()
st.pyplot(fig)

st.write("### Perbandingan Penyewaan Sepeda pada Hari Kerja dan Akhir Pekan")
workingday_agg = df_filtered.groupby("workingday")["cnt"].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=workingday_agg["workingday"], y=workingday_agg["cnt"], ax=ax, palette="pastel")
ax.set_xticks([0, 1])
ax.set_xticklabels(["Akhir Pekan / Libur", "Hari Kerja"])
plt.xlabel("Jenis Hari")
plt.ylabel("Rata-rata Penyewaan Sepeda")
plt.title("Penyewaan Sepeda Berdasarkan Jenis Hari")
fig.tight_layout()
st.pyplot(fig)

st.write("### Sumber Data")
st.write("Data diambil dari sistem Bike Sharing Washington D.C. (2011-2012).")