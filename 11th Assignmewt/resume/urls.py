from django.urls import path
from . import views

urlpatterns = [
    path('<int:employee_id>/pdf/', views.download_pdf, name='resume_pdf'),
    path('<int:employee_id>/docx/', views.download_docx, name='resume_docx'),
]
