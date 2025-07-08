from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from .models import Note
from rest_framework import serializers

# Serializer for Note model
class NoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'user', 'created_at', 'updated_at']
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

# Custom permission to allow only owners to edit/delete their notes
class IsOwner(permissions.BasePermission):
    """
    Allows access only to owners of the Note.
    """
    # PUBLIC_INTERFACE
    def has_object_permission(self, request, view, obj):
        """Grant permission only to the owner of the note."""
        return obj.user == request.user

# PUBLIC_INTERFACE
class NoteListCreateView(generics.ListCreateAPIView):
    """
    get:
    List all notes for the current authenticated user.

    post:
    Create a new note for the current authenticated user.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# PUBLIC_INTERFACE
class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Retrieve a note for the current authenticated user.

    put:
    Update a note for the current authenticated user.

    patch:
    Partially update a note for the current authenticated user.

    delete:
    Delete a note for the current authenticated user.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Note.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

@api_view(['GET'])
def health(request):
    return Response({"message": "Server is up!"})
