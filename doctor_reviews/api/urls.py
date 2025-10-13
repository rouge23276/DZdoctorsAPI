from django.urls import path
from .views import (doctor_list_create, doctor_detail, 
                   doctor_reviews, review_detail, create_reply)
from views import DoctorList, DoctorDetail



app_name = 'api'

urlpatterns = [
    path('doctors/', DoctorList.as_view()),
    path('doctors/<int:pk>/', DoctorDetail.as_view()),
    path('doctors/<uuid:doctor_id>/', doctor_detail, name='doctor-detail'),
    path('doctors/<uuid:doctor_id>/reviews/', doctor_reviews, name='doctor-reviews'),
    path('reviews/<uuid:review_id>/', review_detail, name='review-detail'),
    path('reviews/<uuid:review_id>/replies/', create_reply, name='create-reply'),
]
