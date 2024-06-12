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

    path('kandidat/',kandidat , name='kandidat'),
    path('kandidat/create/', createKandidat, name='createKandidat'),
    path('kandidat/edit/<int:kandidat_id>/', editKandidat, name='editKandidat'),
    path('kandidat/delete/<int:kandidat_id>/', deleteKandidat, name='deleteKandidat'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)