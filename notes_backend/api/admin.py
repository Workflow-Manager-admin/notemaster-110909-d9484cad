from django.contrib import admin
from .models import Note

# PUBLIC_INTERFACE
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Admin view for the Note model."""
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'user__username')
    list_filter = ('user', 'created_at', 'updated_at')
