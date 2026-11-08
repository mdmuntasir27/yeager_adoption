from django.contrib import admin
from .models import AdoptionPost, AdoptionInquiry


@admin.register(AdoptionPost)
class AdoptionPostAdmin(admin.ModelAdmin):
    list_display = ('pet_name', 'animal_type', 'author', 'location', 'status', 'created_at')
    list_filter = ('animal_type', 'gender', 'status')
    search_fields = ('pet_name', 'breed', 'location', 'author__username')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AdoptionInquiry)
class AdoptionInquiryAdmin(admin.ModelAdmin):
    list_display = ('requester', 'post', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('requester__username', 'post__pet_name')
    list_editable = ('status',)
    readonly_fields = ('created_at',)
