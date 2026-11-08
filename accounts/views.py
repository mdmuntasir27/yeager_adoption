from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileUpdateForm
from .models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Yeager Adoption, {user.username}!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    from adoptions.models import AdoptionRequest
    from pets.models import Favorite
    from community.models import AdoptionPost, AdoptionInquiry

    # Ensure profile exists
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    recent_requests = AdoptionRequest.objects.filter(user=request.user).select_related('pet')[:5]
    favorite_pets = Favorite.objects.filter(user=request.user).select_related('pet')
    my_posts = AdoptionPost.objects.filter(author=request.user)
    my_inquiries = AdoptionInquiry.objects.filter(requester=request.user).select_related('post')[:5]

    context = {
        'recent_requests': recent_requests,
        'favorite_pets': favorite_pets,
        'my_posts': my_posts,
        'my_inquiries': my_inquiries,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile, user=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})
