from django.urls import path, include
from rest_framework.routers import DefaultRouter

from playlist import views


router = DefaultRouter()
router.register('tracks', views.TrackViewSet)

app_name = 'playlist'

urlpatterns = [
    path('', include(router.urls))
]
