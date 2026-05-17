from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Q

from quickstart.serializers import BukuSerializer, SiswaSerializer, ProdiSerializer, KuliahSerializer, RegistrasiSerializer
from quickstart.models import Buku, Siswa, Prodi, Kuliah, Registrasi

from django_filters import rest_framework as filters

class MahasiswaFilter(filters.FilterSet):
    prodi = filters.CharFilter(
        field_name="prodi__nama_prodi", 
        lookup_expr='icontains',
        label='Prodi nama prodi contains'
    )
    matkul = filters.CharFilter(
        method='filter_by_matkul',
        label='Mata Kuliah contains'
    )

    class Meta:
        model = Siswa
        fields = ['prodi', 'matkul']

    def filter_by_matkul(self, queryset, name, value):
        return queryset.filter(
            registrasi__kuliah__matkul__icontains=value
        ).distinct()

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

class MahasiswaFilterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Siswa.objects.all()
    serializer_class = SiswaSerializer
    filterset_class = MahasiswaFilter

@api_view(['GET'])
def filter_siswa_by_prodi_matkul(request, prodi_name, matkul_name):
    """
    Filter siswa berdasarkan nama prodi dan mata kuliah
    Contoh: /api/DBT/Web akan menampilkan semua siswa jurusan DBT yang mengambil matkul Web
    """
    # Cari siswa yang terdaftar di mata kuliah tertentu dan berasal dari prodi tertentu
    registrasi = Registrasi.objects.filter(
        kuliah__matkul__icontains=matkul_name, 
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

@api_view(['GET'])
def filter_siswa_by_prodi(request, prodi_name):
    """
    Filter siswa berdasarkan nama prodi
    Contoh: /api/DBT/ akan menampilkan semua siswa jurusan DBT
    """
    # Cari siswa yang berasal dari prodi tertentu
    siswa_qs = Siswa.objects.filter(
        prodi__nama_prodi__icontains=prodi_name
    ).select_related('prodi')
    
    # Siapkan data siswa
    siswa_list = []
    
    for siswa in siswa_qs:
        siswa_data = {
            'id': siswa.id,
            'nama': siswa.nama,
            'nim': siswa.nim,
            'prodi': siswa.prodi.nama_prodi,
            'foto': siswa.foto.url if siswa.foto else None,
            'mata_kuliah': list(
                Registrasi.objects.filter(siswa=siswa).select_related('kuliah').values_list('kuliah__matkul', flat=True)
            )
        }
        siswa_list.append(siswa_data)
    
    return Response({
        'prodi': prodi_name,
        'jumlah_siswa': len(siswa_list),
        'siswa': siswa_list
    })

@api_view(['GET'])
def filter_siswa_by_matkul(request, matkul_name):
    """
    Filter siswa berdasarkan mata kuliah
    Contoh: /api/Web/ akan menampilkan semua siswa yang mengambil matkul Web
    """
    # Cari siswa yang terdaftar di mata kuliah tertentu
    registrasi = Registrasi.objects.filter(
        kuliah__matkul__icontains=matkul_name
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
        'mata_kuliah': matkul_name,
        'jumlah_siswa': len(siswa_list),
        'siswa': siswa_list
    })