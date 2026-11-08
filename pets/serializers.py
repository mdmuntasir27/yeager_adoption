from rest_framework import serializers
from .models import Pet, Favorite


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ['created_at']


class FavoriteSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source='pet.name', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'pet', 'pet_name', 'created_at']
        read_only_fields = ['created_at']

