from rest_framework import serializers

from core.models import Track, Genre


class TrackSerializer(serializers.ModelSerializer):
    """Serializer for track object"""

    class Meta:
        model = Track
        fields = ('id', 'name')
        read_only_fields = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for genre object"""

    class Meta:
        model = Genre
        fields = ('id', 'name')
        read_only_fields = ('id',)
