from django.contrib import messages


def user_logged_in(request, message):
    if not request.session.get('user'):
        messages.error(request, message)
        return False
    return True
