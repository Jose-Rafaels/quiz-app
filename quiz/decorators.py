from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect, render


def admin_required(view_func):
    """
    Custom decorator to check if the user is an admin.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.groups.filter(name="Admin").exists():
            return render(
            request,
            "error_page.html",
            {"message": "You do not have permission to view this page"},
        ) # Bisa diarahkan ke halaman khusus
        return view_func(request, *args, **kwargs)

    return _wrapped_view
