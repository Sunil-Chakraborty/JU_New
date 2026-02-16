from django.db import models


# https://jadavpuruniversity.in/storage/2026/01/IQAC-Newsletter_December-2025.pdf

# https://sunilju.pythonanywhere.com/tracker/report/iqac-newsletter/



class TrackLink(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    target_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ClickLog(models.Model):
    link = models.ForeignKey(TrackLink, on_delete=models.CASCADE, related_name="clicks")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    device = models.CharField(max_length=100, blank=True)
    browser = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.link.name} - {self.clicked_at}"
