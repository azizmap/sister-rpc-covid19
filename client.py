#1301180018

# import xmlrpc bagian client saja
import xmlrpc.client

# buat stub (proxy) untuk client
s = xmlrpc.client.ServerProxy('http://54.151.246.141:5000')

# lakukan pemanggilan fungsi vote("nama_kandidat") yang ada di server
print("Masukkan NIK :")
nik = input()
print("Masukkan nama terduga covid :")
terduga = input()
print("Masukkan alamat :")
alamat = input()
print("Gejalan yang dirasakan terduga:")
keluhan = input()
s.ceknik(nik, terduga, alamat, keluhan)

print()
print()
print()
# lakukan pemanggilan fungsi querry() untuk mengetahui hasil persentase dari masing-masing kandidat
hasil = s.query()
print('=======================PERHATIAN !!!!!=======================')
print(hasil)
# lakukan pemanggilan fungsi lain terserah Anda