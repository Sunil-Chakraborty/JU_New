from django.contrib.messages import get_messages

def clear_messages(request):
    """
    Clears all queued Django messages from the session.
    Useful before rendering login / otp / sensitive pages.
    """
    storage = get_messages(request)
    for _ in storage:
        pass
        
