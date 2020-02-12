from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Genre

from playlist.serializers import GenreSerializer


GENRES_URL = reverse('playlist:genre-list')


class PublicGenresAPITests(TestCase):
    """Test the publically available genres API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(GENRES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGenresAPITests(TestCase):
    """Test genres can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_genre_list(self):
        """Test retrieving a list of genres"""
        Genre.objects.create(user=self.user, name='Pop')
        Genre.objects.create(user=self.user, name='Rock')

        res = self.client.get(GENRES_URL)

        genres = Genre.objects.all().order_by('-name')
        serializer = GenreSerializer(genres, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_genres_limited_to_user(self):
        """Test that only genres for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        Genre.objects.create(user=user2, name='Techno')

        genre = Genre.objects.create(user=self.user, name='House')

        res = self.client.get(GENRES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], genre.name)

    def test_create_genre_successful(self):
        """Test creating a new genre"""
        payload = {'name': 'House'}
        self.client.post(GENRES_URL, payload)

        exists = Genre.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_genre_invalid(self):
        """Test creating invalid genre fails"""
        payload = {'name': ''}
        res = self.client.post(GENRES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
