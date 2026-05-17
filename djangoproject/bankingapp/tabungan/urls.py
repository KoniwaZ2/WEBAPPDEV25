# from django.urls import include, path
# from . import views
# from rest_framework.routers import DefaultRouter
# from .views import BukuViewSet

# router = DefaultRouter()
# router.register(r"buku", BukuViewSet)

# # app_name = 'tabungan'
# urlpatterns = [
#     path('', include(router.urls)),
#     # path('', views.list_buku, name='list-buku'),
#     # path('buku/create', views.create_buku, name='create-buku'),
#     # path('buku/update/<int:buku_id>/', views.update_buku, name='update-buku'),
#     # path('buku/delete/<int:buku_id>/', views.delete_buku, name='delete-buku'),
#     # path('buku/transaksi/<int:buku_id>/', views.transaksi, name='transaksi'),
# ]

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BukuViewSet, TransaksiViewSet

router = DefaultRouter()
router.register(r"buku", BukuViewSet)
router.register(r"transaksi", TransaksiViewSet)

urlpatterns = [
    path("", include(router.urls)),
]