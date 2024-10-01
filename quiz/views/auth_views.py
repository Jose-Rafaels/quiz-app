from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from ..models import Quiz


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # Validasi form input
        if not username or not email or not password or not role:
            return render(
                request,
                "registration/register.html",
                {"error": "All fields are required."},
            )

        if role not in ["admin", "user"]:
            return render(
                request,
                "registration/register.html",
                {"error": "Invalid role selection."},
            )

        # Periksa apakah username atau email sudah terdaftar
        if User.objects.filter(username=username).exists():
            return render(
                request,
                "registration/register.html",
                {"error": "Username already exists."},
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "registration/register.html",
                {"error": "Email already exists."},
            )

        # Membuat user baru dengan password terenkripsi
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),  # Enkripsi password
        )

        # Menambahkan user ke group yang sesuai
        if role == "admin":
            admin_group = Group.objects.get(
                name="Admin"
            )  # Pastikan group 'Admin' sudah ada
            user.groups.add(admin_group)
        else:
            user_group = Group.objects.get(
                name="User"
            )  # Pastikan group 'User' sudah ada
            user.groups.add(user_group)

        # Login otomatis setelah register
        login(request, user)

        # Redirect ke dashboard atau halaman lain setelah registrasi sukses
        return redirect("dashboard")

    return render(request, "registration/register.html")


@login_required
def dashboard(request):
    is_admin = request.user.groups.filter(name="Admin").exists()
    # print(request.user)
    if is_admin:  # Jika admin (staff)
        # Ambil semua kuis yang dibuat oleh admin tersebut
        quizzes = Quiz.objects.filter(created_by=request.user)
    else:
        # Jika bukan admin, ambil kuis yang telah dikerjakan user
        quizzes = Quiz.objects.filter(quizattempt__user=request.user).distinct()
    context = {"is_admin": is_admin, "quizzes": quizzes}
    return render(request, "dashboard.html", context)


def home_page(request):
    quizzes = Quiz.objects.all()[:3]
    return render(request, 'home_page.html', {'quizzes': quizzes})


@login_required
def logout_view(request):
    """
    Fungsi ini menangani logout pengguna dan mengarahkan kembali ke halaman utama.
    """
    logout(request)
    return redirect("home_page")
