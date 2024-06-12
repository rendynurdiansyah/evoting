
from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect,get_object_or_404

from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template import TemplateDoesNotExist
from dashboard.models import *
from dashboard.forms import *


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
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    return render(request, 'front/pemilihanvote.html', {'pemilihan': pemilihan})

def pengambilanSuara(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, id=pemilihan_id)
    kandidats = Kandidat.objects.filter(pemilihan=pemilihan)
    return render(request, 'front/pengambilanSuara.html', {'pemilihan': pemilihan,'kandidats': kandidats})

def vote(request, pemilihan_id):
    pemilihan = get_object_or_404(Pemilihan, pk=pemilihan_id)
    kandidats = Kandidat.objects.filter(pemilihan=pemilihan)
    
    if request.method == 'POST':
        form = VotingForm(request.POST)
        if form.is_valid():
            kandidat_id = form.cleaned_data['kandidat_id']
            kandidat = get_object_or_404(Kandidat, pk=kandidat_id)
            pemilih_id = request.session.get('pemilih_id')
            pemilih = get_object_or_404(Pemilih, id=pemilih_id)
            
            # Check if the user has already voted for this election
            if Voting.objects.filter(pemilihan=pemilihan, pemilih=pemilih).exists():
                return render(request, 'front/voting_error.html', {'message': 'You have already voted for this election.'})
            
            # Save the vote
            vote = Voting.objects.create(pemilihan=pemilihan, pemilih=pemilih, kandidat=kandidat)
            vote.save()
            return redirect('voting_success')
    else:
        form = VotingForm()

    return render(request, 'front/pengambilanSuara.html', {'pemilihan': pemilihan, 'kandidats': kandidats, 'form': form})

def statistik(request):
    template_name = 'front/statistik.html'
    context = {
        'title':'statistik',
        'welcome':'welcome statistik',
    }
    return render(request, template_name, context)

