from django.urls import path, include
from rest_framework.routers import DefaultRouter

from playlist import views


router = DefaultRouter()
router.register('tracks', views.TrackViewSet)
router.register('ingredients', views.GenreViewSet)

app_name = 'playlist'

urlpatterns = [
    path('', include(router.urls))
]
