
from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect,get_object_or_404 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template import TemplateDoesNotExist
from dashboard.models import *
from dashboard.forms import *
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import logging

# Konfigurasi logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def home(request):
        # Cek login
    if not request.session.get('pemilih_id'):
        return redirect('pemilih_login')

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
        return redirect('pemilih_login')
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
    # Cek login pemilih
    pemilih_id = request.session.get('pemilih_id')
    if not pemilih_id:
        return redirect('pemilih_login')
    
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    
    # Periksa apakah pemilih terpilih dalam pemilihan tertentu berdasarkan DaftarPemilihTerpilih
    pemilih_terpilih = DaftarPemilihTerpilih.objects.filter(pemilihan=pemilihan, pemilih__id=pemilih_id).exists()
    if not pemilih_terpilih:
        return redirect('sorry')  # Ganti dengan halaman yang sesuai
    
    return render(request, 'front/pemilihanvote.html', {'pemilihan': pemilihan})
    
def sorry(request):
        # Cek login
    if not request.session.get('pemilih_id'):
        return redirect('login')
    return render(request, 'front/voting_success.html', {'message': 'Maaf anda tidak termasuk dalam daftar!'})
def pengambilanSuara(request, pemilihan_id):
        # Cek login
    if not request.session.get('pemilih_id'):
        return redirect('pemilih_login')
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    kandidats = Kandidat.objects.filter(pemilihan=pemilihan)
    return render(request, 'front/pengambilanSuara.html', {'pemilihan': pemilihan,'kandidats': kandidats})

@csrf_exempt
def vote(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, pk=pemilihan_id)
    kandidats = Kandidat.objects.filter(pemilihan=pemilihan)

    pemilih_id = request.session.get('pemilih_id')
    if not pemilih_id:
        logger.debug('Pemilih ID tidak ditemukan dalam sesi')
        return JsonResponse({'status': 'error', 'message': 'Pemilih ID tidak ditemukan dalam sesi'}, status=400)

    pemilih = get_object_or_404(Pemilih, id=pemilih_id)

    # Periksa apakah pemilih sudah memberikan suara untuk pemilihan ini
    if Voting.objects.filter(pemilih=pemilih, pemilihan=pemilihan).exists():
        return JsonResponse({'status': 'error', 'message': 'Anda sudah memberikan suara untuk pemilihan ini'}, status=400)

    if request.method == 'POST':
        kandidat_id = request.POST.get('kandidat_id')
        if not kandidat_id:
            logger.debug('Kandidat ID tidak ditemukan dalam POST data')
            return JsonResponse({'status': 'error', 'message': 'Kandidat ID tidak ditemukan dalam POST data'}, status=400)

        kandidat = get_object_or_404(Kandidat, id=kandidat_id)

        voting = Voting(pemilih=pemilih, kandidat=kandidat, pemilihan=pemilihan)
        try:
            voting.save()
            return JsonResponse({'status': 'success', 'message': 'Voting berhasil'})
        except Exception as e:
            logger.error(f"Error saving vote: {e}")
            return JsonResponse({'status': 'error', 'message': 'Error saving vote'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

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
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    voting_results = Voting.objects.filter(pemilihan=pemilihan)
    
    # Hitung informasi yang diperlukan
    jumlah_pemilih = Pemilih.objects.count()
    pemilih_terpilih = voting_results.count()  # Jumlah pemilih yang telah memilih
    jumlah_kandidat = pemilihan.kandidats.count()
    
    # Hitung total suara untuk setiap kandidat
    kandidats = pemilihan.kandidats.all()
    labels = [kandidat.nama for kandidat in kandidats]
    data = [voting_results.filter(kandidat=kandidat).count() for kandidat in kandidats]
    total_suara = sum(data)  # Total semua suara
    
    return render(request, 'front/statistik.html', {
        'pemilihan': pemilihan,
        'jumlah_pemilih': jumlah_pemilih,
        'pemilih_terpilih': pemilih_terpilih,
        'jumlah_kandidat': jumlah_kandidat,
        'total_suara': total_suara,
        'labels': labels,
        'data': data,
    })