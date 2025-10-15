from django import forms
from .models import Buku, Transaksi

class BukuTabungan(forms.ModelForm):
    class Meta:
        model = Buku
        fields = '__all__'

class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['jenis_transaksi', 'jumlah', 'tanggal']