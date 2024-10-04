from django.contrib import admin
from django.urls import path
from home.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name='home'),

    path('job/', job, name='job'),
    path('internship/', internship, name='internship'),
    path("contest/", contest, name='contest'),
    path("news/", news, name='news'),

    path("login/", login_page, name='login'),
    path("logout/", logout_page, name='logout'),
    path("signup/", signup, name='signup'),

    path('student/', student, name='student_dashboard'),  # Student dashboard
    path('company/', company, name='company_dashboard'),  # Company dashboard

    path("contact/", contact, name='contact'),

    path('admin/', admin.site.urls),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files
urlpatterns += staticfiles_urlpatterns()
