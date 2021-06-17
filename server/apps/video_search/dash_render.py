from django.shortcuts import render

from apps.video_search.models import Videos
from apps.video_search.filters import VideoFilter


def load_dashboard_videos(request):
    """Function to render the content in the Dashboard """

    all_videos = Videos.get_all_videos()

    myFilter = VideoFilter(request.GET, queryset=all_videos)
    videos = myFilter.qs

    row_count = videos.count()

    context = {
        'videos': videos,
        'myFilter': myFilter,
        'row_count': row_count
    }

    return render(request, 'video_search/dashboard.html', context)
