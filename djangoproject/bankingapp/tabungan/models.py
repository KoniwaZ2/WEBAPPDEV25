from django.db import models

class Buku(models.Model):
    kantor_bank = models.CharField(max_length=100)
    nomor_rekening = models.CharField(max_length=20, unique=True)
    nama_nasabah = models.CharField(max_length=100)
    alamat = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nama_nasabah}"
    
class Transaksi(models.Model):
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE, related_name='transaksi')
    jenis_transaksi = models.CharField(max_length=50, choices=[('debit', 'Debit'), ('credit', 'Credit')])
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)
    tanggal = models.DateField()
    saldo_akhir_debit = models.DecimalField(decimal_places=2, default=0, max_digits=12)
    saldo_akhir_credit = models.DecimalField(decimal_places=2, default=0, max_digits=12)

    def __str__(self):
        return f"{self.buku.nama_nasabah} - {self.jenis_transaksi} - {self.jumlah} - {self.tanggal}"