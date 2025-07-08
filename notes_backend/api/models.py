from django.db import models
from django.contrib.auth import get_user_model

# PUBLIC_INTERFACE
class Note(models.Model):
    """Model representing a Note owned by a user."""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='notes',
        help_text='The user who created the note.',
    )
    title = models.CharField(max_length=255, help_text='Title of the note.')
    content = models.TextField(blank=True, help_text='Content of the note.')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Time when the note was created.')
    updated_at = models.DateTimeField(auto_now=True, help_text='Time when the note was last updated.')

    def __str__(self):
        return f"{self.title} (by {self.user})"
