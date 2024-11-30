from django.shortcuts import render, redirect
from .forms import URLForm
from .models import URL
import uuid

def index(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            short_url = str(uuid.uuid4())[:6]
            url = URL(original_url=original_url, short_url=short_url)
            url.save()
            return redirect('short_url', short_url=short_url)
    else:
        form = URLForm()
    return render(request, 'index.html', {'form': form})

def short_url(request, short_url):
    try:
        url = URL.objects.get(short_url=short_url)
        return redirect(url.original_url)
    except URL.DoesNotExist:
        return render(request, '404.html')