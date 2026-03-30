from django.urls import path

from . import web_views

app_name = "students_web"

urlpatterns = [
    path("", web_views.student_list, name="student-list"),
    path("courses/add/", web_views.course_create, name="course-create"),
    path("new/", web_views.student_create, name="student-create"),
    path("<int:pk>/edit/", web_views.student_update, name="student-update"),
    path("<int:pk>/delete/", web_views.student_delete, name="student-delete"),
]
