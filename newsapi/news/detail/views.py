from django.shortcuts import render
from rest_framework import generics
from berita.models import Berita, Komentar
from .serializers import BeritaDetailSerializer, KomentarDetailSerializer

class BeritaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Berita.objects.all()
    serializer_class = BeritaDetailSerializer

class KomentarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Komentar.objects.all()
    serializer_class = KomentarDetailSerializer

def berita_detail_html(request, pk):
    return render(request, 'detail/detail.html', {'berita_id': pk})