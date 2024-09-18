from django.http import FileResponse, JsonResponse
from django.shortcuts import render

from .services import generate_scrolling_text_video
from .models import RequestLog
from django.core.cache import cache
from rest_framework.decorators import api_view


@api_view(['GET'])
def create_video(request):
    text = request.GET.get('text', 'Бегущая строка!')

    cache_key = f"video_{text}"
    cached_video = cache.get(cache_key)

    if cached_video:
        print(f"Видео для текста '{text}' взято из кеша.")
        return FileResponse(cached_video, as_attachment=True, filename='scrolling_text.mp4', content_type='video/mp4')

    try:
        video_stream = generate_scrolling_text_video(text)

        cache.set(cache_key, video_stream, timeout=86400)

        log_entry = RequestLog(text=text)
        log_entry.save()

        return FileResponse(video_stream, as_attachment=True, filename='scrolling_text.mp4', content_type='video/mp4')

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def home(request):
    return render(request, 'video_creator/home.html')
