
from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect,get_object_or_404 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import template
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template import TemplateDoesNotExist
from dashboard.models import *
from dashboard.forms import *
import matplotlib.pyplot as plt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.hazmat.primitives.asymmetric import dsa, padding
from cryptography.exceptions import InvalidSignature
from dashboard.utilsRSA import *
from dashboard.utilsDSA import *
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse, Http404
from datetime import datetime
from cryptography.hazmat.primitives import serialization
import base64
import logging
import json


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
        'jumlah_pemilih':jumlah_pemilih,
        'jumlah_pemilihan':jumlah_pemilihan,
        'jumlah_suara':jumlah_suara,
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
            pemilihan = Pemilihan.objects.get(token=token_input)
            return redirect('pemilihanvote', pemilihan_id=pemilihan.id)
        except Pemilihan.DoesNotExist:
            messages.error(request, "Token yang Anda masukkan salah.")
            return redirect('voting')  # Pastikan 'voting_page' adalah URL name untuk halaman input token
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

def load_dsa_private_key(request, pemilih_id):
    try:
        pemilih = Pemilih.objects.get(id=pemilih_id)
        private_key_dsa = pemilih.public_key  # Assuming this is how you store DSA private key in your model
        return JsonResponse({'private_key_dsa': private_key_dsa})
    except Pemilih.DoesNotExist:
        return HttpResponseNotFound('Pemilih not found') 

def get_private_key(request, pemilih_id):
    pemilih = Pemilih.objects.get(id=pemilih_id)
    return HttpResponse(pemilih.private_key, content_type='text/plain')

