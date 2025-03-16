import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('dashboard/main_data.csv')

st.title("Dashboard Penyewaan Sepeda 🚴‍♂️")

st.sidebar.header("Filter Data")

start_date = st.sidebar.date_input("Tanggal Mulai", df['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Selesai", df['dteday'].max())

seasons = df['season'].unique()
seasons = sorted(seasons)
selected_season = st.sidebar.selectbox("Pilih Musim", ["Semua Musim"] + list(seasons))

season_map = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}
if selected_season != "Semua Musim":
    st.sidebar.write(f"Musim {selected_season}: {season_map[selected_season]}")
else:
    st.sidebar.write("Semua Musim")

weathersits = sorted(df['weathersit'].unique())
selected_weathersit = st.sidebar.selectbox("Pilih Cuaca", ["Semua Cuaca"] + list(weathersits))

weather_map = {
    1: "Cerah",
    2: "Berawan",
    3: "Hujan",
}
if selected_weathersit != "Semua Cuaca":
    st.sidebar.write(f"Cuaca {selected_weathersit}: {weather_map[selected_weathersit]}")
else:
    st.sidebar.write("Semua Cuaca")

filtered_df = df[
    (df['dteday'] >= str(start_date)) & 
    (df['dteday'] <= str(end_date))
]

if selected_season != "Semua Musim":
    filtered_df = filtered_df[filtered_df['season'] == selected_season]

if selected_weathersit != "Semua Cuaca":
    filtered_df = filtered_df[filtered_df['weathersit'] == selected_weathersit]

st.subheader("Tinjauan Data Semua")
st.write("Berikut adalah sampel data yang digunakan untuk analisis:")
st.write(df.head())
st.write(f"Jumlah data keseluruhan: {df.shape[0]} baris dan {df.shape[1]} kolom")

st.subheader("Tinjauan Data Terfilter")
st.write("Berikut adalah sampel data yang digunakan untuk analisis setelah difilter:")
st.write(filtered_df.head())
st.write(f"Jumlah data setelah difilter: {filtered_df.shape[0]} baris dan {filtered_df.shape[1]} kolom")

st.write("Cari data dari dataset keseluruhan dengan menggunakan fitur pencarian berikut")
search_column = st.selectbox("Pilih Kolom untuk Pencarian", df.columns)
search_value = st.text_input(f"Masukkan nilai untuk pencarian di kolom {search_column}:")

if search_value:
    search_filtered_df = filtered_df[filtered_df[search_column].astype(str).str.contains(search_value, case=False)]
    st.write(f"Data yang ditemukan ({search_filtered_df.shape[0]} hasil):")
    st.write(search_filtered_df)
else:
    st.write("Masukkan nilai untuk pencarian di kolom yang dipilih.")

st.write("""
    Di bagian ini, dapat dilihat sekilas data penyewaan sepeda yang digunakan untuk analisis. 
    Disini dapat dicari data dari seluruh dataset berdasarkan kolom yang tersedia, 
    seperti tanggal, suhu, kecepatan angin, musim, dan sebagainya.
""")

st.subheader("Distribusi Jumlah Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10,5))
sns.histplot(filtered_df['cnt'], bins=30, kde=True, ax=ax)
ax.set_title("Distribusi Penyewaan Sepeda")
ax.set_xlabel("Jumlah Penyewaan Sepeda")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)

st.write("""
    Grafik di atas menunjukkan frekuensi jumlah penyewaan sepeda dalam berbagai rentang angka.
    Sebagian besar hari memiliki jumlah penyewaan yang berada di tengah, tidak terlalu sedikit atau terlalu banyak.
    Bentuk grafik juga mengindikasikan kemungkinan adanya beberapa hari dengan jumlah penyewaan yang sangat tinggi atau sangat rendah, yang dapat dipengaruhi oleh faktor seperti acara khusus atau musim.
""")

st.subheader("Pengaruh Musim dan Cuaca terhadap Rata-Rata Penyewaan Sepeda")
season_weather_agg = filtered_df.groupby(['season', 'weathersit'])['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x='season', y='cnt', hue='weathersit', data=season_weather_agg, ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim dan Cuaca")
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Jumlah Penyewaan Sepeda")
ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
st.pyplot(fig)

st.write("""
    Grafik ini menunjukkan pengaruh musim dan cuaca terhadap penyewaan sepeda.
    Musim panas dan gugur cenderung memiliki lebih banyak penyewaan sepeda, terutama saat cuaca cerah 
    dan suhu lebih nyaman. Sebaliknya, pada musim dingin dan cuaca buruk, jumlah penyewaan sepeda berkurang secara signifikan. 
""")

st.subheader("Perbandingan Rata-Rata Penyewaan Sepeda pada Hari Kerja dan Akhir Pekan")

filtered_df['weekday'] = pd.to_datetime(filtered_df['dteday']).dt.weekday
filtered_df['is_weekend'] = filtered_df['weekday'].isin([5, 6])
weekend_agg = filtered_df.groupby('is_weekend')['cnt'].mean().reset_index()
weekend_agg['is_weekend'] = weekend_agg['is_weekend'].replace({True: "Akhir Pekan", False: "Hari Kerja"})

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x="is_weekend", y="cnt", data=weekend_agg, ax=ax)
ax.set_title("Perbandingan Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
ax.set_xlabel("Kategori Hari")
ax.set_ylabel("Rata-rata Jumlah Penyewaan Sepeda")
st.pyplot(fig)

st.write("""
    Grafik ini menunjukkan perbandingan antara penyewaan sepeda pada hari kerja dan akhir pekan. 
    Secara umum, penyewaan sepeda lebih banyak terjadi pada hari kerja dibandingkan akhir pekan. 
""")

st.subheader("Perbandingan Tren Penggunaan Sepeda Pada Hari Kerja dan Akhir Pekan pada Tahun 2011 dan 2012")

filtered_df['year_month'] = pd.to_datetime(filtered_df['dteday']).dt.to_period('M')

weekend_trend = filtered_df.groupby(["year_month", "is_weekend"])["cnt"].sum().reset_index()
weekend_trend["year_month"] = weekend_trend["year_month"].astype(str)

plt.figure(figsize=(15,5))
sns.lineplot(x="year_month", y="cnt", hue="is_weekend", data=weekend_trend)
plt.title("Tren Penyewaan Sepeda: Hari Kerja vs Akhir Pekan pada Tahun 2011 dan 2012")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.xticks(rotation=45)
st.pyplot(plt)

st.write("""
    Grafik ini menggambarkan tren penyewaan sepeda antara hari kerja dan akhir pekan berdasarkan bulan.
    Dari grafik ini, kita dapat melihat perbandingan jumlah penyewaan sepeda pada hari kerja dan akhir pekan sepanjang tahun.
""")