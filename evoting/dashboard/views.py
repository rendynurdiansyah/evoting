from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.utils import timezone


# Create your views here.
@login_required
def dashboard(request):
    template_name = 'back/home/index.html'
    context = {
        'title':'my home',
        'welcome':'welcome my home',
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
            form.save()
            return redirect('pemilih')
    else:
        form = PemilihForm()
    return render(request, 'back/home/pemilih.html', {'form': form})

def editPemilih(request, pemilih_id):
    pemilih = get_object_or_404(Pemilih, pk=pemilih_id)
    if request.method == 'POST':
        form = PemilihForm(request.POST, instance=pemilih)
        if form.is_valid():
            form.save()
            return redirect('pemilih')
    else:
        form = PemilihForm(instance=pemilih)
    return render(request, 'back/home/pemilih.html', {'form': form})

def deletePemilih(request, pemilih_id):
    pemilih = get_object_or_404(Pemilih, pk=pemilih_id)
    if request.method == 'POST':
        pemilih.delete()
        return redirect('pemilih')
    return render(request, 'back/home/pemilih.html', {'pemilih': pemilih})

def daftar_pemilih(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    pemilih_terpilih = Pemilih.objects.filter(voting__pemilihan=pemilihan).distinct()

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
            Voting.objects.get_or_create(pemilih=pemilih, pemilihan=pemilihan)
        return redirect('daftar_pemilih', pemilihan_id=pemilihan_id)

    return render(request, 'back/home/tambah_pemilih.html', {
        'pemilihan': pemilihan,
        'semua_pemilih': semua_pemilih,
    })

def hapus_pemilih(request, pemilihan_id, pemilih_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    pemilih = get_object_or_404(Pemilih, id=pemilih_id)
    
    if request.method == 'POST':
        voting = Voting.objects.filter(pemilih=pemilih, pemilihan=pemilihan)
        voting.delete()
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

def createPemilih(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        nim = request.POST.get('nim')
        prodi = request.POST.get('prodi')
        org_hima = request.POST.get('org_hima')
        org_ukm = request.POST.get('org_ukm')
        data = nama  # Data yang akan ditandatangani
        signature = sign_data(data)
        
        Pemilih.objects.create(nama=nama, signature=signature, nim=nim, prodi=prodi, org_hima=org_hima, org_ukm=org_ukm)
        return redirect('pemilih_list')
    return render(request, 'dashboard/create_pemilih.html')
