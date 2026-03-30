from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import Course, Student


api_phone_validator = RegexValidator(
    regex=r"^\+?[0-9]{10,15}$",
    message="Phone number must be 10-15 digits and may start with +.",
)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "faculty", "code", "name", "description"]


class StudentSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    course_ids = serializers.PrimaryKeyRelatedField(
        source="courses",
        many=True,
        queryset=Course.objects.all(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Student
        fields = [
            "id",
            "full_name",
            "guardian_name",
            "phone_number",
            "guardian_phone_number",
            "emergency_contact_number",
            "email",
            "faculty",
            "academic_year",
            "student_id_number",
            "year_of_enrollment",
            "profile_image",
            "courses",
            "course_ids",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_phone_number(self, value):
        api_phone_validator(value)
        return value

    def validate_guardian_phone_number(self, value):
        api_phone_validator(value)
        return value

    def validate_emergency_contact_number(self, value):
        api_phone_validator(value)
        return value

    def validate_year_of_enrollment(self, value):
        if value > 2100:
            raise serializers.ValidationError("Year of enrollment appears invalid.")
        return value

    def validate(self, attrs):
        student_phone = attrs.get("phone_number")
        guardian_phone = attrs.get("guardian_phone_number")
        emergency_phone = attrs.get("emergency_contact_number")
        if student_phone and guardian_phone and student_phone == guardian_phone:
            raise serializers.ValidationError(
                {"guardian_phone_number": "Guardian phone must differ from student phone."}
            )
        if emergency_phone and student_phone and emergency_phone == student_phone:
            raise serializers.ValidationError(
                {"emergency_contact_number": "Emergency contact must differ from student phone."}
            )
        return attrs
