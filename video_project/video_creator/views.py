from django.http import FileResponse, JsonResponse
from .services import generate_scrolling_text_video


def create_video(request):
    text = request.GET.get('text', 'Бегущая строка!')

    try:
        video_stream = generate_scrolling_text_video(text)

        return FileResponse(video_stream, as_attachment=True, filename='scrolling_text.mp4', content_type='video/mp4')

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
