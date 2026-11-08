from django.db import models
from django.contrib.auth.models import User
from pets.models import Pet


class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_requests')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    phone = models.CharField(max_length=20)
    address = models.TextField()
    reason = models.TextField(help_text='Why do you want this pet?')
    previous_pet_experience = models.BooleanField(default=False)
    message = models.TextField(blank=True, help_text='Additional message (optional)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} -> {self.pet.name} ({self.status})'
