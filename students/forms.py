from django import forms

from .models import Course, Student


class CourseChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.get_faculty_display()} | {obj.code} - {obj.name}"


class StudentForm(forms.ModelForm):
    courses = CourseChoiceField(
        queryset=Course.objects.select_related().all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"size": 8}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["courses"].queryset = Course.objects.all().order_by("faculty", "code")

    class Meta:
        model = Student
        fields = [
            "full_name",
            "guardian_name",
            "student_id_number",
            "phone_number",
            "guardian_phone_number",
            "emergency_contact_number",
            "email",
            "faculty",
            "academic_year",
            "year_of_enrollment",
            "profile_image",
            "courses",
        ]
        widgets = {
            "year_of_enrollment": forms.NumberInput(attrs={"min": 1900, "max": 2100}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["faculty", "code", "name", "description"]
