from django.urls import path,include
from .views import *
from django.conf.urls.static import static, settings


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('pemilih/',pemilih , name='pemilih'),

    path('pemilih/create/', createPemilih, name='createPemilih'),
    path('pemilih/edit/<int:pemilih_id>/', editPemilih, name='editPemilih'),
    path('pemilih/delete/<int:pemilih_id>/', deletePemilih, name='deletePemilih'),

    path('pemilihan/',pemilihan , name='pemilihan'),
    path('pemilihan/create/', createPemilihan, name='createPemilihan'),
    path('pemilihan/edit/<int:pemilihan_id>/', editPemilihan, name='editPemilihan'),
    path('pemilihan/delete/<int:pemilihan_id>/', deletePemilihan, name='deletePemilihan'),
    path('close-pemilihan/<int:pemilihan_id>/', closePemilihan, name='closePemilihan'),
    path('pemilihan/reopen/<int:pemilihan_id>/', reopenPemilihan, name='reopenPemilihan'),  

    # Rute untuk menambah pemilih
    path('tambah_pemilih/<int:pemilihan_id>/', tambah_pemilih, name='tambah_pemilih'),

    # Rute untuk daftar pemilih
    path('daftar_pemilih/<int:pemilihan_id>/', daftar_pemilih, name='daftar_pemilih'),

    # Jika Anda memerlukan rute untuk menghapus pemilih dari daftar pemilihan
    path('hapus_pemilih/<int:pemilihan_id>/<int:pemilih_id>/', hapus_pemilih, name='hapus_pemilih'),

    path('kandidat/',kandidat , name='kandidat'),
    path('kandidat/create/', createKandidat, name='createKandidat'),
    path('kandidat/edit/<int:kandidat_id>/', editKandidat, name='editKandidat'),
    path('kandidat/delete/<int:kandidat_id>/', deleteKandidat, name='deleteKandidat'),

    path('laporan_statistik/',laporan_statistik , name='laporan_statistik'),
    path('statistik/<int:pemilihan_id>/',hasil_voting , name='hasil_voting'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)