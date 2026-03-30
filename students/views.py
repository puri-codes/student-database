from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from .models import Course, Student
from .serializers import CourseSerializer, StudentSerializer


class CourseViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	permission_classes = [permissions.IsAuthenticated]
	filterset_fields = ["faculty", "code", "name"]
	search_fields = ["code", "name", "faculty"]
	ordering_fields = ["faculty", "code", "name"]


class StudentViewSet(viewsets.ModelViewSet):
	serializer_class = StudentSerializer
	permission_classes = [permissions.IsAuthenticated]
	parser_classes = [MultiPartParser, FormParser, JSONParser]
	filterset_fields = ["faculty", "academic_year", "year_of_enrollment"]
	search_fields = ["full_name", "student_id_number", "email", "phone_number"]
	ordering_fields = ["full_name", "student_id_number", "year_of_enrollment", "created_at"]

	def get_queryset(self):
		return (
			Student.objects.all()
			.prefetch_related("courses")
			.prefetch_related("enrollments__course")
		)
