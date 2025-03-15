import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('dashboard/main_data.csv')

st.title("Dashboard Penyewaan Sepeda 🚴‍♂️")

st.sidebar.header("Navigasi")
option = st.sidebar.selectbox("Pilih Analisis:", ["Data Overview", "Pengaruh Cuaca dan Musim", "Perbandingan Hari Kerja dan Akhir Pekan", "Tren Penyewaan Sepeda"])

if option == "Data Overview":
    st.subheader("Tinjauan Data")
    st.write("Berikut adalah sampel data yang digunakan untuk analisis:")
    st.write(df.head())
    st.write(f"Jumlah data: {df.shape[0]} baris dan {df.shape[1]} kolom")
    
    st.write("Cari data dari dataset keseluruhan dengan menggunakan fitur pencarian berikut")
    search_column = st.selectbox("Pilih Kolom untuk Pencarian", df.columns)
    search_value = st.text_input(f"Masukkan nilai untuk pencarian di kolom {search_column}:")
    
    if search_value:
        filtered_df = df[df[search_column].astype(str).str.contains(search_value, case=False)]
        st.write(f"Data yang ditemukan ({filtered_df.shape[0]} hasil):")
        st.write(filtered_df)
    else:
        st.write("Masukkan nilai untuk pencarian di kolom yang dipilih.")
    
    st.write("""
        Di bagian ini, dapat dilihat sekilas data penyewaan sepeda yang digunakan untuk analisis. 
        Disini dapat dicari data dari seluruh dataset berdasarkan kolom yang tersedia, 
        seperti tanggal, suhu, kecepatan angin, musim, dan sebagainya.
                 
        Penyewaan sepeda terpengaruh oleh banyak faktor, termasuk kondisi cuaca, hari dalam minggu, 
        dan bahkan waktu dalam sehari. Fitur pencarian memungkinkan Anda untuk mengeksplorasi data lebih lanjut 
        sesuai kebutuhan dan mendapatkan wawasan lebih mendalam dari informasi yang tersedia.
    """)
    
    st.subheader("Distribusi Jumlah Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.histplot(df['cnt'], bins=30, kde=True, ax=ax)
    ax.set_title("Distribusi Penyewaan Sepeda")
    ax.set_xlabel("Jumlah Penyewaan Sepeda")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)
    
    st.write("""
        Grafik di atas menunjukkan frekuensi jumlah penyewaan sepeda dalam berbagai rentang angka.
        Sebagian besar hari memiliki jumlah penyewaan yang berada di tengah, tidak terlalu sedikit atau terlalu banyak.
        Bentuk grafik juga mengindikasikan kemungkinan adanya beberapa hari dengan jumlah penyewaan yang sangat tinggi atau sangat rendah, yang dapat dipengaruhi oleh faktor seperti acara khusus atau musim.
        Secara keseluruhan, penyewaan sepeda lebih sering terjadi dalam jumlah sedang, sedangkan jumlah yang sangat rendah atau sangat tinggi jarang terjadi.
    """)

    st.write("#### Sumber Data")
    st.write("Data diambil dari sistem Bike Sharing Washington D.C. (2011-2012).")

if option == "Pengaruh Cuaca dan Musim":
    st.subheader("Pengaruh Musim dan Cuaca terhadap Rata Rata Penyewaan Sepeda pada Tahun 2011 dan 2012")
    
    season_weather_agg = df.groupby(['season', 'weathersit'])['cnt'].mean().reset_index()
    
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
        Analisis ini dapat membantu dalam perencanaan armada sepeda serta promosi sesuai dengan kondisi cuaca yang ada.
    """)

if option == "Perbandingan Hari Kerja dan Akhir Pekan":
    st.subheader("Perbandingan Rata-Rata Penyewaan Sepeda pada Hari Kerja dan Akhir Pekan")
    
    df['weekday'] = pd.to_datetime(df['dteday']).dt.weekday
    df['is_weekend'] = df['weekday'].isin([5, 6])
    weekend_agg = df.groupby('is_weekend')['cnt'].mean().reset_index()
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
        Ini mungkin karena pengguna sepeda cenderung menggunakannya untuk keperluan transportasi harian seperti perjalanan menuju tempat kerja atau sekolah.
    """)

if option == "Tren Penyewaan Sepeda":
    st.subheader("Perbandingan Tren Penggunaan Sepeda Pada Hari Kerja dan Akhir Pekan pada Tahun 2011 dan 2012")

    df['weekday'] = pd.to_datetime(df['dteday']).dt.weekday
    df['is_weekend'] = df['weekday'].isin([5, 6])

    df['year_month'] = pd.to_datetime(df['dteday']).dt.to_period('M')

    weekend_trend = df.groupby(["year_month", "is_weekend"])["cnt"].sum().reset_index()
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
        Secara umum, penyewaan sepeda lebih banyak terjadi pada hari kerja, dengan jumlah penyewaan yang lebih rendah pada akhir pekan.
        Ini bisa disebabkan oleh faktor-faktor seperti penggunaan sepeda untuk transportasi harian di hari kerja dan kurangnya kebutuhan di akhir pekan.
    """)