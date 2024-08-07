
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path ,include,re_path

from . views import *
from django.contrib.auth import logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404,handler500

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('voting/', voting, name='voting'),
    path('daftar/pemilihan/', daftar_pemilihan, name='daftar_pemilihan'),
    # path('statistik/<int:pemilihan_id>/', statistik, name='statistik'),

    path("", include('dashboard.urls')),  
    path("", include('accounts.urls')),  

    path('validate-token/', validate_token, name='validate_token'),
    path('pemilihanvote/<int:pemilihan_id>/', pemilihanvote, name='pemilihanvote'),
    path('pengambilanSuara/<int:pemilihan_id>/', pengambilanSuara, name='pengambilanSuara'),
    path('vote/<int:pemilihan_id>/', vote, name='vote'),
    path('voting/success/', voting_success, name='voting_success'),
    path('voting_already_used/', voting_already_used, name='voting_already_used'),
    path('sorry/', sorry, name='sorry'),
    path('pemilihan/<int:pemilihan_id>/', pemilihan_view, name='pemilihan_view'),
    path('pemilihan/statistik/<int:pemilihan_id>/', statistik, name='statistik'),
    path('get-private-key/<int:pemilih_id>/', get_private_key, name='get_private_key'),

    path('load_dsa_private_key/<int:pemilih_id>/', load_dsa_private_key, name='load_dsa_private_key'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

