from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AdoptionRequest
from .forms import AdoptionRequestForm
from pets.models import Pet


@login_required
def apply_adoption(request, pet_pk):
    pet = get_object_or_404(Pet, pk=pet_pk)

    if not pet.is_available:
        messages.error(request, 'This pet has already been adopted and is no longer available.')
        return redirect('pet_detail', pk=pet_pk)

    already_applied = AdoptionRequest.objects.filter(
        user=request.user, pet=pet, status__in=['Pending', 'Approved']
    ).exists()

    if already_applied:
        messages.warning(request, 'You already have an active adoption request for this pet.')
        return redirect('pet_detail', pk=pet_pk)

    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption = form.save(commit=False)
            adoption.user = request.user
            adoption.pet = pet
            adoption.save()
            messages.success(request, f'Your adoption application for {pet.name} has been submitted successfully!')
            return redirect('my_requests')
    else:
        form = AdoptionRequestForm()

    return render(request, 'adoptions/apply.html', {'form': form, 'pet': pet})


@login_required
def my_requests(request):
    requests_qs = AdoptionRequest.objects.filter(user=request.user).select_related('pet')
    return render(request, 'adoptions/my_requests.html', {'requests': requests_qs})
