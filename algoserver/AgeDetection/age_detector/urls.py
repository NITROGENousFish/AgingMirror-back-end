from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

app_name = 'age_detector'
urlpatterns = [
    path('detect/', views.detect),
    path('show/', views.detect)
]
urlpatterns += staticfiles_urlpatterns()
