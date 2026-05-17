from django.urls import path, include
from .views import BeritaListView, KomentarListView, berita_list_html

def api_root(request):
    from django.http import JsonResponse
    return JsonResponse({
        'berita': request.build_absolute_uri('berita/'),
        'komentar': request.build_absolute_uri('komentar/'),
    })

urlpatterns = [
    # API endpoints
    path('', api_root, name='api-root'),
    path('berita/', BeritaListView.as_view(), name='berita-list-api'),
    path('komentar/', KomentarListView.as_view(), name='komentar-list-api'),
    path('api-auth/', include('rest_framework.urls')),
    
    # HTML views
    path('html/berita/', berita_list_html, name='berita-list-html')
]
