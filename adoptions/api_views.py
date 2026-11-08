from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import AdoptionRequest
from .serializers import AdoptionRequestSerializer
from pets.models import Pet


class AdoptionRequestViewSet(viewsets.ModelViewSet):
    serializer_class = AdoptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AdoptionRequest.objects.filter(user=self.request.user).select_related('pet', 'user')

    def perform_create(self, serializer):
        pet_id = self.request.data.get('pet')
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            raise ValidationError({'pet': 'Pet not found.'})

        if not pet.is_available:
            raise ValidationError({'pet': 'This pet has already been adopted.'})

        already_applied = AdoptionRequest.objects.filter(
            user=self.request.user, pet=pet, status__in=['Pending', 'Approved']
        ).exists()
        if already_applied:
            raise ValidationError({'pet': 'You already have an active adoption request for this pet.'})

        serializer.save(user=self.request.user, pet=pet)

