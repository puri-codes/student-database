from django.contrib import admin
from django.utils.html import format_html

from .models import Course, Enrollment, Student


class EnrollmentInline(admin.TabularInline):
	model = Enrollment
	extra = 1
	autocomplete_fields = ["course"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = (
		"student_id_number",
		"full_name",
		"guardian_name",
		"email",
		"faculty",
		"academic_year",
		"year_of_enrollment",
		"profile_image_preview",
	)
	list_filter = ("faculty", "academic_year", "year_of_enrollment")
	search_fields = (
		"student_id_number",
		"full_name",
		"guardian_name",
		"email",
		"phone_number",
		"emergency_contact_number",
	)
	ordering = ("full_name",)
	inlines = [EnrollmentInline]

	fieldsets = (
		(
			"Identity",
			{
				"fields": (
					"student_id_number",
					"full_name",
					"guardian_name",
					"email",
					"profile_image",
				)
			},
		),
		(
			"Contact",
			{"fields": ("phone_number", "guardian_phone_number", "emergency_contact_number")},
		),
		(
			"Academic",
			{
				"fields": (
					"faculty",
					"academic_year",
					"year_of_enrollment",
				)
			},
		),
	)

	@admin.display(description="Image")
	def profile_image_preview(self, obj):
		if not obj.profile_image:
			return "No image"
		return format_html(
			'<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:4px;" />',
			obj.profile_image.url,
		)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ("faculty", "code", "name")
	list_filter = ("faculty",)
	search_fields = ("code", "name")
	ordering = ("code",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
	list_display = ("student", "course", "enrolled_at")
	list_filter = ("course", "enrolled_at")
	search_fields = ("student__student_id_number", "student__full_name", "course__code")
