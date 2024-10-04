from django.db import models
from django.contrib.auth.models import User


# Users table, extended from Django's built-in User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
    is_student = models.BooleanField(default=True)


# Contest Model
class Contest(models.Model):
    title = models.CharField(max_length=1000)
    link = models.URLField()
    description = models.TextField(blank=True, null=True)  # A short description of the contest
    start_date = models.DateField(blank=True, null=True)  # Optional start date
    end_date = models.DateField(blank=True, null=True)  # Optional end date
    prize = models.CharField(max_length=100, blank=True, null=True)  # Prize details
    location = models.CharField(max_length=200, blank=True, null=True)  # Online or In-person
    tags = models.CharField(max_length=300, blank=True, null=True)  # Tags like AI, ML, DS, etc.
    participants = models.IntegerField(default=0)  # Number of participants
    likes = models.IntegerField(default=0)  # Field to store the number of likes

    def __str__(self):
        return self.title


# News Model
class News(models.Model):
    headline = models.CharField(max_length=1000)
    summary = models.TextField()  # Using TextField for longer summaries
    link = models.URLField()
    published_date = models.DateField(blank=True, null=True)  # Optional published date
    source = models.CharField(max_length=255, blank=True, null=True)  # Source of the news article
    tags = models.CharField(max_length=300, blank=True, null=True)  # Tags for classification like AI, ML, etc.
    likes = models.IntegerField(default=0)  # Field to store the number of likes

    def __str__(self):
        return self.headline


# Contact Model
class Contact(models.Model):
    q_name = models.CharField(max_length=100)
    q_email = models.EmailField()
    q_subject = models.CharField(max_length=1000)
    q_message = models.TextField()


# Company table
class Company(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField()
    location = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos/')

    def __str__(self):
        return self.company_name


# Jobs table
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField()
    field = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    pay_range = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    expiry_date = models.DateField()
    created_date = models.DateField(auto_now_add=True)
    skills = models.TextField()
    student_applied = models.JSONField()  # To store hashmap of students applied

    def __str__(self):
        return f"{self.company} - {self.category}"


# Internship table (Similar to Job)
class Internship(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField()
    field = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    stipend = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    expiry_date = models.DateField()
    created_date = models.DateField(auto_now_add=True)
    skills = models.TextField()
    student_applied = models.JSONField()  # To store hashmap of students applied

    def __str__(self):
        return f"{self.company} - {self.category}"


# Student table
class Student(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    college = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    github = models.URLField()
    linkedin = models.URLField()
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.user.user.username


# Student Dashboard table
class StudentDashboard(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    jobs_applied = models.JSONField()  # To store hashmap of job applications
    internship_applied = models.JSONField()  # To store hashmap of internship applications


# Company Dashboard table
class CompanyDashboard(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    jobs = models.ManyToManyField(Job)
    internships = models.ManyToManyField(Internship)


# Student Bookmark table
class StudentBookmark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    jobs = models.ManyToManyField(Job)
    internships = models.ManyToManyField(Internship)
    bookmark_date = models.DateTimeField(auto_now_add=True)


# Job Application table
class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='job_applications/')
    cover_letter = models.TextField(blank=True, null=True)  # Optional cover letter
    date_applied = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} applied for {self.job}"


# Internship Application table
class InternshipApplication(models.Model):
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='internship_applications/')
    cover_letter = models.TextField(blank=True, null=True)  # Optional cover letter
    date_applied = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} applied for {self.internship}"
