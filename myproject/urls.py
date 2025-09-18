"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', myapp, name="myapp"),
    path('login_page/', login_page, name="login_page"),
    path('signup_page1/', signup_page1, name="signup_page1"),
    path('signup_page2/', signup_page2, name="signup_page2"),
    path('signup_page3/', signup_page3, name="signup_page3"),
    path('verification/', verification, name="verification"), 
    path('profile/', profile_view, name='profile'),
    path('resend_verification/', resend_verification, name='resend_verification'),
    path('home_page/', home_page, name='home_page'),
    path('logout/', logout_view, name='logout'),
    
    path('service_selection/', service_selection, name='service_selection'),
    path('service_selection/<int:service_id>/', service_detail, name='service_detail'),
    path('service_selection/<int:service_id>/join/', join_queue, name='join_queue'),
    path('service_selection/<int:service_id>/leave/', leave_queue, name='leave_queue'),
]
