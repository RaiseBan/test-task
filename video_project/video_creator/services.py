import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

from django.conf import settings


def generate_scrolling_text_video(text):
    width, height = 100, 100
    fps = 24
    duration = 3
    font_size = 40

    frame_count = int(fps * duration)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    video_stream = BytesIO()

    out = cv2.VideoWriter('temp.mp4', fourcc, fps, (width, height))

    font_path = os.path.join(settings.BASE_DIR, 'video_creator', 'static', 'fonts', 'arial.ttf')
    font = ImageFont.truetype(font_path, font_size)

    text_x = width
    text_y = height // 2 - font_size // 2

    text_width, text_height = font.getbbox(text)[2], font.getbbox(text)[3]
    speed = (text_width + width) / frame_count

    for i in range(frame_count):
        img_pil = Image.new("RGB", (width, height), (255, 0, 255))
        draw = ImageDraw.Draw(img_pil)
        draw.text((int(text_x), int(text_y)), text, font=font, fill=(255, 255, 255))
        frame = np.array(img_pil)
        out.write(frame)
        text_x -= speed

    out.release()

    with open('temp.mp4', 'rb') as video_file:
        video_stream.write(video_file.read())

    video_stream.seek(0)

    return video_stream
