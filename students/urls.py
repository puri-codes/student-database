from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, StudentViewSet

router = DefaultRouter()
router.register("students", StudentViewSet, basename="student")
router.register("courses", CourseViewSet, basename="course")

urlpatterns = [
    path("", include(router.urls)),
]
