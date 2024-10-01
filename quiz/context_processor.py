# quiz/context_processors.py
def user_is_admin(request):
    return {
        'is_admin': request.user.groups.filter(name="Admin").exists()
    }
