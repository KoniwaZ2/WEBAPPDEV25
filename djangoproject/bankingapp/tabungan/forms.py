from django import forms
from .models import Buku

class BukuTabungan(forms.ModelForm):
    class Meta:
        model = Buku
        fields = '__all__'