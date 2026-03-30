from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


phone_validator = RegexValidator(
	regex=r"^\+?[0-9]{10,15}$",
	message="Phone number must be 10-15 digits and may start with +.",
)


class Course(models.Model):
	class FacultyChoices(models.TextChoices):
		BSIT = "bsit", "BSIT"
		MSIT = "msit", "MSIT"
		BBA = "bba", "BBA"
		MBA = "mba", "MBA"

	code = models.CharField(max_length=20, unique=True)
	name = models.CharField(max_length=120, unique=True)
	faculty = models.CharField(
		max_length=30,
		choices=FacultyChoices.choices,
		default=FacultyChoices.BSIT,
	)
	description = models.TextField(blank=True)

	class Meta:
		ordering = ["code"]
		indexes = [
			models.Index(fields=["code"], name="course_code_idx"),
			models.Index(fields=["name"], name="course_name_idx"),
			models.Index(fields=["faculty", "code"], name="course_faculty_code_idx"),
		]

	def __str__(self):
		return f"{self.get_faculty_display()} | {self.code} - {self.name}"


class Student(models.Model):
	class FacultyChoices(models.TextChoices):
		BSIT = "bsit", "BSIT"
		MSIT = "msit", "MSIT"
		BBA = "bba", "BBA"
		MBA = "mba", "MBA"

	class AcademicYearChoices(models.TextChoices):
		YEAR_1 = "year_1", "Year 1"
		YEAR_2 = "year_2", "Year 2"
		YEAR_3 = "year_3", "Year 3"
		YEAR_4 = "year_4", "Year 4"

	full_name = models.CharField(max_length=200)
	guardian_name = models.CharField(max_length=200, default="Unknown Guardian")
	phone_number = models.CharField(max_length=16, validators=[phone_validator])
	guardian_phone_number = models.CharField(max_length=16, validators=[phone_validator])
	emergency_contact_number = models.CharField(
		max_length=16,
		validators=[phone_validator],
		default="+10000000000",
	)
	email = models.EmailField(unique=True)
	faculty = models.CharField(max_length=30, choices=FacultyChoices.choices)
	academic_year = models.CharField(max_length=20, choices=AcademicYearChoices.choices)
	student_id_number = models.CharField(max_length=30, unique=True)
	year_of_enrollment = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900)])
	profile_image = models.ImageField(upload_to="students/", blank=True, null=True)
	courses = models.ManyToManyField(Course, through="Enrollment", related_name="students")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["full_name", "student_id_number"]
		indexes = [
			models.Index(fields=["student_id_number"], name="student_sid_idx"),
			models.Index(fields=["email"], name="student_email_idx"),
			models.Index(fields=["faculty", "academic_year"], name="student_fac_year_idx"),
			models.Index(fields=["year_of_enrollment"], name="student_enroll_year_idx"),
		]

	def __str__(self):
		return f"{self.student_id_number} - {self.full_name}"


class Enrollment(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
	enrolled_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-enrolled_at"]
		constraints = [
			models.UniqueConstraint(
				fields=["student", "course"],
				name="unique_student_course_enrollment",
			)
		]
		indexes = [
			models.Index(fields=["student", "course"], name="enrollment_sc_idx"),
			models.Index(fields=["course"], name="enrollment_course_idx"),
		]

	def __str__(self):
		return f"{self.student.student_id_number} -> {self.course.code}"
