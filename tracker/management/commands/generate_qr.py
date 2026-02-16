from django.core.management.base import BaseCommand
from tracker.models import TrackLink
from tracker.utils import generate_qr

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for link in TrackLink.objects.all():
            path = generate_qr(link.slug)
            self.stdout.write(self.style.SUCCESS(f"QR Generated: {path}"))
