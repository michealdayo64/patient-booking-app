from django.urls import path
from .views import postReview


urlpatterns = [
    path('patient-review/', postReview, name = 'review')
]