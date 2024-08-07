from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.utils import timezone
from django.http import JsonResponse
from .utilsRSA import *
from .utilsDSA import *
import json

# Create your views here.
@login_required
def dashboard(request):
    jumlah_pemilih = Pemilih.objects.count()
    jumlah_pemilihan = Pemilihan.objects.count()
    jumlah_suara = Voting.objects.count()
    jumlah_kandidat = Kandidat.objects.count()
    template_name = 'back/home/index.html'
    context = {
        'title':'my home',
        'welcome':'welcome my home',
        'jumlah_pemilih':jumlah_pemilih,
        'jumlah_pemilihan':jumlah_pemilihan,
        'jumlah_suara':jumlah_suara,
        'jumlah_kandidat':jumlah_kandidat,
    }
    return render(request, template_name, context)

def pemilih(request):
    pemilihs = Pemilih.objects.all()
    form = PemilihForm()
    template_name = 'back/home/pemilih.html'
    context = {
        'title' : 'user',
        'pemilihs': pemilihs,
        'form': form,
    }
    return render(request, template_name, context)

def createPemilih(request):
    if request.method == 'POST':
        form = PemilihForm(request.POST)
        if form.is_valid():
            # Generate DSA keys
            private_key, public_key = generate_dsa_keys()
            
            # Save the form but do not commit to the database yet
            pemilih = form.save(commit=False)
            pemilih.private_key = private_key
            pemilih.public_key = public_key
            
            # Now save the pemilih object to the database
            pemilih.save()

            # Optionally, generate RSA key as mentioned in your previous code
            generate_rsa_keys(pemilih.id)

            return redirect('pemilih')  # Replace 'pemilih' with the appropriate URL name
    else:
        form = PemilihForm()
    
    return render(request, 'back/home/pemilih.html', {'form': form})

def editPemilih(request, pemilih_id):
    pemilih = get_object_or_404(Pemilih, pk=pemilih_id)
    if request.method == 'POST':
        print("Data POST diterima:", request.POST)
        form = PemilihForm(request.POST, instance=pemilih)
        if form.is_valid():
            form.save()
            return redirect('pemilih')  # Redirect ke halaman daftar pemilih setelah berhasil menyimpan
        else:
            print("Form tidak valid:", form.errors)
            return render(request, 'back/home/pemilih.html', {'edit_form': form, 'edit_errors': form.errors, 'edit_pemilih_id': pemilih_id})
    else:
        form = PemilihForm(instance=pemilih)
    return render(request, 'back/home/pemilih.html', {'edit_form': form, 'edit_pemilih_id': pemilih_id})

def deletePemilih(request, pemilih_id):
    pemilih = get_object_or_404(Pemilih, pk=pemilih_id)
    if request.method == 'POST':
        pemilih.delete()
        return redirect('pemilih')
    return render(request, 'back/home/pemilih.html', {'pemilih': pemilih})

