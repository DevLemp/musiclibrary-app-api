from rest_framework import serializers

from core.models import Track


class TrackSerializer(serializers.ModelSerializer):
    """Serializer for track object"""

    class Meta:
        model = Track
        fields = ('id', 'title')
        read_only_fields = ('id',)
