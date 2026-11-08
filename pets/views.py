from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Pet, Favorite


def pet_list(request):
    pets = Pet.objects.all()

    query = request.GET.get('q', '')
    animal_type = request.GET.get('animal_type', '')
    breed = request.GET.get('breed', '')
    gender = request.GET.get('gender', '')
    location = request.GET.get('location', '')
    status = request.GET.get('status', '')

    if query:
        pets = pets.filter(
            Q(name__icontains=query) |
            Q(breed__icontains=query) |
            Q(animal_type__icontains=query)
        )
    if animal_type:
        pets = pets.filter(animal_type=animal_type)
    if breed:
        pets = pets.filter(breed__icontains=breed)
    if gender:
        pets = pets.filter(gender=gender)
    if location:
        pets = pets.filter(location__icontains=location)
    if status:
        pets = pets.filter(status=status)

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(pets, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    favorite_pet_ids = []
    if request.user.is_authenticated:
        favorite_pet_ids = list(
            Favorite.objects.filter(user=request.user).values_list('pet_id', flat=True)
        )

    context = {
        'page_obj': page_obj,
        'query': query,
        'animal_type': animal_type,
        'breed': breed,
        'gender': gender,
        'location': location,
        'status': status,
        'animal_type_choices': Pet.ANIMAL_TYPE_CHOICES,
        'gender_choices': Pet.GENDER_CHOICES,
        'status_choices': Pet.STATUS_CHOICES,
        'favorite_pet_ids': favorite_pet_ids,
    }
    return render(request, 'pets/pet_list.html', context)


def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    is_favorite = False
    already_applied = False

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, pet=pet).exists()
        from adoptions.models import AdoptionRequest
        already_applied = AdoptionRequest.objects.filter(
            user=request.user, pet=pet, status__in=['Pending', 'Approved']
        ).exists()

    context = {
        'pet': pet,
        'is_favorite': is_favorite,
        'already_applied': already_applied,
    }
    return render(request, 'pets/pet_detail.html', context)


@login_required
@require_POST
def toggle_favorite(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, pet=pet)
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})
