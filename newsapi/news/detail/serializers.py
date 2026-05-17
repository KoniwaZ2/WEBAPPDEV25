from rest_framework import serializers
from berita.models import Berita, Komentar

class KomentarDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Komentar
        fields = '__all__'

class BeritaDetailSerializer(serializers.ModelSerializer):
    komentar = KomentarDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Berita
        fields = '__all__'
