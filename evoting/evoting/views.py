
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
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from dashboard.utilsRSA import *
from io import BytesIO
from datetime import datetime
import base64
import logging



# Konfigurasi logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def home(request):

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
        pemilihan = get_object_or_404(Pemilihan, token=token_input)
        if pemilihan:
            # Redirect to the voting page with the valid pemilihan id
            return redirect('pemilihanvote', pemilihan_id=pemilihan.id)
        else:
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

def vote(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, pk=pemilihan_id)
    kandidats = Kandidat.objects.filter(pemilihan=pemilihan)

    pemilih_id = request.session.get('pemilih_id')
    if not pemilih_id:
        logger.error('Pemilih ID tidak ditemukan dalam sesi')
        return JsonResponse({'status': 'error', 'message': 'Pemilih ID tidak ditemukan dalam sesi'}, status=400)

    pemilih = get_object_or_404(Pemilih, id=pemilih_id)
    
    voting = Voting.objects.filter(judul_pemilihan=pemilihan.judul, nama_pemilih=pemilih.nama).first()
    
    if voting:
        logger.error('Pemilih telah memberikan suara untuk pemilihan ini')
        return JsonResponse({'status': 'error', 'message': 'Anda sudah memberikan suara untuk pemilihan ini'}, status=400)

    if request.method == 'POST':
        form = VotingForm(request.POST)
        if form.is_valid():
            kandidat_id = form.cleaned_data['kandidat_id']
            kandidat = get_object_or_404(Kandidat, id=kandidat_id, pemilihan=pemilihan)
            
            public_key = load_public_key(pemilih)
            encrypted_nama_pemilih =  pemilih.nama
            encrypted_nama_kandidat = encrypt_with_public_key(public_key, kandidat.nama)
            encrypted_judul_pemilihan = pemilihan.judul
            waktu_voting = datetime.now()

            voting = Voting(
                nama_pemilih=encrypted_nama_pemilih,
                nama_kandidat=encrypted_nama_kandidat,
                judul_pemilihan=encrypted_judul_pemilihan,
                waktu_voting=waktu_voting
            )
            try:
                voting.save()
                
                request.session['has_voted'] = True
                
                private_key = pemilih.get_private_key()
                message = f"{pemilih.nama}-{kandidat.nama}-{pemilihan.judul}-{str(waktu_voting)}"
                signature = private_key.sign(
                    message.encode('utf-8'), hashes.SHA1()
                )
                signature_b64 = base64.b64encode(signature).decode('utf-8')

                # Simpan signature ke sesi
                request.session['vote_signature'] = signature_b64

                response = JsonResponse({'status': 'success', 'message': 'Voting berhasil'})
                response['X-Vote-Signature'] = signature_b64
                logger.info('Tanda tangan DSA berhasil ditambahkan ke header')

                return response
            except Exception as e:
                logger.error(f'Error saat menyimpan vote: {str(e)}')
                return JsonResponse({'status': 'error', 'message': 'Error saving vote'}, status=500)
        else:
            logger.error('Form is not valid')
            return JsonResponse({'status': 'error', 'message': 'Form is not valid'}, status=400)

    logger.error('Invalid request method')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def hasil_pemilihan(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    votings = Voting.objects.filter(judul_pemilihan=pemilihan.judul)

    pemilih_id = request.session.get('pemilih_id')
    if not pemilih_id:
        logger.error('Pemilih ID tidak ditemukan dalam sesi')
        return render(request, 'front/error.html', {'message': 'Pemilih ID tidak ditemukan dalam sesi'}, status=400)

    pemilih = get_object_or_404(Pemilih, id=pemilih_id)
    private_key = load_private_key(pemilih)

    decrypted_votes = []
    valid_vote_count = 0

    for vote in votings:
        try:
            print(request.META)
            signature_b64 = request.META.get('X-Vote-Signature')
            if not signature_b64:
                logger.error('Signature tidak ditemukan dalam header')
                continue

            signature = base64.b64decode(signature_b64)
            message = f"{vote.nama_pemilih}-{vote.nama_kandidat}-{vote.judul_pemilihan}-{vote.waktu_voting}"

            public_key = pemilih.get_public_key()
            public_key.verify(
                signature,
                message.encode('utf-8'),
                hashes.SHA256()
            )

            decrypted_nama_pemilih = vote.nama_pemilih
            decrypted_nama_kandidat = decrypt_with_private_key(private_key, vote.nama_kandidat)
            decrypted_judul_pemilihan = vote.judul_pemilihan

            decrypted_votes.append({
                'nama_pemilih': decrypted_nama_pemilih,
                'nama_kandidat': decrypted_nama_kandidat,
                'judul_pemilihan': decrypted_judul_pemilihan,
                'waktu_voting': vote.waktu_voting,
            })

            valid_vote_count += 1

        except Exception as e:
            logger.error(f"Error decrypting vote {vote.id}: {e}")
            continue

    form = VotingForm()
    template_name = 'front/hasil_pemilihan.html'
    context = {
        'pemilihan': pemilihan,
        'decrypted_votes': decrypted_votes,
        'form': form,
        'valid_vote_count': valid_vote_count,
    }
    return render(request, template_name, context)

def api_hasil_pemilihan(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    votings = Voting.objects.filter(judul_pemilihan=pemilihan.judul)
    
    pemilih_id = request.session.get('pemilih_id')
    if not pemilih_id:
        return JsonResponse({'status': 'error', 'message': 'Pemilih ID tidak ditemukan dalam sesi'}, status=400)
    
    pemilih = get_object_or_404(Pemilih, id=pemilih_id)
    private_key = load_private_key(pemilih)
    
    decrypted_votes = []
    valid_vote_count = 0

    for vote in votings:
        try:
            decrypted_nama_pemilih = vote.nama_pemilih
            decrypted_nama_kandidat = decrypt_with_private_key(private_key, vote.nama_kandidat)
            decrypted_judul_pemilihan = vote.judul_pemilihan

            decrypted_votes.append({
                'nama_pemilih': decrypted_nama_pemilih,
                'nama_kandidat': decrypted_nama_kandidat,
                'judul_pemilihan': decrypted_judul_pemilihan,
                'waktu_voting': vote.waktu_voting,
            })

            valid_vote_count += 1

        except Exception as e:
            continue

    response_data = {
        'status': 'success',
        'valid_vote_count': valid_vote_count,
        'decrypted_votes': decrypted_votes
    }

    return JsonResponse(response_data)
    
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


