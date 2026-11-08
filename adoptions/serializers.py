from rest_framework import serializers
from .models import AdoptionRequest


class AdoptionRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    pet_name = serializers.CharField(source='pet.name', read_only=True)

    class Meta:
        model = AdoptionRequest
        fields = [
            'id', 'user', 'username', 'pet', 'pet_name',
            'phone', 'address', 'reason', 'previous_pet_experience',
            'message', 'status', 'created_at'
        ]
        read_only_fields = ['user', 'status', 'created_at']

