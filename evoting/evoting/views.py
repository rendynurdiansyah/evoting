
from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect,get_object_or_404 

from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template import TemplateDoesNotExist
from dashboard.models import *
from dashboard.forms import *

import logging

# Konfigurasi logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def login_view(request):
    if request.method == 'POST':
        nim = request.POST.get('nim')
        pemilih = get_object_or_404(Pemilih, nim=nim)
        request.session['pemilih_id'] = pemilih.id
        return redirect('voting')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')

def home(request):
        # Cek login
    if not request.session.get('pemilih_id'):
        return redirect('login_view')

    jumlah_pemilih = Pemilih.objects.count()
    jumlah_pemilihan = Pemilihan.objects.count()
    jumlah_suara = Voting.objects.count()
    template_name = 'front/index.html'
    context = {
        'title':'my home',
        'welcome':'welcome my home',
    }
    return render(request, template_name, context)

def voting(request):
        # Cek login
    if not request.session.get('pemilih_id'):
        return redirect('login')
    return render(request, 'front/voting.html')

def validate_token(request):
    if request.method == "POST":
        token_input = request.POST.get('token')
        try:
            # Convert input token to UUID
            token_uuid = uuid.UUID(token_input)
            pemilihan = get_object_or_404(Pemilihan, token=token_uuid)
            # Redirect to the voting page with the valid pemilihan id
            return redirect('pemilihanvote', pemilihan_id=pemilihan.id)
        except (ValueError, Pemilihan.DoesNotExist):
            # Token is invalid or does not exist
            return HttpResponse("Invalid token", status=400)
    return HttpResponse(status=405)

def pemilihanvote(request, pemilihan_id):
        # Cek login
    if not request.session.get('pemilih_id'):
        return redirect('login')
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    return render(request, 'front/pemilihanvote.html', {'pemilihan': pemilihan})

def pengambilanSuara(request, pemilihan_id):
        # Cek login
    if not request.session.get('pemilih_id'):
        return redirect('login')
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    kandidats = Kandidat.objects.filter(pemilihan=pemilihan)
    return render(request, 'front/pengambilanSuara.html', {'pemilihan': pemilihan,'kandidats': kandidats})

def vote(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, pk=pemilihan_id)
    kandidats = Kandidat.objects.filter(pemilihan=pemilihan)
    
    pemilih_id = request.session.get('pemilih_id')
    if not pemilih_id:
        logger.debug('Pemilih ID tidak ditemukan dalam sesi')
        return redirect('login')

    pemilih = get_object_or_404(Pemilih, id=pemilih_id)
    
    # Periksa apakah pemilih sudah memberikan suara untuk pemilihan ini
    if Voting.objects.filter(pemilih=pemilih, pemilihan=pemilihan).exists():
        return redirect('voting_already_used')

    if request.method == 'POST':
        kandidat_id = request.POST.get('kandidat_id')
        if not kandidat_id:
            logger.debug('Kandidat ID tidak ditemukan dalam POST data')
            return redirect('pengambilanSuara', pemilihan_id=pemilihan_id)
        
        kandidat = get_object_or_404(Kandidat, id=kandidat_id)
        
        voting = Voting(pemilih=pemilih, kandidat=kandidat, pemilihan=pemilihan)
        try:
            voting.save()
            return redirect('voting_success')
        except Exception as e:
            logger.error(f"Error saving vote: {e}")
            return HttpResponse("Error saving vote", status=500)
    
    template_name = 'front/pengambilanSuara.html'
    context = {
        'title': 'Voting',
        'pemilihan': pemilihan,
        'kandidats': kandidats,
    }
    return render(request, template_name, context)

def voting_success(request):
        # Cek login
    if not request.session.get('pemilih_id'):
        return redirect('login')
    return render(request, 'front/voting_success.html', {'message': 'Thank you for voting!'})

def voting_already_used(request):
    return render(request, 'front/voting_gagal.html', {'message': 'Maaf, suara Anda sudah digunakan.'})

def daftar_pemilihan(request):
    pemilihans = Pemilihan.objects.all()
    context = {
        'pemilihans': pemilihans,
    }
    return render(request, 'front/daftar_pemilihan.html', context)
    
def statistik(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, pk=pemilihan_id)
    kandidats = Kandidat.objects.filter(pemilihan=pemilihan)
    
    labels = []
    data = []

    for kandidat in kandidats:
        labels.append(kandidat.nama)
        jumlah_suara = Voting.objects.filter(pemilihan=pemilihan, kandidat=kandidat).count()
        data.append(jumlah_suara)

    context = {
        'pemilihan': pemilihan,
        'labels': labels,
        'data': data,
    }
    return render(request, 'front/statistik.html', context)

