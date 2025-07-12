import csv
from collections import deque
from datetime import datetime

# Nama file CSV
FILE_NAME = 'transaksi.csv'

# Struktur data
transaksi_list = []         # Menyimpan semua data dari file
transaksi_queue = deque()   # Antrian untuk data baru

# Fungsi untuk memuat data dari file CSV ke dalam list
def load_data():
    try:
        with open(FILE_NAME, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transaksi_list.append(row)
    except FileNotFoundError:
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['tanggal', 'jenis', 'jumlah', 'kategori'])

# Fungsi untuk menyimpan transaksi baru dari queue ke file CSV
def simpan_data():
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        while transaksi_queue:
            transaksi = transaksi_queue.popleft()
            writer.writerow([transaksi['tanggal'], transaksi['jenis'], transaksi['jumlah'], transaksi['kategori']])
            transaksi_list.append(transaksi)
    print("✅ Transaksi baru telah disimpan ke file.")

# Fungsi untuk menambahkan transaksi baru
def tambah_transaksi():
    tanggal = datetime.now().strftime('%Y-%m-%d')
    jenis = input("Jenis transaksi (pemasukan/pengeluaran): ").lower()
    jumlah = input("Jumlah (angka): ")
    kategori = input("Kategori: ")

    transaksi = {
        'tanggal': tanggal,
        'jenis': jenis,
        'jumlah': jumlah,
        'kategori': kategori
    }

    transaksi_queue.append(transaksi)
    print("🔃 Transaksi dimasukkan ke dalam antrian. Gunakan opsi 'Simpan Transaksi' untuk menyimpan ke file.")

# Fungsi untuk menampilkan semua transaksi
def tampilkan_transaksi():
    if not transaksi_list:
        print("⚠️  Tidak ada data transaksi.")
        return
    print("\n=== Daftar Transaksi ===")
    for t in transaksi_list:
        print(f"{t['tanggal']} | {t['jenis']} | Rp{t['jumlah']} | {t['kategori']}")

# Fungsi untuk menampilkan laporan berdasarkan bulan/tahun
def laporan_bulanan():
    bulan = input("Masukkan bulan (contoh: 07): ")
    tahun = input("Masukkan tahun (contoh: 2025): ")
    total_pemasukan = 0
    total_pengeluaran = 0

    for t in transaksi_list:
        tgl = t['tanggal']
        if tgl[5:7] == bulan and tgl[0:4] == tahun:
            jumlah = int(t['jumlah'])
            if t['jenis'] == 'pemasukan':
                total_pemasukan += jumlah
            elif t['jenis'] == 'pengeluaran':
                total_pengeluaran += jumlah

    print(f"\n📊 Laporan Bulan {bulan}-{tahun}")
    print(f"Total Pemasukan  : Rp{total_pemasukan}")
    print(f"Total Pengeluaran: Rp{total_pengeluaran}")
    print(f"Saldo Bulan Ini  : Rp{total_pemasukan - total_pengeluaran}")

# Menu utama
def menu():
    load_data()
    while True:
        print("\n=== APLIKASI KEUANGAN PRIBADI ===")
        print("1. Tambah Transaksi")
        print("2. Simpan Transaksi (ke file)")
        print("3. Lihat Daftar Transaksi")
        print("4. Laporan Bulanan")
        print("5. Keluar")
        pilihan = input("Pilih menu (1-5): ")

        if pilihan == '1':
            tambah_transaksi()
        elif pilihan == '2':
            simpan_data()
        elif pilihan == '3':
            tampilkan_transaksi()
        elif pilihan == '4':
            laporan_bulanan()
        elif pilihan == '5':
            print("👋 Keluar dari program.")
            break
        else:
            print("❌ Pilihan tidak valid.")

# Jalankan program
if __name__ == "__main__":
    menu()
