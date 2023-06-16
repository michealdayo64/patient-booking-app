from django.urls import path
from .views import registerView, loginView, update_profile, logoutView, forgetPass, resetPass, verificationView, AdditionaInfoView

urlpatterns = [
    path('register-page/', registerView, name='register'),
    path('login-page/', loginView, name='login'),
    path('logout-page/', logoutView, name='logout'),
    path('update-profile/', update_profile, name='update-user'),
    path('forgot-pass/', forgetPass, name='forgot-pass'),
    path('reset-pass/<uidb64>/<token>', resetPass, name='reset-user-pass'),
    path('activate/<uidb64>/<token>/', verificationView, name='activate'),
    path('new-intake/', AdditionaInfoView.as_view(), name='new-intake'),

]
