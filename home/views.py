from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'index.html')


@login_required(login_url="/login/")
def job(request):
    return render(request, 'job.html')


@login_required(login_url="/login/")
def internship(request):
    return render(request, 'internship.html')


@login_required(login_url="/login/")
def contest(request):
    return render(request, 'contest.html')


@login_required(login_url="/login/")
def news(request):
    return render(request, 'news.html')


def contact(request):
    if request.method == "POST":
        q_name = request.POST.get('q_name')
        q_email = request.POST.get('q_email')
        q_subject = request.POST.get('q_subject')
        q_message = request.POST.get('q_message')

        # Create and save the contact query
        Contact.objects.create(
            q_name=q_name,
            q_email=q_email,
            q_subject=q_subject,
            q_message=q_message
        )
        messages.info(request, "Your query has been accepted. We will get back to you shortly.")
        return redirect("/contact/")

    return render(request, 'contact.html')


@login_required(login_url="/login/")
def student(request):
    return render(request, 'student.html')


@login_required(login_url="/login/")
def company(request):
    company = request.user.company
    # print("company",company)
    jobs = Job.objects.filter(company=company)
    internships = Internship.objects.filter(company=company)
    return render(request, 'company.html', {'jobs': jobs, 'internships': internships})


@login_required(login_url="/login/")
def postjob(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        field = request.POST.get('field')
        category = request.POST.get('category')
        pay_range = request.POST.get('pay_range')
        location = request.POST.get('location')
        expiry_date = request.POST.get('expiry_date')
        skills = request.POST.get('skills')

        # Save the job
        job = Job.objects.create(
            title=title,
            description=description,
            field=field,
            category=category,
            pay_range=pay_range,
            location=location,
            expiry_date=expiry_date,
            skills=skills,
            company=request.user.company,
            student_applied={}  # Initialize with an empty dictionary
        )
        messages.success(request, "Job posted successfully!")
        return redirect('/company/')

    return render(request, 'postjob.html')


@login_required(login_url="/login/")
def postinternship(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        field = request.POST.get('field')
        category = request.POST.get('category')
        stipend = request.POST.get('stipend')
        location = request.POST.get('location')
        expiry_date = request.POST.get('expiry_date')
        skills = request.POST.get('skills')

        # Save the internship
        internship = Internship.objects.create(
            title=title,
            description=description,
            field=field,
            category=category,
            stipend=stipend,
            location=location,
            expiry_date=expiry_date,
            skills=skills,
            company=request.user.company,
            student_applied={}  # Initialize with an empty dictionary
        )
        messages.success(request, "Internship posted successfully!")
        return redirect('/company/')

    return render(request, 'postinternship.html')

@login_required(login_url="/login/")
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, company=request.user.company)
    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.description = request.POST.get('description')
        job.field = request.POST.get('field')
        job.category = request.POST.get('category')
        job.pay_range = request.POST.get('pay_range')
        job.location = request.POST.get('location')
        job.expiry_date = request.POST.get('expiry_date')
        job.skills = request.POST.get('skills')
        job.save()
        messages.success(request, "Job updated successfully!")
        return redirect('/company/')
    return render(request, 'editjob.html', {'job': job})

@login_required(login_url="/login/")
def edit_internship(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id, company=request.user.company)
    if request.method == 'POST':
        internship.title = request.POST.get('title')
        internship.description = request.POST.get('description')
        internship.field = request.POST.get('field')
        internship.category = request.POST.get('category')
        internship.stipend = request.POST.get('stipend')
        internship.location = request.POST.get('location')
        internship.expiry_date = request.POST.get('expiry_date')
        internship.skills = request.POST.get('skills')
        internship.save()
        messages.success(request, "Internship updated successfully!")
        return redirect('/company/')
    return render(request, 'editinternship.html', {'internship': internship})


@login_required(login_url="/login/")
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, company=request.user.company)
    job.delete()
    messages.success(request, "Job deleted successfully!")
    return redirect('/company/')

@login_required(login_url="/login/")
def delete_internship(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id, company=request.user.company)
    internship.delete()
    messages.success(request, "Internship deleted successfully!")
    return redirect('/company/')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalid Username")
            return redirect("/login/")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Invalid Password")
            return redirect("/login/")
        else:
            login(request, user)

            # Redirect based on whether the user is a student or a company
            if hasattr(user, 'student'):
                return redirect('/student/')
            elif hasattr(user, 'company'):
                return redirect('/company/')

            return redirect("/")

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect("/")


def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect("/signup/")
        else:
            user = User.objects.create_user(
                first_name=first_name,
                email=email,
                username=username,
                password=password
            )

            # Create account based on user type
            if user_type == "student":
                Student.objects.create(user=user, college='', branch='', github='', linkedin='')
                messages.success(request, "Student account created successfully")
            elif user_type == "company":
                Company.objects.create(user=user, company_name=first_name, phone_number='', email=email, website='', location='')
                messages.success(request, "Company account created successfully")

            return redirect("/login/")

    return render(request, 'signup.html')