def daftar_pemilih(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    
    # Retrieve distinct Pemilih objects associated with the given Pemilihan
    pemilih_terpilih = Pemilih.objects.filter(pemilihan__id=pemilihan_id).distinct()

    # Simpan data pemilih_terpilih ke DaftarPemilihTerpilih if it doesn't exist already
    for pemilih in pemilih_terpilih:
        if not DaftarPemilihTerpilih.objects.filter(pemilihan=pemilihan, pemilih=pemilih).exists():
            DaftarPemilihTerpilih.objects.create(pemilihan=pemilihan, pemilih=pemilih)

    return render(request, 'back/home/daftar_pemilih.html', {
        'pemilihan': pemilihan,
        'pemilih_terpilih': pemilih_terpilih
    })

def tambah_pemilih(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    semua_pemilih = Pemilih.objects.all()

    if request.method == 'POST':
        pemilih_ids = request.POST.getlist('pemilih_ids[]')
        for pemilih_id in pemilih_ids:
            pemilih = get_object_or_404(Pemilih, id=pemilih_id)
            # Tambahkan pemilih ke DaftarPemilihTerpilih jika belum ada
            if not DaftarPemilihTerpilih.objects.filter(pemilihan=pemilihan, pemilih=pemilih).exists():
                DaftarPemilihTerpilih.objects.create(pemilihan=pemilihan, pemilih=pemilih)
        return redirect('daftar_pemilih', pemilihan_id=pemilihan_id)

    return render(request, 'back/home/tambah_pemilih.html', {
        'pemilihan': pemilihan,
        'semua_pemilih': semua_pemilih,
    })

def hapus_pemilih(request, pemilihan_id, pemilih_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    pemilih = get_object_or_404(Pemilih, id=pemilih_id)
    
    if request.method == 'POST':
        # Hapus pemilih dari DaftarPemilihTerpilih
        DaftarPemilihTerpilih.objects.filter(pemilihan=pemilihan, pemilih=pemilih).delete()
        return redirect('daftar_pemilih', pemilihan_id=pemilihan_id)
    
    return redirect('daftar_pemilih', pemilihan_id=pemilihan_id)


def pemilihan(request):
    pemilihans = Pemilihan.objects.all()
    form = PemilihanForm()

    # Check if any election should be closed
    for pemilihan in pemilihans:
        if not pemilihan.is_election_closed:  # Only check if the election is not already closed
            if pemilihan.waktu_selesai < timezone.now():
                pemilihan.is_election_closed = True
                pemilihan.save()

            # Check if all voters have voted
            if pemilihan.pemilih.count() > 0:
                total_voters = pemilihan.pemilih.count()
                total_votes = pemilihan.pemilih.exclude(suara=None).count()
                if total_votes == total_voters:
                    pemilihan.is_election_closed = True
                    pemilihan.save()

    context = {
        'title': 'user',
        'pemilihans': pemilihans,
        'form': form,
    }
    return render(request, 'back/home/pemilihan.html', context)
def createPemilihan(request):
    if request.method == 'POST':
        form = PemilihanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pemilihan')
    else:
        form = PemilihanForm()
    
    return render(request, 'back/home/pemilihan.html', {'form': form})

def editPemilihan(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    if request.method == 'POST':
        form = PemilihanForm(request.POST, instance=pemilihan)
        if form.is_valid():
            form.save()
            return redirect('pemilihan')
    else:
        form = PemilihanForm(instance=pemilihan)
    return render(request, 'back/home/pemilihan.html', {'form': form, 'pemilihan': pemilihan})

def deletePemilihan(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    if request.method == 'POST':
        pemilihan.delete()
        return redirect('pemilihan')
    return render(request, 'back/home/pemilihan.html', {'pemilihan': pemilihan})

def closePemilihan(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    
    # Set is_closed to True to close the election
    pemilihan.is_election_closed = True
    pemilihan.save()

    return redirect('pemilihan')  # Ganti dengan URL yang sesuai

def reopenPemilihan(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    
    # Set is_closed to False to reopen the election
    pemilihan.is_election_closed = False
    pemilihan.save()

    return redirect('pemilihan')


def kandidat(request):
    kandidats = Kandidat.objects.all()
    pilihan_kandidat = Pemilihan.objects.all()
    form = KandidatForm()
    template_name = 'back/home/kandidat.html'
    context = {
        'title': 'Daftar Kandidat',
        'kandidats': kandidats,
        'pilihan_kandidat': pilihan_kandidat,
        'form': form,
    }
    return render(request, template_name, context)

def createKandidat(request):
    if request.method == 'POST':
        form = KandidatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('kandidat')
    else:
        form = KandidatForm()
    return render(request, 'back/home/kandidat.html', {'form': form})

def editKandidat(request, kandidat_id):
    kandidat = get_object_or_404(Kandidat, id=kandidat_id)
    pilihan_kandidat = Pemilihan.objects.all()  # Ambil semua pilihan kandidat
    if request.method == 'POST':
        form = KandidatForm(request.POST, request.FILES, instance=kandidat)
        if form.is_valid():
            form.save()
            return redirect('kandidat')
    else:
        form = KandidatForm(instance=kandidat)
    
    return render(request, 'back/home/kandidat.html', {'form': form, 'kandidat': kandidat, 'pilihan_kandidat': pilihan_kandidat})

def deleteKandidat(request, kandidat_id):
    kandidat = get_object_or_404(Kandidat, id=kandidat_id)
    if request.method == 'POST':
        kandidat.delete()
        return redirect('kandidat')
    return render(request, 'back/home/kandidat.html', {'kandidat': kandidat})

def laporan_statistik(request):
    pemilihans = Pemilihan.objects.all()
    template_name = 'back/home/statistik.html'
    context = {
        'title':'my home',
        'welcome':'welcome my home',
        'pemilihans':pemilihans,
    }
    return render(request, template_name, context)

def hasil_voting(request, pemilihan_id):
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