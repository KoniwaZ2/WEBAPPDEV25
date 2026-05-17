from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, generics
from .models import Komentar, Berita
from .serializers import KomentarSerializer, BeritaSerializer

class BeritaListView(generics.ListCreateAPIView):
    queryset = Berita.objects.all()
    serializer_class = BeritaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['judul']

class KomentarListView(generics.ListCreateAPIView):
    queryset = Komentar.objects.all()
    serializer_class = KomentarSerializer
    filter_backends = [DjangoFilterBackend]

# HTML views untuk menampilkan data dari API
def berita_list_html(request):
    return render(request, 'berita/list.html')