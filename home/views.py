from datetime import datetime
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q
import random

def home(request):
    return render(request, 'index.html')


def job(request):
    jobs = Job.objects.all()
    return render(request, 'job.html', {'jobs': jobs})


def internship(request):
    # Get filter parameters from the request
    stipend_ranges = request.GET.getlist('stipend', [])
    category = request.GET.get('category', '')
    internship_type = request.GET.get('internship_type', '')
    location = request.GET.get('location', '')

    # Start with all internships
    internships = Internship.objects.all()

    # Apply stipend range filter
    if stipend_ranges:
        stipend_filters = Q()
        for stipend_range in stipend_ranges:
            if stipend_range == '0-5000':
                stipend_filters |= Q(stipend__lte=5000)
            elif stipend_range == '5001-10000':
                stipend_filters |= Q(stipend__gt=5000, stipend__lte=10000)
            elif stipend_range == '10001-15000':
                stipend_filters |= Q(stipend__gt=10000, stipend__lte=15000)
            elif stipend_range == '15001-20000':
                stipend_filters |= Q(stipend__gt=15000, stipend__lte=20000)
            elif stipend_range == '20001+':
                stipend_filters |= Q(stipend__gt=20000)
        internships = internships.filter(stipend_filters)

    # Apply category filter
    if category:
        internships = internships.filter(category__icontains=category)

    # Apply internship type filter
    if internship_type:
        internships = internships.filter(type__icontains=internship_type)

    # Apply location filter
    if location:
        internships = internships.filter(location__icontains=location)

    return render(request, 'internship.html', {'internships': internships})


def contest(request):
    return render(request, 'contest.html')


def bookmark(request):
    return render(request, 'bookmark.html')


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
    student = request.user.student
    applied_jobs = Job.objects.filter(student_applied__has_key=str(student.id))
    applied_internships = Internship.objects.filter(student_applied__has_key=str(student.id))
    student_tests = StudentTestData.objects.filter(student=student)

    # Extract test details from SubjectTestData
    test_details = []
    for student_test in student_tests:
        test = student_test.test
        test_details.append({
            'subject': test.subject,
            'score': test.score,
            'test_date': test.testDate
        })
    print(test_details)
    return render(request, 'student.html', {'applied_jobs': applied_jobs, 'applied_internships': applied_internships, 'test_details':test_details})

@login_required(login_url="/login/")
def edit_student(request):
    student = get_object_or_404(Student, user=request.user)
    
    if request.method == 'POST':
        student.college = request.POST.get('college')
        student.branch = request.POST.get('branch')
        student.github = request.POST.get('github')
        student.linkedin = request.POST.get('linkedin')
        student.email = request.POST.get('email')
        
        # Update profile picture if a new one is uploaded
        if 'profile_picture' in request.FILES:
            student.profile_picture = request.FILES['profile_picture']
        
        # Save the changes
        student.save()
        messages.success(request, "Student profile updated successfully!")
        return redirect('/student/')  # Redirect to a relevant page after saving
    
    return render(request, 'editstudent.html', {'student': student})


@login_required(login_url="/login/")
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    student = request.user.student
    if str(student.id) not in job.student_applied:
        job.student_applied[str(student.id)] = {'applied_date': datetime.now().strftime('%Y-%m-%d')}
        job.save()
        messages.success(request, "Applied for the job successfully!")
    else:
        messages.info(request, "You have already applied for this job.")
    return redirect('/job/')

@login_required(login_url="/login/")
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, company=request.user.company)
    applicants = []
    for student_id, application_details in job.student_applied.items():
        student = get_object_or_404(Student, id=student_id)
        applicants.append({
            'student': student,
            'application_details': application_details
        })
    return render(request, 'job_applicants.html', {'job': job, 'applicants': applicants})


@login_required(login_url="/login/")
def apply_internship(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id)
    student = request.user.student
    if str(student.id) not in internship.student_applied:
        internship.student_applied[str(student.id)] = {'applied_date': datetime.now().strftime('%Y-%m-%d')}
        internship.save()
        messages.success(request, "Applied for the internship successfully!")
    else:
        messages.info(request, "You have already applied for this internship.")
    return redirect('/internship/')

@login_required(login_url="/login/")
def internship_applicants(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id, company=request.user.company)
    applicants = []
    for student_id, application_details in internship.student_applied.items():
        student = get_object_or_404(Student, id=student_id)
        applicants.append({
            'student': student,
            'application_details': application_details
        })
    return render(request, 'internship_applicants.html', {'internship': internship, 'applicants': applicants})


