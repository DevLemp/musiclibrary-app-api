from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Track

from playlist import serializers


class TrackViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tracks in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Track.objects.all()
    serializer_class = serializers.TrackSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(artist=self.request.user).order_by('-title')
