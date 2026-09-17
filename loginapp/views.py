from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .forms import StudentForm
from .models import Student
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Registration successful!")
        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")
@login_required
@login_required
def dashboard(request):
    students = Student.objects.all()
    return render(request, "dashboard.html", {"students": students})
@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = StudentForm()

    return render(request, "add_student.html", {"form": form})
def logout_view(request):
    logout(request)
    return redirect("login")
@login_required
def edit_student(request, id):
    student = Student.objects.get(id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = StudentForm(instance=student)

    return render(request, "edit_student.html", {"form": form})
@login_required
def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect("dashboard")