#1301180018

# import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCServer
import pandas as pd

# import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading

# Batasi hanya pada path /RPC2 saja supaya tidak bisa mengakses path lainnya
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Buat server
#"127.0.0.1", 8008
with SimpleXMLRPCServer(("0.0.0.0", 5000),
        requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()

    #server.register_function(pow)
    # buat data struktur dictionary untuk menampung nama_kandidat dan hasil voting
    data_rakyat = pd.read_csv('data_rakyat.csv')
    data_laporan = []
    data_jemputan = []
    data = {}
    
    # kode setelah ini adalah critical section, menambahkan vote tidak boeh terjadi race condition
    # siapkan lock
    lock = threading.Lock()

    # def post(x) :
    #     print(x)
    #     lock.release()
    status = 0
    #  buat fungsi bernama vote_candidate()
    def cek_nik(nik, terduga, alamat, gejala):
        
        # critical section dimulai harus dilock
        lock.acquire()
        global status
        # jika kandidat ada dalam dictionary maka tambahkan  nilai votenya
        data = data_rakyat[data_rakyat['NIK'] == int(nik)]
        laporan = {}
        if len(data) > 0:
            # nik = data['NIK']
            # nama = data['Nama']
            laporan['nik'] = nik
            laporan['nama'] = data['Nama'][0]
            laporan['terduga'] = terduga
            laporan['alamat'] = alamat
            laporan['gejala'] = gejala
            status = 1
            data_laporan.append(laporan)
            # data_laporan.append([nik, nama, terduga, alamat, gejala])
        # critical section berakhir, harus diunlock
        lock.release()
        
    
    # register fungsi vote_candidate() sebagai vote
    server.register_function(cek_nik, 'ceknik')

    # buat fungsi bernama querry_result
    def querry_result():
        # critical section dimulai
        print('================================Data Laporan================================')
        print(data_laporan)
        lock.acquire()
        global status
        if(status != 0):
            status = 0
            lock.release()
            data_jemputan.append('Anda akan dijemput pada ..... oleh .....')
            print('================================Data JEMPUTAN================================')
            print(data_jemputan)
            return ('Anda akan dijemput pada ..... oleh .....')
        else:
            lock.release()
            return ('NIK tidak terdaftar')
        # hitung total vote yang ada
        # total_vote = sum(nama_kandidat.values())
        # hasil = []
        # # hitung hasil persentase masing-masing kandidat
        # for keys in nama_kandidat:
        #     hasil.append([keys, nama_kandidat[keys] / total_vote * 100])
        
        # # critical section berakhir
        # lock.release()
        # print(data_laporan)
        # return ('kamu dijemput sama kakak apink jam 2')
    # register querry_result sebagai querry
    server.register_function(querry_result, 'query')


    print ("Server covid berjalan...")
    # Jalankan server
    server.serve_forever()
