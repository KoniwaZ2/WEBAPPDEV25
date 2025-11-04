from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Q

from quickstart.serializers import BukuSerializer, SiswaSerializer, ProdiSerializer, KuliahSerializer, RegistrasiSerializer
from quickstart.models import Buku, Siswa, Prodi, Kuliah, Registrasi


# @api_view(['GET'])
# def api_root(request, format=None):
#     """
#     Custom API Root yang menampilkan semua endpoint termasuk filter custom dengan data dari database
#     """
#     # Ambil data aktual dari database
#     prodi_list = Prodi.objects.all().values_list('nama_prodi', flat=True)[:5]  # Ambil 5 prodi pertama
#     matkul_list = Kuliah.objects.all().values_list('matkul', flat=True)[:5]    # Ambil 5 matkul pertama
    
#     # Generate contoh URL berdasarkan data aktual
#     prodi_matkul_examples = []
#     prodi_examples = []
#     matkul_examples = []
    
#     # Ambil kombinasi prodi-matkul yang benar-benar ada registrasinya
#     registrasi_sample = Registrasi.objects.select_related(
#         'siswa__prodi', 'kuliah'
#     ).distinct()[:3]
    
#     for reg in registrasi_sample:
#         prodi_matkul_examples.append(
#             request.build_absolute_uri(
#                 f'/api/filter/prodi/{reg.siswa.prodi.nama_prodi}/matkul/{reg.kuliah.matkul}/'
#             )
#         )
    
#     # Contoh filter by prodi
#     for prodi in prodi_list[:3]:
#         prodi_examples.append(
#             request.build_absolute_uri(f'/api/filter/prodi/{prodi}/')
#         )
    
#     # Contoh filter by matkul
#     for matkul in matkul_list[:3]:
#         matkul_examples.append(
#             request.build_absolute_uri(f'/api/filter/matkul/{matkul}/')
#         )
    
#     return Response({
#         'buku': reverse('buku-list', request=request, format=format),
#         'siswa': reverse('siswa-list', request=request, format=format),
#         'prodi': reverse('prodi-list', request=request, format=format),
#         'kuliah': reverse('kuliah-list', request=request, format=format),
#         'registrasi': reverse('registrasi-list', request=request, format=format),
#         'filter': {
#             'filter-by-prodi-and-matkul': {
#                 'description': 'Filter siswa berdasarkan prodi DAN mata kuliah',
#                 'format': '/api/filter/prodi/<prodi_name>/matkul/<matkul_name>/',
#                 'prodi_tersedia': list(prodi_list),
#                 'matkul_tersedia': list(matkul_list),
#                 'contoh_url': prodi_matkul_examples if prodi_matkul_examples else ['Belum ada data registrasi']
#             },
#             'filter-by-prodi': {
#                 'description': 'Filter siswa berdasarkan prodi saja',
#                 'format': '/api/filter/prodi/<prodi_name>/',
#                 'prodi_tersedia': list(prodi_list),
#                 'contoh_url': prodi_examples if prodi_examples else ['Belum ada data prodi']
#             },
#             'filter-by-matkul': {
#                 'description': 'Filter siswa berdasarkan mata kuliah saja',
#                 'format': '/api/filter/matkul/<matkul_name>/',
#                 'matkul_tersedia': list(matkul_list),
#                 'contoh_url': matkul_examples if matkul_examples else ['Belum ada data mata kuliah']
#             }
#         },
#         'statistik': {
#             'total_siswa': Siswa.objects.count(),
#             'total_prodi': Prodi.objects.count(),
#             'total_kuliah': Kuliah.objects.count(),
#             'total_registrasi': Registrasi.objects.count(),
#             'total_buku': Buku.objects.count(),
#         }
#     })


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