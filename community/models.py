from django.db import models
from django.contrib.auth.models import User


class AdoptionPost(models.Model):
    ANIMAL_TYPE_CHOICES = [
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Bird', 'Bird'),
        ('Rabbit', 'Rabbit'),
        ('Other', 'Other'),
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unknown', 'Unknown'),
    ]
    STATUS_CHOICES = [
        ('Open', 'Open for Adoption'),
        ('Given', 'Given for Adoption'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_posts')
    pet_name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=50, choices=ANIMAL_TYPE_CHOICES)
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(help_text='Age in years', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Unknown')
    location = models.CharField(max_length=150)
    description = models.TextField(help_text='Describe the pet and why you are giving it for adoption')
    image = models.ImageField(upload_to='community_posts/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.pet_name} by {self.author.username}'

    @property
    def is_open(self):
        return self.status == 'Open'

    @property
    def request_count(self):
        return self.adoption_inquiries.count()


class AdoptionInquiry(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Contacted', 'Contacted'),
        ('Rejected', 'Rejected'),
    ]

    post = models.ForeignKey(AdoptionPost, on_delete=models.CASCADE, related_name='adoption_inquiries')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_inquiries')
    message = models.TextField(help_text='Why do you want to adopt this pet?')
    contact_phone = models.CharField(max_length=20)
    contact_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('post', 'requester')

    def __str__(self):
        return f'{self.requester.username} interested in {self.post.pet_name}'
