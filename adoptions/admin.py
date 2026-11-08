from django.contrib import admin
from .models import AdoptionRequest


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'pet__name', 'phone')
    list_editable = ('status',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Application Info', {
            'fields': ('user', 'pet', 'status')
        }),
        ('Contact', {
            'fields': ('phone', 'address')
        }),
        ('Reason', {
            'fields': ('reason', 'previous_pet_experience', 'message')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if change:
            original = AdoptionRequest.objects.get(pk=obj.pk)
            if original.status != 'Approved' and obj.status == 'Approved':
                obj.pet.status = 'Adopted'
                obj.pet.save()
        super().save_model(request, obj, form, change)
