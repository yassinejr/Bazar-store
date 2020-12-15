from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import login, authenticate, logout
from .forms import UserForm, EditProfileForm, ProfileForm
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


@login_required(login_url='/accounts/login/')
def edit_profile(request, slug):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES,
                                   instance=request.user.profile)  # request.FILES is show the selected image or file

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('accounts/profile')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        args = {}
        # args.update(csrf(request))
        args['form'] = form
        args['profile_form'] = profile_form
        return render(request, 'registration/edit_profile.html', args)
