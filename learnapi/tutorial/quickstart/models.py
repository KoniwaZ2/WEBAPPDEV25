from django.db import models
from django.utils import timezone

class Buku(models.Model):
    kantor_bank = models.CharField(max_length=100)
    nomor_rekening = models.CharField(max_length=20, unique=True)
    nama_nasabah = models.CharField(max_length=100)
    alamat = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nama_nasabah}"
    
class Prodi(models.Model):
    nama_prodi = models.CharField(max_length=100)
    kaprodi = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.nama_prodi}"
    
class Siswa(models.Model):
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=20, unique=True)
    foto = models.ImageField(upload_to='fotosiswa/')
    prodi = models.ForeignKey(Prodi, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nama}"

class Kuliah(models.Model):
    matkul = models.CharField(max_length=100)
    prodi = models.ForeignKey(Prodi, on_delete=models.CASCADE)
    hari = models.CharField(max_length=10, unique=True)
    sks = models.IntegerField()

    def __str__(self):
        return f"{self.matkul}"
    
class Registrasi(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    kuliah = models.ForeignKey(Kuliah, on_delete=models.CASCADE)
    tanggal_registrasi = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.siswa.nama} - {self.kuliah.matkul}"