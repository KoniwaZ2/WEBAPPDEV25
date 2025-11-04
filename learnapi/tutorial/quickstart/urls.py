from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    BukuViewSet, SiswaViewSet, ProdiViewSet, KuliahViewSet, RegistrasiViewSet, 
    filter_siswa_by_prodi_matkul, filter_siswa_by_prodi, filter_siswa_by_matkul
)

router = DefaultRouter()
router.register(r"buku", BukuViewSet)
router.register(r"siswa", SiswaViewSet)
router.register(r"prodi", ProdiViewSet)
router.register(r"kuliah", KuliahViewSet)
router.register(r"registrasi", RegistrasiViewSet)

urlpatterns = [
    # path("", api_root, name="api-root"),
    path("", include(router.urls)),
    path("filter/prodi/<str:prodi_name>/matkul/<str:matkul_name>/", filter_siswa_by_prodi_matkul, name="filter-siswa-prodi-matkul"),
    path("filter/prodi/<str:prodi_name>/", filter_siswa_by_prodi, name="filter-siswa-prodi"),
    path("filter/matkul/<str:matkul_name>/", filter_siswa_by_matkul, name="filter-siswa-matkul"),
]