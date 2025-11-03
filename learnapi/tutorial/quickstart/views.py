from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Q

from quickstart.serializers import BukuSerializer, SiswaSerializer, ProdiSerializer, KuliahSerializer, RegistrasiSerializer
from quickstart.models import Buku, Siswa, Prodi, Kuliah, Registrasi


class BukuViewSet(viewsets.ModelViewSet):
    queryset = Buku.objects.all()
    serializer_class = BukuSerializer

class SiswaViewSet(viewsets.ModelViewSet):
    queryset = Siswa.objects.all()
    serializer_class = SiswaSerializer

class ProdiViewSet(viewsets.ModelViewSet):
    queryset = Prodi.objects.all()
    serializer_class = ProdiSerializer

class KuliahViewSet(viewsets.ModelViewSet):
    queryset = Kuliah.objects.all()
    serializer_class = KuliahSerializer

class RegistrasiViewSet(viewsets.ModelViewSet):
    queryset = Registrasi.objects.all()
    serializer_class = RegistrasiSerializer

@api_view(['GET'])
def filter_siswa_by_prodi_matkul(request, prodi_name, matkul_name):
    """
    Filter siswa berdasarkan nama prodi dan mata kuliah
    Contoh: /api/DBT/Web akan menampilkan semua siswa jurusan DBT yang mengambil matkul Web
    """
    # Cari siswa yang terdaftar di mata kuliah tertentu dan berasal dari prodi tertentu
    registrasi = Registrasi.objects.filter(
        kuliah__matkul__icontains=matkul_name,  # icontains untuk case-insensitive search
        siswa__prodi__nama_prodi__icontains=prodi_name
    ).select_related('siswa', 'kuliah', 'siswa__prodi')
    
    # Ambil data siswa yang unik
    siswa_list = []
    siswa_ids = set()
    
    for reg in registrasi:
        if reg.siswa.id not in siswa_ids:
            siswa_ids.add(reg.siswa.id)
            siswa_data = {
                'id': reg.siswa.id,
                'nama': reg.siswa.nama,
                'nim': reg.siswa.nim,
                'prodi': reg.siswa.prodi.nama_prodi,
                'foto': reg.siswa.foto.url if reg.siswa.foto else None,
                'mata_kuliah': []
            }
            siswa_list.append(siswa_data)
    
    # Tambahkan info mata kuliah untuk setiap siswa
    for siswa_data in siswa_list:
        matkul_list = registrasi.filter(siswa__id=siswa_data['id']).values_list('kuliah__matkul', flat=True)
        siswa_data['mata_kuliah'] = list(matkul_list)
    
    return Response({
        'prodi': prodi_name,
        'mata_kuliah': matkul_name,
        'jumlah_siswa': len(siswa_list),
        'siswa': siswa_list
    })