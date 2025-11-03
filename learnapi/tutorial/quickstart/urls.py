from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BukuViewSet, SiswaViewSet, ProdiViewSet, KuliahViewSet, RegistrasiViewSet, filter_siswa_by_prodi_matkul

router = DefaultRouter()
router.register(r"buku", BukuViewSet)
router.register(r"siswa", SiswaViewSet)
router.register(r"prodi", ProdiViewSet)
router.register(r"kuliah", KuliahViewSet)
router.register(r"registrasi", RegistrasiViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("<str:prodi_name>/<str:matkul_name>/", filter_siswa_by_prodi_matkul, name="filter-siswa"),
]