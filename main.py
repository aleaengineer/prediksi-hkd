import csv
from collections import Counter
import random
import pandas as pd

# --- Konfigurasi File ---
NAMA_FILE = 'histori.csv'     # Nama file histori
KOLOM_ANGKA = 'Nomor'         # Kolom angka 5 digit
DELIMITER = ';'               # Delimiter CSV

# --- Fungsi Baca Data ---
def baca_data_csv(file_path, kolom, delimiter=';'):
    df = pd.read_csv(file_path, sep=delimiter)
    angka = df[kolom].astype(str).str.zfill(5)
    angka = angka[angka.str.match(r'^\d{5}$')].tolist()
    return angka

# --- Fungsi Posisi & Frekuensi ---
def pecah_posisi(data):
    return (
        [x[0] for x in data],  # AS
        [x[1] for x in data],  # KOP
        [x[2] for x in data],  # KEPALA
        [x[4] for x in data],  # EKOR
    )

def top_n_frekuensi(pos_list, n=3):
    return [item for item, _ in Counter(pos_list).most_common(n)]

# --- Fungsi Buat Prediksi ---
def buat_prediksi(as_list, kop_list, kepala_list, ekor_list, jumlah=5):
    prediksi = set()
    while len(prediksi) < jumlah:
        as_ = random.choice(as_list)
        kop = random.choice(kop_list)
        kepala = random.choice(kepala_list)
        ekor = random.choice(ekor_list)
        tengah = random.randint(0, 9)  # Digit ke-4 acak
        angka = f"{as_}{kop}{kepala}{tengah}{ekor}"
        prediksi.add(angka)
    return list(prediksi)

# --- Main ---
if __name__ == "__main__":
    try:
        data_histori = baca_data_csv(NAMA_FILE, KOLOM_ANGKA, DELIMITER)
        if len(data_histori) < 10:
            print("⚠️ Data terlalu sedikit. Tambahkan lebih banyak histori.")
        else:
            as_, kop_, kepala_, ekor_ = pecah_posisi(data_histori)
            prediksi = buat_prediksi(
                top_n_frekuensi(as_),
                top_n_frekuensi(kop_),
                top_n_frekuensi(kepala_),
                top_n_frekuensi(ekor_),
                jumlah=5
            )

            print("\n🔮 Prediksi Harian (AS-KOP-KEPALA-EKOR):")
            for angka in prediksi:
                print("➡️", angka)

    except Exception as e:
        print("❌ Terjadi kesalahan:", e)
