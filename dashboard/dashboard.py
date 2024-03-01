import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_sum_rental_df(df):
    sum_rental_df = df.reset_index()
    sum_rental_df.rename(columns={
        "cnt_hourly": "total_rental",
        "registered_hourly": "registered_user",
    }, inplace=True)
    return sum_rental_df

df = pd.read_csv("dashboard/df_bike.csv")

# Filter data
df['dteday'] = pd.to_datetime(df['dteday'])
min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?q=80&w=3540&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
# submission code
st.header('Bike Sharing Dashboard :sparkles:')

col1, col2 = st.columns(2)

with col1:
    total_orders_df = create_sum_rental_df(df)
    total_orders = total_orders_df.total_rental.sum()
    st.metric("Total Bike Sharing", value=total_orders)

with col2:
    registeredUser_df = create_sum_rental_df(df)
    registeredUser = registeredUser_df.registered_user.sum()
    st.metric("Total Registered", value=registeredUser)

seasonal_data = df.groupby('season_daily')['cnt_daily'].mean()
season_names = ['Spring', 'Summer', 'Fall', 'Winter']

# Menampilkan grafik menggunakan Streamlit
st.write("## Jumlah Sewa Sepeda Harian per Musim")
plt.figure(figsize=(8, 6))
plt.bar(season_names, seasonal_data, color=['lightgreen', 'gold', 'orange', 'lightblue'])
plt.xlabel('Musim')
plt.ylabel('Rata-rata Jumlah Sewa Harian')
plt.title('Jumlah Sewa Sepeda Harian per Musim')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(range(4), season_names)  # Mengatur label sumbu x sesuai season_names
st.pyplot(plt)

seasonal_data_hour = df.groupby('season_hourly')['cnt_hourly'].mean()

# Menampilkan grafik menggunakan Streamlit
st.write("## Jumlah Sewa Sepeda per jam")
plt.figure(figsize=(8, 6))
plt.bar(season_names, seasonal_data, color=['lightgreen', 'gold', 'orange', 'lightblue'])
plt.xlabel('Musim')
plt.ylabel('Rata-rata Jumlah Sewa per jam dalam semusim')
plt.title('Jumlah Sewa Sepeda per jam dalam semusim')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(range(4), season_names)  # Mengatur label sumbu x sesuai season_names
st.pyplot(plt)

# Menampilkan kedua grafik secara bersebelahan
st.write("## Pola Jumlah Sewa Sepeda Harian Berdasarkan Bulan dan Jam")
sns.set_style("whitegrid")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 6))

sns.lineplot(x="mnth_daily", y="cnt_daily", data=df, color='skyblue', ax=ax1)
ax1.set_title("Pola Jumlah Sewa Sepeda Harian Berdasarkan Bulan")
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Jumlah Sewa Sepeda Harian")
ax1.set_xticks(range(1, 13))
ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

sns.lineplot(x="hr", y="cnt_hourly", data=df, color='orange', ax=ax2)
ax2.set_title("Pola Jumlah Sewa Sepeda Harian Berdasarkan Jam")
ax2.set_xlabel("Jam")
ax2.set_ylabel("Jumlah Sewa Sepeda Harian")
ax2.set_xticks(range(24))
ax2.grid(axis='both', linestyle='--', alpha=0.5)
st.pyplot(fig)

# Menampilkan grafik menggunakan Streamlit
st.write("## Pengaruh Cuaca Terhadap Jumlah Sewa Sepeda Harian")
plt.figure(figsize=(12, 8))
avg_weather = df.groupby('weather_label')['cnt_daily'].mean().reset_index().sort_values("cnt_daily")
sns.barplot(x="weather_label", y="cnt_daily", data=avg_weather, estimator=sum)
plt.title("Pengaruh Cuaca Terhadap Jumlah Sewa Sepeda Harian", fontsize=16)
plt.xlabel("Cuaca", fontsize=14)
plt.ylabel("Total Jumlah Sewa Sepeda Harian", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--')
st.pyplot(plt)

# Menampilkan grafik menggunakan Streamlit
st.write("## Perbandingan Hari Sewa Sepeda Setiap Hari ")
plt.figure(figsize=(8, 5))
sns.barplot(x='weekday_daily', y='cnt_daily', data=df, palette='Set1')
plt.title('Rata-rata Penyewaan Sepeda Setiap Hari')
plt.xlabel('Hari')
plt.ylabel('Rata-rata Penyewaan')
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
st.pyplot(plt)

st.caption('Copyright © Izza 2024')