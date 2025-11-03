from rest_framework import serializers

from quickstart.models import Buku, Siswa, Prodi, Kuliah, Registrasi


class BukuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buku
        fields = '__all__'

class SiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Siswa
        fields = '__all__'

class ProdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prodi
        fields = '__all__'

class KuliahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kuliah
        fields = '__all__'

class RegistrasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registrasi
        fields = '__all__'