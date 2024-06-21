from django.db import models
import uuid

class Pemilihan(models.Model):
    judul = models.CharField(max_length=200, verbose_name="Judul")
    waktu_mulai = models.DateTimeField(verbose_name="Waktu Mulai")
    waktu_selesai = models.DateTimeField(verbose_name="Waktu Selesai")
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pemilih = models.ManyToManyField('Pemilih', related_name='pemilihan', blank=True)
    is_election_closed = models.BooleanField(default=False, verbose_name="Pemilihan Ditutup")

    def __str__(self):
        return self.judul

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
    pemilih = models.ForeignKey(Pemilih, on_delete=models.CASCADE)
    kandidat = models.ForeignKey(Kandidat, on_delete=models.CASCADE,null=True, blank=True)
    pemilihan = models.ForeignKey(Pemilihan, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pemilih', 'pemilihan')

class DaftarPemilihTerpilih(models.Model):
    pemilihan = models.ForeignKey(Pemilihan, on_delete=models.CASCADE)
    pemilih = models.ForeignKey(Pemilih, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pemilihan} - {self.pemilih}"