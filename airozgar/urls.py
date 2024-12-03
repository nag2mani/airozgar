from home.views import *
from django.urls import path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name='home'),

    path('job/', job, name='job'),
    path('internship/', internship, name='internship'),
    path("contest/", contest, name='contest'),
    path("news/", news, name='news'),
    path("contact/", contact, name='contact'),

    path("login/", login_page, name='login'),
    path("logout/", logout_page, name='logout'),
    path("signup/", signup, name='signup'),

    path('student/', student, name='student'),
    path('bookmark/', bookmark, name='bookmark'),
    path('editstudent/', edit_student, name='edit_student'),

    path('applyjob/<int:job_id>/', apply_job, name='apply_job'),
    path('applyinternship/<int:internship_id>/', apply_internship, name='apply_internship'),
    path('company/', company, name='company'),
    path('editcompany/', edit_company, name='edit_company'),
    
    path('postjob/', postjob, name='postjob'),
    path('hardapply/', hardapply, name='hardapply'),
    path('postinternship/', postinternship, name='postinternship'),
    path('job_applicants/<int:job_id>/', job_applicants, name='job_applicants'),
    path('update-application-status/<int:job_id>/<int:student_id>/', update_application_status, name='update_application_status'),
    path('student-applications/', student_applications, name='student_applications'),
    path('internship_applicants/<int:internship_id>/', internship_applicants, name='internship_applicants'),

    path('editjob/<int:job_id>/', edit_job, name='edit_job'),
    path('editinternship/<int:internship_id>/', edit_internship, name='edit_internship'),
    
    path('deletejob/<int:job_id>/', delete_job, name='delete_job'),
    path('deleteinternship/<int:internship_id>/', delete_internship, name='delete_internship'),

    path('quiz/', quiz, name='quiz'),

    path('admin/', admin.site.urls),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files
urlpatterns += staticfiles_urlpatterns()