from .models import Berita, Komentar
from rest_framework import serializers

class KomentarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Komentar
        fields = '__all__'

class BeritaSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='berita-detail',
        lookup_field='pk'
    )
    
    class Meta:
        model = Berita
        fields = ['id', 'judul', 'tanggal', 'gambar', 'detail_url']