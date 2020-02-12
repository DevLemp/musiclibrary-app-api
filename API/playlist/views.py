from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Track, Genre

from playlist import serializers


class BasePlaylistAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base viewset for user's owned objects"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TrackViewSet(BasePlaylistAttrViewSet):
    """Manage tracks in the database"""
    queryset = Track.objects.all()
    serializer_class = serializers.TrackSerializer

class GenreViewSet(BasePlaylistAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
