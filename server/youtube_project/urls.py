from django.urls import path, include

urlpatterns = [
    path('', include("apps.video_search.urls")),
]
