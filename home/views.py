from home.models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

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
    # Student-specific dashboard logic
    return render(request, 'student.html')


@login_required(login_url="/login/")
def company(request):
    # Company-specific dashboard logic
    return render(request, 'company.html')


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

            # Check if the user is a student or a company based on the user profile
            if hasattr(user, 'userprofile'):
                if user.userprofile.is_student:
                    # If the user is a student, redirect to the student dashboard
                    return redirect('/student/')
                else:
                    # If the user is a company, redirect to the company dashboard
                    return redirect('/company/')
            
            # Fallback if user type is not identified (optional)
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
        user_type = request.POST.get('user_type')  # Retrieve the user type from the form

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect("/signup/")
        else:
            # Create a new user
            user = User.objects.create_user(
                first_name=first_name,
                email=email,
                username=username,
                password=password
            )

            # Create a UserProfile linked to the user
            user_profile = UserProfile.objects.create(user=user, is_student=(user_type == "student"))

            if user_type == "student":
                # Create a student profile and record
                Student.objects.create(user=user_profile, college='', branch='', github='', linkedin='', resume='')
                messages.info(request, "Student account created successfully")
            elif user_type == "company":
                # Create a company profile and record
                Company.objects.create(user=user_profile, company_name=first_name, phone_number='', email=email, website='', location='', logo='')
                messages.info(request, "Company account created successfully")

            return redirect("/login/")  # Redirect to the login page after successful signup

    return render(request, 'signup.html')
