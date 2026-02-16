from django.shortcuts import get_object_or_404, redirect, render
from .models import TrackLink, ClickLog
from user_agents import parse
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
from .models import TrackLink, ClickLog


def track_redirect(request, slug):
    link = get_object_or_404(TrackLink, slug=slug)

    # Get IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    # Parse device info
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)

    device = "Mobile" if user_agent.is_mobile else "Tablet" if user_agent.is_tablet else "PC"
    browser = user_agent.browser.family
    os = user_agent.os.family

    # Save click
    ClickLog.objects.create(
        link=link,
        ip_address=ip,
        user_agent=user_agent_string,
        device=device,
        browser=browser,
        os=os
    )

    return redirect(link.target_url)


def analytics(request):
    links = TrackLink.objects.all()
    return render(request, "tracker/analytics.html", {"links": links})


def report(request, slug):
    link = get_object_or_404(TrackLink, slug=slug)
    clicks = ClickLog.objects.filter(link=link).order_by('-clicked_at')

    # totals
    total_clicks = clicks.count()
    unique_visitors = clicks.values('ip_address').distinct().count()

    today = now().date()
    today_clicks = clicks.filter(clicked_at__date=today).count()

    # device stats
    device_stats = clicks.values('device').annotate(total=Count('id')).order_by('-total')

    # browser stats
    browser_stats = clicks.values('browser').annotate(total=Count('id')).order_by('-total')

    # last 7 days trend
    last7 = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = clicks.filter(clicked_at__date=day).count()
        last7.append((day, count))

    context = {
        "link": link,
        "total_clicks": total_clicks,
        "unique_visitors": unique_visitors,
        "today_clicks": today_clicks,
        "device_stats": device_stats,
        "browser_stats": browser_stats,
        "last7": last7,
        "clicks": clicks[:50],
    }

    return render(request, "tracker/report.html", context)
