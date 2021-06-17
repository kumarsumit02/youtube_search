from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.video_search.views import VideoDataApi, ApiKeyDataApi


router=DefaultRouter()
router.register("api/v1/videos", VideoDataApi, basename="Videos")
router.register("api/v1/api_key", ApiKeyDataApi, basename="API Keys")

urlpatterns = [
    path('', include(router.urls) ),
]
