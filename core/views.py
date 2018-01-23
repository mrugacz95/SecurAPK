import os

from django.shortcuts import render, redirect

from core.forms import UploadFileForm
from core.models import App
from core.tasks import analize_apk


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            apk = form.save()
            apk_hash = os.path.dirname(apk.file.name)
            apk.file = apk_hash
            apk.save()
            analize_apk.delay(apk_hash)
            return redirect('results', apk_hash=apk_hash)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def results(request, apk_hash):
    app = App.objects.filter(file=apk_hash).order_by('-created_date').first()
    return render(request, 'results.html', {'app': app})


def results_list(request):
    apps = App.objects.filter(ready=True).all()
    return render(request, 'results_list.html', {'apps': apps})
