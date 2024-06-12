from django.db import models
import uuid

class Pemilihan(models.Model):
    judul = models.CharField(max_length=200, verbose_name="Judul")
    waktu_mulai = models.DateTimeField(verbose_name="Waktu Mulai")
    waktu_selesai = models.DateTimeField(verbose_name="Waktu Selesai")
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.judul

class Pemilih(models.Model):
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=20)
    prodi = models.CharField(max_length=100)
    org_hima = models.CharField(max_length=100)
    org_ukm = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

class Kandidat(models.Model):
    pemilihan = models.ForeignKey(Pemilihan, on_delete=models.CASCADE, related_name="kandidats" ,default=1)
    nama = models.CharField(max_length=100)
    visi_misi = models.TextField()
    foto = models.ImageField(upload_to='foto/', blank=True, null=True)

    def __str__(self):
        return self.nama

class Voting(models.Model):
    pemilih = models.ForeignKey(Pemilih, on_delete=models.CASCADE)
    kandidat = models.ForeignKey(Kandidat, on_delete=models.CASCADE)
    pemilihan = models.ForeignKey(Pemilihan, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pemilih', 'pemilihan')