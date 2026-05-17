from django.urls import path
from .views import BeritaDetailView, KomentarDetailView, berita_detail_html

urlpatterns = [
    path('berita/<int:pk>/', BeritaDetailView.as_view(), name='berita-detail'),
    path('html/berita/<int:pk>/', berita_detail_html, name='berita-detail-html'),
    path('komentar/<int:pk>/', KomentarDetailView.as_view(), name='komentar-detail'),
]
