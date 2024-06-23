from django.db import models
import secrets
from .utilsRSA import *


class Pemilihan(models.Model):
    judul = models.CharField(max_length=200, verbose_name="Judul")
    waktu_mulai = models.DateTimeField(verbose_name="Waktu Mulai")
    waktu_selesai = models.DateTimeField(verbose_name="Waktu Selesai")
    token = models.CharField(max_length=32, editable=False, unique=True)
    pemilih = models.ManyToManyField('Pemilih', related_name='pemilihan', blank=True)
    is_election_closed = models.BooleanField(default=False, verbose_name="Pemilihan Ditutup")

    def __str__(self):
        return self.judul

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(6)  # Menghasilkan string heksadesimal random dengan panjang 32 karakter
        super().save(*args, **kwargs)

class Pemilih(models.Model):
    nama = models.TextField( blank=True, null=True)
    nim = models.TextField( blank=True, null=True)
    prodi = models.TextField(blank=True, null=True)
    org_hima = models.TextField(blank=True, null=True)
    org_ukm = models.TextField(blank=True, null=True)
    public_key = models.TextField(blank=True, null=True)  # Bidang untuk menyimpan kunci publik
    private_key = models.TextField(blank=True, null=True)  # Bidang untuk menyimpan kunci privat

    def _str_(self):
        return self.nama

class Kandidat(models.Model):
    pemilihan = models.ForeignKey(Pemilihan, on_delete=models.CASCADE, related_name="kandidats" ,default=1)
    no_urut = models.IntegerField(blank=True, null=True)
    nama = models.CharField(max_length=100)
    visi_misi = models.TextField()
    foto = models.ImageField(upload_to='foto/', blank=True, null=True)

    def __str__(self):
        return self.nama

class Voting(models.Model):
    nama_pemilih = models.CharField(max_length=200, blank=True, null=True)
    nama_kandidat = models.CharField(max_length=100, blank=True, null=True)
    nama_kandidat_dekripsi = models.CharField(max_length=100, blank=True, null=True)  # Field untuk hasil dekripsi
    judul_pemilihan = models.CharField(max_length=200, blank=True, null=True)
    waktu_voting = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama_pemilih} - {self.nama_kandidat} ({self.judul_pemilihan})"

class DaftarPemilihTerpilih(models.Model):
    pemilihan = models.ForeignKey(Pemilihan, on_delete=models.CASCADE)
    pemilih = models.ForeignKey(Pemilih, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pemilihan} - {self.pemilih}"