from django.contrib import admin
from .models import Buku, Siswa, Prodi, Kuliah, Registrasi

@admin.register(Buku)
class BukuAdmin(admin.ModelAdmin):
    list_display = ('kantor_bank', 'nomor_rekening', 'nama_nasabah', 'alamat')
    search_fields = ('nomor_rekening', 'nama_nasabah')

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nim', 'prodi')
    search_fields = ('nama', 'nim')

@admin.register(Prodi)
class ProdiAdmin(admin.ModelAdmin):
    list_display = ('nama_prodi', 'kaprodi')
    search_fields = ('nama_prodi', 'kaprodi')

@admin.register(Kuliah)
class KuliahAdmin(admin.ModelAdmin):
    list_display = ('matkul', 'prodi', 'hari', 'sks')
    search_fields = ('matkul', 'hari')

@admin.register(Registrasi)
class RegistrasiAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'kuliah')
    search_fields = ('siswa__nama', 'kuliah__matkul')

