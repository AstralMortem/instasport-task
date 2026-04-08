from django.contrib import admin
from .models import Training



@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ("title", "scheduled_at", "created_by", "id")
    search_fields = ("title",)
    exclude = ("created_by",)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        return super().save_model(request, obj, form, change)
    