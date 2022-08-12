from distutils.command.upload import upload
from django.db import models

# Create your models here.
class Song(models.Model):
    song = models.FileField(upload_to='songs')
    waveform = models.ImageField(upload_to='waveforms', null=True)

    def __str__(self):
        return str(self.song).replace('songs/', '')

class Wave(models.Model):
    amplitude = models.FloatField()
