from django import forms
from .models import *

class PemilihanForm(forms.ModelForm):
    class Meta:
        model = Pemilihan
        fields = ['judul', 'waktu_mulai', 'waktu_selesai']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan judul acara'}),
            'waktu_mulai': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'waktu_selesai': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        labels = {
            'judul': 'Judul Acara',
            'waktu_mulai': 'Waktu Mulai',
            'waktu_selesai': 'Waktu Selesai',
        }

class PemilihForm(forms.ModelForm):
    class Meta:
        model = Pemilih
        fields = ['nama', 'nim', 'prodi', 'org_hima', 'org_ukm']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Nama'}),
            'nim': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Masukkan nim'}),
            'prodi': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Masukkan prodi'}),
            'org_hima': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Masukkan Organinasi Himpunan'}),
            'org_ukm': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Masukkan Organisasi UKM'}),
        }

class KandidatForm(forms.ModelForm):
    class Meta:
        model = Kandidat
        fields = ['nama', 'visi_misi', 'foto', 'pemilihan']
        
        widgets = {
            'pemilihan': forms.Select(attrs={'class': 'form-control'}),
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'visi_misi': forms.Textarea(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class TokenForm(forms.Form):
    token = forms.UUIDField(label="Token")