import streamlit as st
import pandas as pd
import random
from collections import Counter
from datetime import datetime

# --- Fungsi Utility ---
def pecah_posisi(data):
    return (
        [x[0] for x in data],
        [x[1] for x in data],
        [x[2] for x in data],
        [x[4] for x in data],
    )

def top_n_frekuensi(pos_list, n=3):
    return [item for item, _ in Counter(pos_list).most_common(n)]

def buat_prediksi(as_list, kop_list, kepala_list, ekor_list, jumlah=5):
    prediksi = set()
    while len(prediksi) < jumlah:
        as_ = random.choice(as_list)
        kop = random.choice(kop_list)
        kepala = random.choice(kepala_list)
        ekor = random.choice(ekor_list)
        tengah = random.randint(0, 9)
        angka = f"{as_}{kop}{kepala}{tengah}{ekor}"
        prediksi.add(angka)
    return list(prediksi)

def tampilkan_frekuensi(pos_list, label):
    freq = Counter(pos_list)
    df = pd.DataFrame(freq.items(), columns=['Digit', 'Frekuensi']).sort_values(by='Frekuensi', ascending=False)
    st.dataframe(df.set_index('Digit'), height=250)

# --- Streamlit UI ---
st.set_page_config(page_title="Prediksi Harian AS-KOP-KEPALA-EKOR", layout="centered")
st.title("🔮 Prediksi Harian (AS-KOP-KEPALA-EKOR)")
st.caption("Upload file histori 5 digit (CSV, delimiter `;`)")

uploaded_file = st.file_uploader("Unggah file histori.csv", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, sep=';')
        if 'Nomor' not in df.columns:
            st.error("❌ Kolom 'Nomor' tidak ditemukan.")
        else:
            df['Nomor'] = df['Nomor'].astype(str).str.zfill(5)
            nomor_list = df['Nomor'][df['Nomor'].str.match(r'^\d{5}$')].tolist()

            if len(nomor_list) < 10:
                st.warning("⚠️ Data terlalu sedikit.")
            else:
                as_, kop_, kepala_, ekor_ = pecah_posisi(nomor_list)

                st.subheader("📊 Frekuensi Angka per Posisi")
                col1, col2 = st.columns(2)
                with col1:
                    tampilkan_frekuensi(as_, "AS")
                    tampilkan_frekuensi(kop_, "KOP")
                with col2:
                    tampilkan_frekuensi(kepala_, "KEPALA")
                    tampilkan_frekuensi(ekor_, "EKOR")

                jumlah_prediksi = st.slider("Jumlah angka prediksi", 1, 20, 5)
                if st.button("🔁 Generate Prediksi"):
                    prediksi = buat_prediksi(
                        top_n_frekuensi(as_),
                        top_n_frekuensi(kop_),
                        top_n_frekuensi(kepala_),
                        top_n_frekuensi(ekor_),
                        jumlah=jumlah_prediksi
                    )
                    st.success(f"🎯 Prediksi Tanggal {datetime.today().strftime('%Y-%m-%d')}")
                    for angka in prediksi:
                        st.write(f"➡️ {angka}")

                    # Simpan ke CSV
                    prediksi_df = pd.DataFrame({'Prediksi': prediksi})
                    csv_output = prediksi_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Hasil (.csv)",
                        data=csv_output,
                        file_name=f"prediksi_{datetime.today().strftime('%Y%m%d')}.csv",
                        mime='text/csv'
                    )
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
