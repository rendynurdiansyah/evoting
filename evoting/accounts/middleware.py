# accounts/middleware.py
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import User
from accounts.models import Pemilih

class AdminSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.admin_user = SimpleLazyObject(lambda: self.get_admin_user(request))
        response = self.get_response(request)
        return response

    def get_admin_user(self, request):
        user = None
        if request.user.is_authenticated and request.user.is_staff:
            user = request.user
        return user

class PemilihSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.pemilih_user = SimpleLazyObject(lambda: self.get_pemilih_user(request))
        response = self.get_response(request)
        return response

    def get_pemilih_user(self, request):
        pemilih = None
        if 'pemilih_id' in request.session:
            pemilih_id = request.session['pemilih_id']
            pemilih = Pemilih.objects.filter(id=pemilih_id).first()
        return pemilih
