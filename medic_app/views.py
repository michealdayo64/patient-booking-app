from datetime import datetime
from django.shortcuts import render, redirect
from .models import Ailments, Appointment, Payment
from auths.models import Account, AdditionalInformation
from django.http import JsonResponse
import json
from django.contrib import messages
from .forms import WriteUsForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from reviews.models import Review

# Create your views here.


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def index(request):
    ailment_list = Ailments.objects.all()
    review_list = Review.objects.all()[:6]
    if request.method == "POST":
        form = WriteUsForm(request.POST or None)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "Form Submitted Successfully")
            return redirect('index')
        else:
            WriteUsForm()
            messages.success(request, "You need to fill the form")
            return redirect('index')
    context = {
        "ailment_list": ailment_list,
        "review_list": review_list
    }
    return render(request, 'index.html', context)


def booking_page(request):
    context = {}
    ailment_list = Ailments.objects.all()
    context["ailment_list"] = ailment_list

    return render(request, 'view/schedule.html', context)


'''def fifteenMinBook(request):
    data = {}
    if request.user.is_authenticated:
        user_id = request.user.id
        user = Account.objects.get(id=user_id)
        if request.method == "POST":
            user.fifteen_min_trial = True
            user.save()
            data["response"] = "15min free trial Selected"
            return JsonResponse(data=data)
    else:
        data["response"] = "User not authenticated"
        return JsonResponse(json.dumps(data), safe=False)'''


def bookingDetails(request, id=None):
    payload = {}
    ns = json.loads(request.body)

    if request.method == "POST":
        date = ns["date"]
        date_format = datetime.strptime(date, '%d/%m/%Y')
        time = ns["time"]
        email = ns['email']
        phone_no = ns["phone"]
        message = ns["message"]

        addInfo = AdditionalInformation.objects.get(email=email)
        print(addInfo)

        if id:
            ailment_id = Ailments.objects.get(id=id)
            app_id = Appointment.objects.create(add_info=addInfo, ailment_id=ailment_id, phone_no=phone_no,
                                                message=message, date=date_format, appointment_time=time, is_booked=False)
            payload["response"] = "Appointment Order"
            payload['app_id'] = app_id.id
            payload['firstname'] = app_id.add_info.firstname
            payload['lastname'] = app_id.add_info.lastname
            payload['service'] = app_id.ailment_id.title
            payload['date_and_time'] = f'{app_id.date}, {app_id.appointment_time}'
            return JsonResponse((payload), safe=False)
        else:
            app_id = Appointment.objects.create(
                add_info=addInfo, phone_no=phone_no, message=message, date=date_format, appointment_time=time, is_booked=False)
            payload["response"] = "Appointment Order"
            payload['app_id'] = app_id.id
            payload['firstname'] = app_id.add_info.firstname
            payload['lastname'] = app_id.add_info.lastname
            payload['service'] = "15min Consultation"
            payload['date_and_time'] = f'{app_id.date}, {app_id.appointment_time}'
            return JsonResponse((payload), safe=False)


def bookingSummary(request, id):
    payload = {}

    print(id)
    appointment = Appointment.objects.get(id=id)
    print(appointment.date, appointment.appointment_time)
    payload = {
        "firstname": appointment.user.first_name,
        "lastname": appointment.user.last_name,
        "service": appointment.ailment_id.title,
        "date_and_time": f'{appointment.date}, {appointment.appointment_time}'
    }
    return JsonResponse(data=payload, safe=False)


def newPatientIntakeForm(request):
    pass


def getAllAppointment(request):
    payload = {}
    data = []
    app = Appointment.objects.all()
    for i in app:
        data.append({
            'date': i.date,
            'time': i.appointment_time
        })
    payload['result'] = data
    return JsonResponse(payload, safe=False)


def getAppointmentTimeByDate(request):
    # date = request.POST.get
    payload = {}
    ns = json.loads(request.body)
    date = ns['date']
    data = []
    # strdate = datetime.strptime(date, '%d-%m-%Y')
    app = Appointment.objects.filter(date=date)
    print(app)
    for i in app:
        data.append({
            'date': i.date,
            'time': i.appointment_time
        })
    payload['result'] = data
    return JsonResponse((payload), safe=False)


def faq(request):
    if request.method == "POST":
        form = WriteUsForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, "Form Submitted Successfully")
            return redirect('faq')
        else:
            WriteUsForm()
            messages.success(request, "You need to fill the form")
            return redirect('faq')
    return render(request, 'view/faq.html')


@login_required
def paymnent(request, id):
    user = request.user
    if request.method == "POST":
        upload_pay = request.FILES.get('upload_pay')
        app_id = Appointment.objects.get(id=id)
        app_id.is_booked = True
        app_id.save()
        if app_id.ailment_id != None:
            Payment.objects.create(user=user, app_id=app_id,
                                   is_payed=True, payment_prove=upload_pay)
            subject = "Appointment Booking"
            message = f"Dear, {user.first_name}, {user.last_name}, You have just booked an appointment Successfully for the treatment of {app_id.ailment_id.title}"
            mail_from = settings.EMAIL_HOST_USER
            mail_to = [user.email, 'omotoshomicheal93@gmail.com']
            email = EmailMessage(subject, message, mail_from, mail_to)
            EmailThread(email).start()
            messages.success(request, 'You have payed Successful')
            return redirect('index')
        else:
            Payment.objects.create(user=user, app_id=app_id,
                                   is_payed=True, payment_prove=upload_pay)
            subject = "Appointment Booking"
            message = f"Dear, {user.first_name}, {user.last_name}, You have just booked an appointment Successfully for the treatment for free 15 Min Service"
            mail_from = settings.EMAIL_HOST_USER
            mail_to = [user.email, 'omotoshomicheal93@gmail.com']
            email = EmailMessage(subject, message, mail_from, mail_to)
            EmailThread(email).start()
            messages.success(request, 'You have payed Successful')
            return redirect('index')
    # print(app_id)
    return render(request, 'view/payment.html')


def theProvider(request):
    return render(request, 'view/the_provider.html')


def services(request):
    return render(request, 'view/services.html')


def medPsycGyn(request):
    ailment_list = Ailments.objects.all()
    return render(request, 'view/med_psy_gyn.html', {'ailment_list': ailment_list})


def blog(request):
    return render(request, 'view/blog.html')


def about(request):
    return render(request, 'view/about.html')


def contact(request):
    return render(request, 'view/contact.html')


def private_policy(request):
    return render(request, 'view/private_policy.html')


def t_and_c(request):
    return render(request, 'view/t_and_c.html')
