from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import login, authenticate
from .forms import UserForm
from .utils import cookieCart, cartData, guestOrder



def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')

    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'registration/signup.html', context)


@login_required(login_url='/accounts/login/')
def profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    data = cartData(request)

    cartitems = data['cartitems']
    context = {'profile': profile, 'cartitems': cartitems}
    return render(request, 'registration/profile.html', context)
