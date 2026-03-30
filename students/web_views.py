from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CourseForm, StudentForm
from .models import Course, Student


@login_required
def student_list(request):
    faculty = request.GET.get("faculty")
    academic_year = request.GET.get("academic_year")

    students = Student.objects.all().prefetch_related("courses")
    courses = Course.objects.all().order_by("faculty", "code")
    if faculty:
        students = students.filter(faculty=faculty)
    if academic_year:
        students = students.filter(academic_year=academic_year)

    context = {
        "students": students,
        "courses": courses,
        "course_form": CourseForm(),
        "faculty_choices": Student.FacultyChoices.choices,
        "year_choices": Student.AcademicYearChoices.choices,
        "active_faculty": faculty,
        "active_year": academic_year,
    }
    return render(request, "students/student_list.html", context)


@login_required
@transaction.atomic
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            selected_courses = form.cleaned_data.get("courses")
            student = form.save()
            student.courses.set(selected_courses)
            messages.success(request, "Student created successfully.")
            return redirect("students_web:student-list")
    else:
        form = StudentForm()

    return render(
        request,
        "students/student_form.html",
        {"form": form, "title": "Add Student", "submit_label": "Create Student"},
    )


@login_required
@transaction.atomic
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            selected_courses = form.cleaned_data.get("courses")
            student = form.save()
            student.courses.set(selected_courses)
            messages.success(request, "Student updated successfully.")
            return redirect("students_web:student-list")
    else:
        form = StudentForm(instance=student)
        form.fields["courses"].initial = student.courses.all()

    return render(
        request,
        "students/student_form.html",
        {"form": form, "title": "Edit Student", "submit_label": "Save Changes"},
    )


@login_required
@transaction.atomic
def student_delete(request, pk):
    if request.method != "POST":
        return redirect("students_web:student-list")

    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect("students_web:student-list")


@login_required
@transaction.atomic
def course_create(request):
    if request.method != "POST":
        return redirect("students_web:student-list")

    form = CourseForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Course created successfully.")
        return redirect("students_web:student-list")

    students = Student.objects.all().prefetch_related("courses")
    context = {
        "students": students,
        "courses": Course.objects.all().order_by("faculty", "code"),
        "course_form": form,
        "faculty_choices": Student.FacultyChoices.choices,
        "year_choices": Student.AcademicYearChoices.choices,
        "active_faculty": "",
        "active_year": "",
        "show_course_form": True,
    }
    return render(request, "students/student_list.html", context)
