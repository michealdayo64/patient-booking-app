from django.urls import path
from .views import (index, about, blog, contact, booking_page, faq, private_policy, t_and_c, services, medPsycGyn, getAppointmentTimeByDate,
                    bookingDetails, bookingSummary, getAllAppointment, paymnent, theProvider)
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', index, name='index'),
    path('about-page/', about, name='about'),
    path('the-provider/', theProvider, name='the-provider'),
    path('blog-page/', blog, name='blog'),
    path('contact-page/', contact, name='contact'),
    path('booking-page/', booking_page, name='booking'),
    path('faq-page/', faq, name='faq'),
    path('private-policy-page/', private_policy, name='private-policy'),
    path('t-and-c/', t_and_c, name='t-and-c'),
    path('services/', services, name='services'),
    path('medical-management/', medPsycGyn, name='medical-management'),
    # path('fifteen-min/', csrf_exempt(fifteenMinBook), name='fifteen-min'),
    path('booking-order/', csrf_exempt(bookingDetails), name='booking-order'),
    path('booking-order/<id>/', csrf_exempt(bookingDetails),
         name='booking-order-id'),
    path('summary/<id>/', bookingSummary, name="summary-id"),
    path('get-appointment/', getAllAppointment, name='get-appointment'),
    path('payment/<id>/', paymnent, name='payment'),
    path('get-app-by-date/', csrf_exempt(getAppointmentTimeByDate),
         name='get-app-by-date')
]
