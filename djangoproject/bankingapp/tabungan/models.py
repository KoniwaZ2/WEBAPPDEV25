from django.db import models

class Buku(models.Model):
    kantor_bank = models.CharField(max_length=100)
    nomor_rekening = models.CharField(max_length=20, unique=True)
    nama_nasabah = models.CharField(max_length=100)
    alamat = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nama_nasabah}"