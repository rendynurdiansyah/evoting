from django.db import models
import secrets
from .utilsRSA import *
from .utilsDSA import *
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.hazmat.primitives import serialization
import base64, os

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
    nim = models.TextField( blank=True, null=True,unique=True)
    prodi = models.TextField(blank=True, null=True)
    org_hima = models.TextField(blank=True, null=True)
    org_ukm = models.TextField(blank=True, null=True)
    public_key = models.TextField(blank=True, null=True)  # Bidang untuk menyimpan kunci publik
    private_key = models.TextField(blank=True, null=True)  # Bidang untuk menyimpan kunci privat

    def _str_(self):
        return self.nama
    
    def generate_keys_dsa(self):
        generate_dsa_keys(self.id)

    def get_private_key(self):
        return load_dsa_private_key(self.id)

    def get_public_key(self):
        return load_dsa_public_key(self.id)

class Kandidat(models.Model):
    pemilihan = models.ForeignKey(Pemilihan, on_delete=models.CASCADE, related_name="kandidats" ,default=1)
    no_urut = models.IntegerField(blank=True, null=True)
    nama = models.CharField(max_length=100)
    visi_misi = models.TextField()
    foto = models.ImageField(upload_to='foto/', blank=True, null=True)

    def __str__(self):
        return self.nama

class Voting(models.Model):
    nama_pemilih = models.TextField( blank=True, null=True)
    nama_kandidat = models.TextField( blank=True, null=True) # Field untuk hasil dekripsi
    judul_pemilihan = models.TextField( blank=True, null=True)
    waktu_voting = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama_pemilih} - {self.nama_kandidat} ({self.judul_pemilihan})"
    
    def sign_vote(self):
        message = f'{self.pemilih.id}{self.kandidat.id}{self.pemilihan.id}{self.timestamp}'.encode('utf-8')
        private_key = self.pemilih.get_private_key()
        signature = private_key.sign(
            message,
            hashes.SHA1()
        )
        self.signature = base64.b64encode(signature).decode('utf-8')
        self.save()

    def verify_signature(self):
        message = f'{self.pemilih.id}{self.kandidat.id}{self.pemilihan.id}{self.timestamp}'.encode('utf-8')
        public_key = self.pemilih.get_public_key()
        signature = base64.b64decode(self.signature.encode('utf-8'))

        try:
            public_key.verify(
                signature,
                message,
                hashes.SHA1()
            )
            return True
        except Exception as e:
            return False


class DaftarPemilihTerpilih(models.Model):
    pemilihan = models.ForeignKey(Pemilihan, on_delete=models.CASCADE)
    pemilih = models.ForeignKey(Pemilih, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pemilihan} - {self.pemilih}"