@csrf_exempt
def pemilihan_view(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    kandidats = Kandidat.objects.filter(pemilihan=pemilihan)

    # Retrieve pemilih_id from session
    pemilih_id = request.session.get('pemilih_id')
    print("Session pemilih_id in view:", pemilih_id)  # Debug line
    
    pemilih = None
    if pemilih_id:
        pemilih = get_object_or_404(Pemilih, id=pemilih_id)
        print("Pemilih fetched:", pemilih)  # Debug line

    context = {
        'pemilihan': pemilihan,
        'kandidats': kandidats,
        'pemilih': pemilih,
    }
    return render(request, 'front/pengambilanSuara.html', context)
    
@csrf_exempt
def vote(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, pk=pemilihan_id)
    kandidats = Kandidat.objects.filter(pemilihan=pemilihan)

    pemilih_id = request.session.get('pemilih_id')
    if not pemilih_id:
        logger.error('Pemilih ID tidak ditemukan dalam sesi')
        return JsonResponse({'status': 'error', 'message': 'Pemilih ID tidak ditemukan dalam sesi'}, status=400)

    pemilih = get_object_or_404(Pemilih, id=pemilih_id)

    # private_key_rsa = load_rsa_private_key(pemilih_id)
    # dekrip_nama_pemilih = decrypt_with_private_key(private_key_rsa.export_key(), pemilih.nama)
    # dekrip_nama_pemilihan = decrypt_with_private_key(private_key_rsa.export_key(), pemilihan.judul)

    voting = Voting.objects.filter(judul_pemilihan=pemilihan.judul, nama_pemilih=pemilih.nama).first()

    if voting:
        logger.error('Pemilih telah memberikan suara untuk pemilihan ini')
        return JsonResponse({'status': 'error', 'message': 'Anda sudah memberikan suara untuk pemilihan ini'}, status=400)

    if request.method == 'POST':
        kandidat_id = request.POST.get('kandidat_id')
        signature_b64 = request.headers.get('X-Vote-Signature')
        if not kandidat_id or not signature_b64:
            logger.error('Kandidat ID atau tanda tangan tidak ada')
            return JsonResponse({'status': 'error', 'message': 'Kandidat ID atau tanda tangan tidak ada'}, status=400)

        kandidat = get_object_or_404(Kandidat, id=kandidat_id, pemilihan=pemilihan)
        logger.debug(f"Memproses permintaan voting untuk pemilihan ID: {pemilihan_id}")

        # Tambahkan pernyataan logging untuk data penting
        logger.debug(f"kandidat_id: {request.POST.get('kandidat_id')}")
        logger.debug(f"X-Vote-Signature: {request.headers.get('X-Vote-Signature')}")

        try:
            # Verifikasi tanda tangan DSA
            public_key_dsa = load_dsa_public_key(pemilih.public_key)
            message = f"vote-{kandidat_id}-{pemilihan_id}"
            signature = base64.b64decode(signature_b64)
            public_key_dsa.verify(signature, message.encode('utf-8'), hashes.SHA1())

            # Menggunakan RSA untuk enkripsi nama kandidat
            public_key_rsa = load_rsa_public_key(pemilih_id)
            encrypted_nama_pemilih = pemilih.nama
            encrypted_nama_kandidat = encrypt_with_public_key(public_key_rsa.export_key(), kandidat.nama)
            encrypted_judul_pemilihan = pemilihan.judul
            waktu_voting = datetime.now()

            # Simpan suara
            voting = Voting(
                nama_pemilih=encrypted_nama_pemilih,
                nama_kandidat=encrypted_nama_kandidat,
                judul_pemilihan=encrypted_judul_pemilihan,
                waktu_voting=waktu_voting
            )
            voting.save()

            request.session['has_voted'] = True
            request.session['vote_signature'] = signature_b64

            response = JsonResponse({'status': 'success', 'message': 'Voting berhasil'})
            response['X-Vote-Signature'] = signature_b64
            logger.info('Tanda tangan DSA berhasil ditambahkan ke header')

            return response
        except InvalidSignature as e:
            logger.error(f'Error saat memverifikasi tanda tangan: {str(e)}')
            return JsonResponse({'status': 'error', 'message': 'Tanda tangan tidak valid'}, status=400)
        except Exception as e:
            logger.error(f'Error saat menyimpan vote: {str(e)}')
            return JsonResponse({'status': 'error', 'message': 'Error saving vote'}, status=500)
    else:
        logger.error('Invalid request method')
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
    for pemilihan in pemilihans:
        pemilihan.jumlah_kandidat = Kandidat.objects.filter(pemilihan=pemilihan).count()
        pemilihan.jumlah_pemilih = DaftarPemilihTerpilih.objects.filter(pemilihan=pemilihan).count()
    context = {
        'pemilihans': pemilihans,
    }
    return render(request, 'front/daftar_pemilihan.html', context)


def statistik(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    voting_results = Voting.objects.filter(judul_pemilihan=pemilihan.judul)
    
    # Calculate required information
    jumlah_pemilih = Pemilih.objects.count()
    pemilih_terpilih = voting_results.count()  # Number of voters who have voted
    jumlah_kandidat = Kandidat.objects.filter(pemilihan=pemilihan).count()
    
    # Decrypt candidate names and count votes
    vote_counts = {}
    pemilih_ids = Pemilih.objects.values_list('id', flat=True)  # Get all pemilih ids
    
    for vote in voting_results:
        decrypted = False
        for pemilih_id in pemilih_ids:
            private_key_rsa = load_rsa_private_key(pemilih_id)
            try:
                decrypted_nama_kandidat = decrypt_with_private_key(private_key_rsa, vote.nama_kandidat)
                decrypted_nama_kandidat = decrypted_nama_kandidat.strip()  # Ensure no leading/trailing spaces
                if decrypted_nama_kandidat in vote_counts:
                    vote_counts[decrypted_nama_kandidat] += 1
                else:
                    vote_counts[decrypted_nama_kandidat] = 1
                decrypted = True
                break
            except Exception as e:
                logger.error(f"Error decrypting vote for vote ID {vote.id}: {str(e)}")
                continue
        if not decrypted:
            logger.error(f"Error decrypting vote for vote ID {vote.id}: Unable to decrypt")
            # Handle error condition here, e.g., log, return error response, etc.

    labels = list(vote_counts.keys())
    data = list(vote_counts.values())
    total_suara = sum(data)  # Total votes

    # Convert to JSON strings
    labels_json = json.dumps(labels)
    data_json = json.dumps(data)

    return render(request, 'front/statistik.html', {
        'pemilihan': pemilihan,
        'jumlah_pemilih': jumlah_pemilih,
        'pemilih_terpilih': pemilih_terpilih,
        'jumlah_kandidat': jumlah_kandidat,
        'total_suara': total_suara,
        'labels': labels_json,  # Pass JSON string
        'data': data_json,  # Pass JSON string
    })
