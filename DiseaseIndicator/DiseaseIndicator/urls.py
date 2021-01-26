"""DiseaseIndicator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name = 'index'),
    path('start', views.start , name = 'start'),
    path('Symptom', views.getSymptopm , name = 'symptom'),
    path('audioSymptom', views.audioGetSymptom , name = 'audioSymptom'),
    path('SymptomDetails', views.detSymptopm , name = 'symptomDetails'),
    path('audioSymptomDetails', views.audioDetSymptopm , name = 'symptomDetails'),
    path('getResult', views.calculate , name = 'getResult'),
    path('getResultAudio', views.audioCalculate , name = 'getResultaudio'),
    path('getCalAudio', views.audioCalculateResult , name = 'getAudioResult'),




]
