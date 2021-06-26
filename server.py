#1301180018

# import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCServer
from datetime import datetime, timedelta
import pandas as pd

# import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading

# Batasi hanya pada path /RPC2 saja supaya tidak bisa mengakses path lainnya
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Buat server
#"0.0.0.0", 8008
with SimpleXMLRPCServer(("0.0.0.0", 8008),
        requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()

    #server.register_function(pow)
    # buat data struktur dictionary untuk menampung nama_kandidat dan hasil voting
    data_rakyat = pd.read_csv('data_rakyat.csv')
    data_penjemput = pd.read_csv('anggota_jemput.csv')
    data_laporan = []
    data_jemputan = []
    data = {}
    print(data_rakyat['NIK'])
    lock = threading.Lock()
    
    #status untuk berhasil add laporan atau tidak
    status = 0
    tim = 1
    #  buat fungsi bernama vote_candidate()
    def add_laporan(nik, terduga, alamat, gejala):
        
        # critical section dimulai harus dilock
        lock.acquire()
        global status
        # jika kandidat ada dalam dictionary maka tambahkan  nilai votenya
        data = data_rakyat[data_rakyat['NIK'] == int(nik)]
        laporan = {}
        if len(data) > 0:
            laporan['nik'] = nik
            laporan['nama'] = data['Nama'][0]
            laporan['terduga'] = terduga
            laporan['alamat'] = alamat
            laporan['gejala'] = gejala
            status = 1
            data_laporan.append(laporan)
            
        # critical section berakhir, harus diunlock
        lock.release()
        
    
    # register fungsi vote_candidate() sebagai vote
    server.register_function(add_laporan, 'laporan')

    # buat fungsi bernama querry_result
    def querry_result():
        # critical section dimulai
        print('================================Data Laporan================================')
        print(data_laporan)
        lock.acquire()
        global status
        global tim
        if(status != 0):
            status = 0

            jam_jemput = datetime.now() + timedelta(hours = 1)
            jam_jemput = jam_jemput.strftime("%H:%M:%S")
            id = len(data_jemputan)
            tim_penjemput = tim
            penjemput = data_penjemput[data_penjemput['id_tim']==tim_penjemput]
            data_jemputan.append([id, jam_jemput, tim_penjemput])
            
            tim += 1
            if (tim > len(data_penjemput)):
                tim = 1

            lock.release()      
            print('================================Data JEMPUTAN================================')
            print(data_jemputan)
            return([id, jam_jemput, tim_penjemput, penjemput['Anggota1'].values[0], penjemput['Anggota2'].values[0], penjemput['Anggota3'].values[0]])
            # return ('Nomor jemputan : ',id,', pukul ',jam_jemput,' oleh ',data_jemputan[id][2])
        else:
            lock.release()
            return ('NIK tidak terdaftar')
    server.register_function(querry_result, 'query')

    def query_cek(id):
        lock.acquire()
        if (id < 0 or id >= len(data_jemputan)):
            lock.release()
            return('Data id tidak ada')
        
        tim_penjemput = data_jemputan[id][2]
        penjemput = data_penjemput[data_penjemput['id_tim']==tim_penjemput]
        lock.release()
        # return ('Nomor jemputan : ',data_jemputan[id][0],', pukul ',data_jemputan[id][1],' oleh ',data_jemputan[id][2])
        return([data_jemputan[id][0], data_jemputan[id][1], tim_penjemput, penjemput['Anggota1'].values[0], penjemput['Anggota2'].values[0], penjemput['Anggota3'].values[0]])
    server.register_function(query_cek, 'cek_jemput')

    print ("Server covid berjalan...")
    # Jalankan server
    server.serve_forever()