@login_required(login_url="/login/")
def company(request):
    company = request.user.company
    jobs = Job.objects.filter(company=company)
    internships = Internship.objects.filter(company=company)
    students = Student.objects.all()
    return render(request, 'company.html', {'jobs': jobs, 'internships': internships, 'students':students})


@login_required(login_url="/login/")
def edit_company(request):
    company = get_object_or_404(Company, user=request.user)

    if request.method == 'POST':
        company.company_name = request.POST.get('company_name')
        company.phone_number = request.POST.get('phone_number')
        company.email = request.POST.get('email')
        company.website = request.POST.get('website')
        company.location = request.POST.get('location')

        # Update profile picture if a new one is uploaded
        if 'profile_picture' in request.FILES:
            company.profile_picture = request.FILES['profile_picture']

        company.save()
        messages.success(request, "Company profile updated successfully!")
        return redirect('/company/')

    return render(request, 'editcompany.html', {'company': company})



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


@login_required(login_url="/login/")
def quiz(request):
    if request.method == "POST":
        if "subject" in request.POST:
            # Handle subject selection
            subject = request.POST["subject"]
            questions = Question.objects.filter(subject=subject)
            selected_questions = random.sample(
                list(questions), min(len(questions), 10)
            )
            request.session['selected_questions'] = [
                {
                    'id': q.questionId,
                    'question': q.question,
                    'option_1': q.option_1,
                    'option_2': q.option_2,
                    'option_3': q.option_3,
                    'option_4': q.option_4,
                    'answer': q.correct_answer,  # Store the correct answer as 'A', 'B', etc.
                }
                for q in selected_questions
            ]
            return render(request, 'quiz.html', {
                'questions': request.session['selected_questions'],
                'subject': subject
            })
        else:
            # Handle answer submission
            user_answers = request.POST.dict()
            selected_questions = request.session.get('selected_questions', [])
            correct_count = 0
            questions_with_answers = []  # This will store the question, user answer, and correct result

            dic = {"option_1": "A", "option_2": "B", "option_3": "C", "option_4": "D"}

            for question in selected_questions:
                question_id = str(question['id'])
                correct_answer = Question.objects.get(questionId=question_id).correct_answer  # Fetch the correct answer from DB
                subject = Question.objects.get(questionId=question_id).subject
                user_answer = user_answers.get(question_id)
                
                # Determine if the answer is correct
                is_correct = dic.get(user_answer) == correct_answer
                correct_count += 1 if is_correct else 0

                # Save the question, user answer, and correct result
                questions_with_answers.append({
                    'question': question['question'],
                    'user_answer': dic.get(user_answer),
                    'correct_answer': correct_answer,
                    'is_correct': is_correct
                })

            total_questions = len(selected_questions)
            score = correct_count  # The score will be the number of correct answers

            # Save the test result in the Test table
            test = SubjectTestData.objects.create(
                subject=subject,
                score=score,
                questions=questions_with_answers  # Store the questions and answers as JSON
            )

            # Update the StudentTest table
            student_test, created = StudentTestData.objects.get_or_create(
                student=request.user.student,
                test=test
            )

            if subject == "Mathematics":
                # If the test is Mathematics, update the score if it's higher
                if student_test.mathematics_score < score:
                    student_test.mathematics_score = score  # Update the score for Mathematics
            elif subject == "Machine Learning":
                # If the test is Machine Learning, update the score if it's higher
                if student_test.machine_learning_score < score:
                    student_test.machine_learning_score = score  # Update the score for Machine Learning

            # Update test count and last test score
            student_test.test_count += 1  # Increment the test count
            student_test.last_test_score = score  # Update the most recent score
            student_test.save()

            return render(request, 'quiz.html', {
                'result': True,
                'correct_count': correct_count,
                'total_questions': total_questions
            })

    # If GET request, display subject selection
    subjects = Question.objects.values_list('subject', flat=True).distinct()
    return render(request, 'quiz.html', {'subjects': subjects})

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
                Student.objects.create(user=user, email= email, student_name = first_name, college='', branch='', github='', linkedin='', profile_picture='home/static/img/blank-profile.webp')
                messages.success(request, "Student account created successfully")
            elif user_type == "company":
                Company.objects.create(user=user, company_name=first_name, phone_number='', email=email, website='', location='', profile_picture='home/static/img/blank-profile.webp')
                messages.success(request, "Company account created successfully")

            return redirect("/login/")

    return render(request, 'signup.html')
