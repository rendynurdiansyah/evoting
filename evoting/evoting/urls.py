
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path ,include,re_path

from . views import *

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404,handler500

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('voting/', voting, name='voting'),
    path('statistik/', statistik, name='statistik'),

    path("", include('dashboard.urls')),  

    path('validate-token/', validate_token, name='validate_token'),
    path('pemilihanvote/<int:pemilihan_id>/', pemilihanvote, name='pemilihanvote'),
    path('pengambilanSuara/<int:pemilihan_id>/', pengambilanSuara, name='pengambilanSuara'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
