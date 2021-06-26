#1301180018

# import xmlrpc bagian client saja
import xmlrpc.client
import os

# buat stub (proxy) untuk client
# s = xmlrpc.client.ServerProxy('http://127.0.0.1:8008')
s = xmlrpc.client.ServerProxy('http://54.151.246.141:8008')

# lakukan pemanggilan fungsi vote("nama_kandidat") yang ada di server
# status = True
while True:
  print("Silahkan pilih menu :")
  print("1. Lapor Covid-19")
  print("2. Cek Pengantaran")
  print("3. Keluar")
  print("Silahkan pilih menu (1 atau 2) :")
  pil = int(input())
  print()

  if(pil == 1):
    print("Masukkan NIK :")
    nik = input()
    print("Masukkan nama terduga covid :")
    terduga = input()
    print("Masukkan alamat :")
    alamat = input()
    print("Gejala yang dirasakan terduga:")
    keluhan = input()
    s.laporan(nik, terduga, alamat, keluhan)

    os.system('cls')
    hasil = s.query()
    print('=======================PERHATIAN !!!!!=======================')
    if isinstance(hasil, list):
      print('Id Jemputan : ', hasil[0])
      print('Dijemput pukul : ', hasil[1])
      print('Tim Penjemput : ', hasil[2])
      print('Anggota 1 : ', hasil[3])
      print('Anggota 2 : ', hasil[4])
      print('Anggota 3 : ', hasil[5])
      print('')
    else:
      print(hasil)
      print('')
  elif(pil == 2):
    print("masukkan id jemputan")
    id = int(input())
    hasil = s.cek_jemput(id)

    os.system('cls')
    print('=======================PERHATIAN !!!!!=======================')
    if isinstance(hasil, list):
      print('Id Jemputan : ', hasil[0])
      print('Dijemput pukul : ', hasil[1])
      print('Tim Penjemput : ', hasil[2])
      print('Anggota 1 : ', hasil[3])
      print('Anggota 2 : ', hasil[4])
      print('Anggota 3 : ', hasil[5])
      print('')
    else:
      print(hasil)
    print('')
    # panggil fungsi cek jemputan
  elif(pil == 3):
    os.system('cls')
    break
  else:
    os.system('cls')

# lakukan pemanggilan fungsi querry() untuk mengetahui hasil persentase dari masing-masing kandidat
# lakukan pemanggilan fungsi lain terserah Anda