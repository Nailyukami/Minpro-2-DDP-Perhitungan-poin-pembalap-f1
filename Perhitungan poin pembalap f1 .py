import math
import pwinput





daftar_pembalap = {
    1: {"nama": "George Russell", "tim": "Mercedes"},
    2: {"nama": "Max Verstappen", "tim": "Red Bull Racing"},
    3: {"nama": "Lewis Hamilton", "tim": "Ferrari"},
    4: {"nama": "Lando Norris", "tim": "McLaren"},
    5: {"nama": "Oscar Piastri", "tim": "McLaren"},
    6: {"nama": "Isack Hadjar", "tim": "Red Bull Racing"},
    7: {"nama": "Pierre Gasly", "tim": "Alpine"},
    8: {"nama": "Liam Lawson", "tim": "Racing Bulls"},
    9: {"nama": "Charles Leclerc", "tim": "Ferrari"},
    10: {"nama": "Kimi Antonelli", "tim": "Mercedes"}
}


poin_posisi = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# Dictionary akun: username -> password dan role
akun = {
    "admin": {"password": "admin123", "role": "admin"},
    "nailyukami": {"password": "user456", "role": "user"}
}

# List berisi dictionary hasil balapan
data_balapan = []


# ------------------------------------------------------------
# FUNGSI VALIDASI INPUT
# ------------------------------------------------------------
def input_angka(pesan, minimal, maksimal):
    while True:
        teks = input(pesan)
        if teks == "":
            print("Input tidak boleh kosong!")
        elif not teks.isdigit():
            print("Input harus berupa angka!")
        else:
            angka = int(teks)
            if angka < minimal or angka > maksimal:
                print("Angka harus antara " + str(minimal) + " sampai " + str(maksimal) + "!")
            else:
                return angka


def input_teks(pesan):
    while True:
        teks = input(pesan)
        if teks == "":
            print("Input tidak boleh kosong!")
        else:
            return teks



def tampil_pembalap():
    print("\nDaftar Pembalap")
    for nomor in daftar_pembalap:
        print(str(nomor) + ". " + daftar_pembalap[nomor]["nama"] + " (" + daftar_pembalap[nomor]["tim"] + ")")


def tampil_hasil():
    print("\nSeluruh Data Hasil Balapan")
    if len(data_balapan) == 0:
        print("Belum ada data hasil balapan.")
        return False
    for data in data_balapan:
        nomor = data["nomor"]
        print("ID " + str(data["id"]) + " | " + data["balapan"] + " | " +
              daftar_pembalap[nomor]["nama"] + " - " + daftar_pembalap[nomor]["tim"] +
              " | Posisi: " + str(data["posisi"]) + " | Poin: " + str(data["poin"]))
    return True


def tampil_klasemen():
    print("\nKlasemen Total Poin")
    klasemen = []
    for nomor in daftar_pembalap:
        total = 0
        jumlah = 0
        for data in data_balapan:
            if data["nomor"] == nomor:
                total = total + data["poin"]
                jumlah = jumlah + 1
        klasemen.append([nomor, total, jumlah])

    # urutkan dari poin terbesar (bubble sort)
    for i in range(len(klasemen)):
        for j in range(len(klasemen) - 1 - i):
            if klasemen[j][1] < klasemen[j + 1][1]:
                sementara = klasemen[j]
                klasemen[j] = klasemen[j + 1]
                klasemen[j + 1] = sementara

    peringkat = 1
    for item in klasemen:
        nomor = item[0]
        total = item[1]
        jumlah = item[2]
        if jumlah > 0:
            rata = math.ceil(total / jumlah)  # library math
        else:
            rata = 0
        print(str(peringkat) + ". " + daftar_pembalap[nomor]["nama"] + " (" +
              daftar_pembalap[nomor]["tim"] + ") : " + str(total) + " poin | " +
              "Rata-rata: " + str(rata) + " poin/balapan")
        peringkat = peringkat + 1



def cek_duplikat(balapan, nomor, posisi, id_abaikan):
    for data in data_balapan:
        if data["id"] != id_abaikan and data["balapan"].lower() == balapan.lower():
            if data["nomor"] == nomor:
                return "Pembalap ini sudah punya hasil di balapan tersebut!"
            if data["posisi"] == posisi:
                return "Posisi ini sudah ditempati pembalap lain di balapan tersebut!"
    return ""


def cari_hasil(id_hasil):
    for data in data_balapan:
        if data["id"] == id_hasil:
            return data
    return None


