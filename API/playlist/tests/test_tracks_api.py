from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Track

from playlist.serializers import TrackSerializer


TRACKS_URL = reverse('playlist:track-list')


class PublicTracksApiTests(TestCase):
    """Test the publicly available tracks API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving tracks"""
        res = self.client.get(TRACKS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTracksApiTests(TestCase):
    """Test the authorized user tracks API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tracks(self):
        """Test retrieving tracks"""
        Track.objects.create(artist=self.user, title='Sylia')
        Track.objects.create(artist=self.user, title='Hayk')

        res = self.client.get(TRACKS_URL)

        tracks = Track.objects.all().order_by('-title')
        serializer = TrackSerializer(tracks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tracks_limited_to_user(self):
        """Test that tracks returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        Track.objects.create(artist=user2, title='Boom')
        track = Track.objects.create(artist=self.user, title='Shadows')

        res = self.client.get(TRACKS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], track.title)
