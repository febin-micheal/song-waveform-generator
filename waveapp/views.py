import librosa
import librosa.display
import matplotlib.pyplot as plt
from os.path import basename
import pandas as pd
from django.db import connection
from django.shortcuts import render, redirect
from .models import *
from .forms import SongForm
import io
from django.core.files.images import ImageFile

# Create your views here.

def home(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('output')
    else:
        form = SongForm()
    return render(request, 'waveapp/home.html', {
        'form': form
    })

def output(request):

    song_dir = Song.objects.values_list('song', flat=True).last()
    song_file = 'media/' + song_dir
    samples, sample_rate = librosa.load(song_file)

    plt.figure(figsize = (13, 5))
    librosa.display.waveshow(y = samples, sr = sample_rate)
    plt.title(basename(song_file))

    file_name = basename(song_dir).replace('.mp3', '.png')
    file_name = basename(song_dir).replace('.flac', '.png')
    figure = io.BytesIO()
    plt.savefig(figure, format='png')
    content_file = ImageFile(figure)

    obj = Song.objects.last()
    obj.waveform.save(file_name, content_file)

    df = pd.DataFrame(samples)

    file = 'waveapp/output.csv'
    with open(file, 'w') as csvfile:
        df.to_csv(csvfile)

    with open(file, 'r') as f:
        with connection.cursor() as cursor:
            next(f)
            cursor.execute('TRUNCATE waveapp_wave')
            cursor.copy_from(f, 'waveapp_wave', sep=',')

    wave_dir = Song.objects.values_list('waveform', flat=True).last()
    wave_file = 'http://localhost:8000/media/' + wave_dir

    return render(request, 'waveapp/output.html', {
        'wave_file': wave_file
    })
