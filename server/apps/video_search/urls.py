from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.video_search.dash_render import load_dashboard_videos
from apps.video_search.views import VideoDataApi, ApiKeyDataApi


# Register the API urls
router = DefaultRouter()
router.register("videos", VideoDataApi, basename="Videos")
router.register("api_key", ApiKeyDataApi, basename="API Keys")

urlpatterns = [
    path('', load_dashboard_videos),
    path('api/v1/', include(router.urls)),
]
