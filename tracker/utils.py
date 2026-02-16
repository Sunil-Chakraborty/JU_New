import qrcode
from django.conf import settings
import os

def generate_qr(slug):
    url = f"{settings.SITE_URL}/r/{slug}/"

    img = qrcode.make(url)

    path = os.path.join(settings.MEDIA_ROOT, f"qr_{slug}.png")
    img.save(path)

    return f"{settings.MEDIA_URL}qr_{slug}.png"
