# Bike Sharing Dashboard 🚴‍♂️✨

Dashboard ini dibuat untuk menganalisis pola penyewaan sepeda berdasarkan musim, cuaca, dan jenis hari (kerja/libur) menggunakan dataset dari sistem Bike Sharing Washington D.C.

## 📂 Struktur Folder

```
submission
├───dashboard
│   ├───dashboard.py
├───data
│   ├───data_1.csv
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## 🛠 Setup Environment - Anaconda

Jika menggunakan **Anaconda**, jalankan perintah berikut untuk membuat environment baru:

```
conda create --name bike-sharing python=3.9
conda activate bike-sharing
pip install -r requirements.txt
```

## 🛠 Setup Environment - Shell/Terminal

Jika **tidak menggunakan Anaconda**, jalankan perintah berikut:

```
mkdir bike_sharing_dashboard
cd bike_sharing_dashboard
pipenv install
pipenv shell
pip install -r requirements.txt
```

## 🚀 Jalankan Aplikasi Streamlit

Setelah environment siap, jalankan aplikasi **Streamlit** dengan perintah:

```
streamlit run dashboard/dashboard.py
```

Buka browser dan akses **`http://localhost:8501/`** untuk melihat dashboard.

## 🌐 (Opsional) Deploy ke Streamlit Cloud

1. **Upload proyek ke GitHub.**
2. **Buka [Streamlit Cloud](https://share.streamlit.io/) dan deploy dari repository GitHub.**
3. **Simpan link dashboard di file `url.txt`.**

## 📌 Catatan

- Dataset yang digunakan (`data_1.csv`, `data_1.csv`) berasal dari sistem Bike Sharing Washington D.C. tahun **2011-2012**.
- Semua dependensi terdapat dalam **`requirements.txt`**.