def tambah_hasil():
    print("\nTambah Hasil Balapan")
    tampil_pembalap()
    nomor = input_angka("Masukkan nomor pembalap: ", 1, len(daftar_pembalap))
    balapan = input_teks("Masukkan nama balapan (contoh: GP Monaco): ")
    posisi = input_angka("Masukkan posisi finish (1-10): ", 1, 10)

    pesan = cek_duplikat(balapan, nomor, posisi, 0)
    if pesan != "":
        print(pesan)
        return

    id_baru = 1
    for data in data_balapan:
        if data["id"] >= id_baru:
            id_baru = data["id"] + 1

    poin = poin_posisi[posisi]
    data_baru = {"id": id_baru, "balapan": balapan, "nomor": nomor, "posisi": posisi, "poin": poin}
    data_balapan.append(data_baru)
    print("Data berhasil ditambahkan!")
    print("Pembalap:", daftar_pembalap[nomor]["nama"])
    print("Tim:", daftar_pembalap[nomor]["tim"])
    print("Posisi:", posisi)
    print("Poin:", poin)


def ubah_hasil():
    print("\nUbah Hasil Balapan")
    if tampil_hasil() == False:
        return
    id_hasil = input_angka("Masukkan ID yang diubah: ", 1, 100000)
    data = cari_hasil(id_hasil)
    if data == None:
        print("ID tidak ditemukan!")
        return

    posisi = input_angka("Masukkan posisi finish baru (1-10): ", 1, 10)
    pesan = cek_duplikat(data["balapan"], data["nomor"], posisi, data["id"])
    if pesan != "":
        print(pesan)
        return

    data["posisi"] = posisi
    data["poin"] = poin_posisi[posisi]
    print("Data berhasil diubah!")


def hapus_hasil():
    print("\nHapus Hasil Balapan")
    if tampil_hasil() == False:
        return
    id_hasil = input_angka("Masukkan ID yang dihapus: ", 1, 100000)
    data = cari_hasil(id_hasil)
    if data == None:
        print("ID tidak ditemukan!")
        return

    yakin = input("Yakin ingin menghapus? (y/n): ")
    if yakin == "y" or yakin == "Y":
        data_balapan.remove(data)
        print("Data berhasil dihapus!")
    elif yakin == "n" or yakin == "N":
        print("Penghapusan dibatalkan.")
    else:
        print("Pilihan tidak valid, penghapusan dibatalkan.")


# ------------------------------------------------------------
# FUNGSI LOGIN & REGISTRASI
# ------------------------------------------------------------
def login():
    print("\nLOGIN")
    percobaan = 0
    while percobaan < 3:
        username = input_teks("Username: ")
        password = pwinput.pwinput("Password: ")  # library pwinput
        if username in akun and akun[username]["password"] == password:
            print("Login berhasil! Selamat datang, " + username)
            return akun[username]["role"]
        percobaan = percobaan + 1
        print("Username atau password salah! (" + str(percobaan) + "/3)")
    print("Terlalu banyak percobaan gagal.")
    return None


def registrasi():
    print("\nREGISTRASI AKUN USER")
    username = input_teks("Username baru: ")
    if username in akun:
        print("Username sudah dipakai!")
        return
    password = pwinput.pwinput("Password baru (minimal 6 karakter): ")
    if len(password) < 6:
        print("Password minimal 6 karakter!")
        return
    akun[username] = {"password": password, "role": "user"}
    print("Registrasi berhasil! Silakan login.")


# ------------------------------------------------------------
# MENU PER ROLE
# ------------------------------------------------------------
def menu_admin():
    aktif = True
    while aktif:
        print("\nMENU ADMIN")
        print("1. Tambah Hasil Balapan")
        print("2. Tampilkan Hasil Balapan")
        print("3. Tampilkan Klasemen")
        print("4. Ubah Hasil Balapan")
        print("5. Hapus Hasil Balapan")
        print("6. Logout")
        pilihan = input("Masukkan pilihan: ")
        if pilihan == "1":
            tambah_hasil()
        elif pilihan == "2":
            tampil_hasil()
        elif pilihan == "3":
            tampil_klasemen()
        elif pilihan == "4":
            ubah_hasil()
        elif pilihan == "5":
            hapus_hasil()
        elif pilihan == "6":
            print("Logout")
            aktif = False
        else:
            print("Pilihan tidak valid!")


def menu_user():
    aktif = True
    while aktif:
        print("\nMENU USER")
        print("1. Tampilkan Hasil Balapan")
        print("2. Tampilkan Klasemen")
        print("3. Logout")
        pilihan = input("Masukkan pilihan: ")
        if pilihan == "1":
            tampil_hasil()
        elif pilihan == "2":
            tampil_klasemen()
        elif pilihan == "3":
            print("Logout")
            aktif = False
        else:
            print("Pilihan tidak valid!")



def main():
    print("SISTEM PERHITUNGAN POIN PEMBALAP F1")
    lanjut = True
    while lanjut == True:
        print("\n1. Login")
        print("2. Registrasi")
        print("3. Keluar")
        pilihan = input("Masukkan pilihan: ")
        if pilihan == "1":
            role = login()
            if role == "admin":
                menu_admin()
            elif role == "user":
                menu_user()
        elif pilihan == "2":
            registrasi()
        elif pilihan == "3":
            print("Keluar")
            lanjut = False
        else:
            print("Pilihan tidak valid!")


main()