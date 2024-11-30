from django.shortcuts import render, redirect, get_object_or_404
from .forms import SnippetForm
from .models import Snippet
import uuid
from django.contrib.auth.decorators import login_required

def create_snippet(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.shareable_url = str(uuid.uuid4())[:6]
            snippet.save()
            return redirect('view_snippet', shareable_url=snippet.shareable_url)
    else:
        form = SnippetForm()
    return render(request, 'create_snippet.html', {'form': form})

def view_snippet(request, shareable_url):
    snippet = get_object_or_404(Snippet, shareable_url=shareable_url)
    print(snippet.secret_key)
    if snippet.secret_key:
        return render(request, 'enter_secret_key.html', {'shareable_url': shareable_url})
    return render(request, 'view_snippet.html', {'snippet': snippet})

def enter_secret_key(request, shareable_url):
    snippet = get_object_or_404(Snippet, shareable_url=shareable_url)
    if request.method == 'POST':
        secret_key = request.POST['secret_key']
        if secret_key == snippet.secret_key:
            return render(request, 'view_snippet.html', {'snippet': snippet})
        return render(request, 'invalid_secret_key.html')
    return render(request, 'enter_secret_key.html', {'shareable_url': shareable_url})
