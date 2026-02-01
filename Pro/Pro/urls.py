"""
URL configuration for Pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
# Pro/Pro/urls.py
from django.contrib import admin
from django.urls import path
from api.views import UploadCSV, Summary, summary_dashboard, history_view, generate_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', UploadCSV.as_view()),
    path('summary/', Summary.as_view()),
     path('dashboard/', summary_dashboard),
     path('history/', history_view),
     path("generate-pdf/", generate_pdf),

]


