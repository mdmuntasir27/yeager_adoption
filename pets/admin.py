from django.contrib import admin
from .models import Pet, Favorite


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type', 'breed', 'age', 'gender', 'location', 'status', 'created_at')
    list_filter = ('animal_type', 'gender', 'status', 'location')
    search_fields = ('name', 'breed', 'location')
    list_editable = ('status',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'animal_type', 'breed', 'age', 'gender', 'location')
        }),
        ('Details', {
            'fields': ('description', 'image', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'pet__name')
