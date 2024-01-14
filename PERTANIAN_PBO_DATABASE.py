import mysql.connector

# Kelas untuk Database (CRUD)
class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="",  
            database="5220411239"
        )
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Tabel untuk PertanianUmum
        self.cursor.execute("CREATE TABLE IF NOT EXISTS pertanian (id INT AUTO_INCREMENT PRIMARY KEY, luas_lahan VARCHAR(255), jumlah_tanaman INT, jenis_pupuk VARCHAR(255))")

        # Tabel untuk PertanianSayuran
        self.cursor.execute("CREATE TABLE IF NOT EXISTS pertanian_sayuran (id INT AUTO_INCREMENT PRIMARY KEY, jenis_sayuran VARCHAR(255), pertanian_id INT, FOREIGN KEY (pertanian_id) REFERENCES pertanian(id))")

        # Tabel untuk PertanianBuah
        self.cursor.execute("CREATE TABLE IF NOT EXISTS pertanian_buah (id INT AUTO_INCREMENT PRIMARY KEY, jenis_buah VARCHAR(255), pertanian_id INT, FOREIGN KEY (pertanian_id) REFERENCES pertanian(id))")

        self.connection.commit()

    def tambah_data_pertanian(self, pertanian):
        if isinstance(pertanian, Pertanian):
            self.cursor.execute("INSERT INTO pertanian (luas_lahan, jumlah_tanaman, jenis_pupuk) VALUES (%s, %s, %s)",
                                (pertanian.luas_lahan, pertanian.jumlah_tanaman, pertanian.jenis_pupuk))
            self.connection.commit()

            pertanian_id = self.cursor.lastrowid

            if isinstance(pertanian, PertanianSayuran):
                self.cursor.execute("INSERT INTO pertanian_sayuran (jenis_sayuran, pertanian_id) VALUES (%s, %s)",
                                    (pertanian.jenis_sayuran, pertanian_id))
            elif isinstance(pertanian, PertanianBuah):
                self.cursor.execute("INSERT INTO pertanian_buah (jenis_buah, pertanian_id) VALUES (%s, %s)",
                                    (pertanian.jenis_buah, pertanian_id))

            self.connection.commit()
            print("Data pertanian berhasil ditambahkan.")
        else:
            print("Objek yang ditambahkan bukan instance dari kelas Pertanian.")

    def tampilkan_data_pertanian(self):
        self.cursor.execute(
            "SELECT pertanian.id, pertanian.luas_lahan, pertanian.jumlah_tanaman, pertanian.jenis_pupuk, pertanian_sayuran.jenis_sayuran, pertanian_buah.jenis_buah FROM pertanian LEFT JOIN pertanian_sayuran ON pertanian.id = pertanian_sayuran.pertanian_id LEFT JOIN pertanian_buah ON pertanian.id = pertanian_buah.pertanian_id")
        data = self.cursor.fetchall()

        if not data:
            print("Tidak ada data pertanian.")
        else:
            for row in data:
                print(f"ID: {row[0]}, Luas Lahan: {row[1]}, Jumlah Tanaman: {row[2]}, Jenis Pupuk: {row[3]}")

                if row[4]:
                    print(f"Jenis Sayuran: {row[4]}")
                elif row[5]:
                    print(f"Jenis Buah: {row[5]}")

    def update_data_pertanian(self, id, luas_lahan, jumlah_tanaman, jenis_pupuk, jenis_tanaman):
        self.cursor.execute("UPDATE pertanian SET luas_lahan = %s, jumlah_tanaman = %s, jenis_pupuk = %s WHERE id = %s",
                            (luas_lahan, jumlah_tanaman, jenis_pupuk, id))

        if jenis_tanaman == 'sayuran':
            self.cursor.execute("UPDATE pertanian_sayuran SET jenis_sayuran = %s WHERE pertanian_id = %s",
                                (jenis_tanaman, id))
        elif jenis_tanaman == 'buah':
            self.cursor.execute("UPDATE pertanian_buah SET jenis_buah = %s WHERE pertanian_id = %s",
                                (jenis_tanaman, id))

        self.connection.commit()
        print("Data pertanian berhasil diupdate.")

    def hapus_data_pertanian(self, id):
        self.cursor.execute("DELETE FROM pertanian WHERE id = %s", (id,))
        self.connection.commit()
        print("Data pertanian berhasil dihapus.")

    def __del__(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except AttributeError:
            pass  


# Kelas Utama untuk Pertanian
class Pertanian:
    def __init__(self, luas_lahan, jumlah_tanaman, jenis_pupuk):
        self.luas_lahan = luas_lahan
        self.jumlah_tanaman = jumlah_tanaman
        self.jenis_pupuk = jenis_pupuk

    def get_info(self):
        return f"Lahan:{self.luas_lahan}, Tanaman:{self.jumlah_tanaman}, Pupuk:{self.jenis_pupuk}"

class PertanianSayuran(Pertanian):
    def __init__(self, luas_lahan, jumlah_tanaman, jenis_pupuk, jenis_sayuran):
        super().__init__(luas_lahan, jumlah_tanaman, jenis_pupuk)
        self.jenis_sayuran = jenis_sayuran

    def tampilkan_info(self):
        print(
            f"Pertanian sayuran dengan luas lahan {self.luas_lahan}, menggunakan pupuk {self.jenis_pupuk}, dan menanam {self.jumlah_tanaman} tanaman {self.jenis_sayuran}.")

class PertanianBuah(Pertanian):
    def __init__(self, luas_lahan, jumlah_tanaman, jenis_pupuk, jenis_buah):
        super().__init__(luas_lahan, jumlah_tanaman, jenis_pupuk)
        self.jenis_buah = jenis_buah

    def tampilkan_info(self):
        print(
            f"Pertanian buah dengan luas lahan {self.luas_lahan}, menggunakan pupuk {self.jenis_pupuk}, dan menanam {self.jumlah_tanaman} tanaman {self.jenis_buah}.")

# Buat subclass PertanianBuah yang mewarisi Pertanian
class PertanianBuah(Pertanian):
    def __init__(self, luas_lahan, jumlah_tanaman, jenis_pupuk, jenis_buah):
        super().__init__(luas_lahan, jumlah_tanaman, jenis_pupuk)
        self.jenis_buah = jenis_buah

    def tampilkan_info(self):
        print(
            f"Pertanian buah dengan luas lahan {self.luas_lahan}, menggunakan pupuk {self.jenis_pupuk}, dan menanam {self.jumlah_tanaman} tanaman {self.jenis_buah}.")


# Fungsi untuk menampilkan menu
def menu():
    print("\n===== Menu =====")
    print("1. Tambah Data Pertanian")
    print("2. Tampilkan Data Pertanian")
    print("3. Update Data Pertanian")
    print("4. Hapus Data Pertanian")
    print("5. Keluar")



db = Database()

while True:
    menu()
    choice = input("Pilih menu (1-5): ")

    if choice == '1':
        print("\n===== Jenis Pertanian =====")
        print("1. Pertanian Umum")
        print("2. Pertanian Sayuran")
        print("3. Pertanian Buah")
        jenis_pertanian = input("Pilih jenis pertanian [1-3]: ")

        luas_lahan = input("Masukkan luas lahan: ")
        jumlah_tanaman = input("Masukkan jumlah tanaman: ")
        jenis_pupuk = input("Masukkan jenis pupuk: ")

        if jenis_pertanian == '1':
            pertanian = Pertanian(luas_lahan, jumlah_tanaman, jenis_pupuk)
        elif jenis_pertanian == '2':
            jenis_sayuran = input("Masukkan jenis sayuran: ")
            pertanian = PertanianSayuran(luas_lahan, jumlah_tanaman, jenis_pupuk, jenis_sayuran)
        elif jenis_pertanian == '3':
            jenis_buah = input("Masukkan jenis buah: ")
            pertanian = PertanianBuah(luas_lahan, jumlah_tanaman, jenis_pupuk, jenis_buah)
        else:
            print("Jenis pertanian tidak valid.")

        db.tambah_data_pertanian(pertanian)
    elif choice == '2':
        db.tampilkan_data_pertanian()

    elif choice == '3':
        db.tampilkan_data_pertanian()
        id_pertanian = input("Masukkan ID pertanian yang ingin diupdate: ")
        luas_lahan_baru = input("Masukkan luas lahan baru: ")
        jumlah_tanaman_baru = input("Masukkan jumlah tanaman baru: ")
        jenis_pupuk_baru = input("Masukkan jenis pupuk baru: ")
        jenis_tanaman_baru = input("Masukkan jenis tanaman (sayuran/buah): ")

        db.update_data_pertanian(id_pertanian, luas_lahan_baru, jumlah_tanaman_baru, jenis_pupuk_baru, jenis_tanaman_baru)

    elif choice == '4':
        db.tampilkan_data_pertanian()
        id_pertanian_hapus = input("Masukkan ID pertanian yang ingin dihapus: ")
        db.hapus_data_pertanian(id_pertanian_hapus)

    elif choice == '5':
        print("Keluar dari program.")
        break

    else:
        print("Pilihan tidak valid. Silakan pilih lagi.")
