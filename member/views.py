from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponse, redirect, render

from .forms import UserForm


def signup(request) -> HttpResponse:
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/member/login/')
    else:
        form = UserForm()
    return render(request, 'member/signup.html', {'form': form})
