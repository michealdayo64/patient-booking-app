from django.shortcuts import render, redirect
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, AdditionalInformationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Account, AdditionalInformation
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import account_activation_token
import threading
# import validate_email
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.generic import View


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


# Create your views here.

# REGISTER VIEW
def registerView(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={
                           'uidb64': uidb64, 'token': account_activation_token.make_token(user)})
            activate_url = f'http://{domain}{link}'
            subject = 'Activate your account'
            message = f"Hi, {user.username} thank you registering with Amitopcare LLC. Kindly use the link below to verify your account\n {activate_url}"
            mail_from = settings.EMAIL_HOST_USER
            mail_to = [user.email]
            email = EmailMessage(subject, message, mail_from, mail_to)
            EmailThread(email).start()
            # email.send(fail_silently=False)
            # send_mail(subject, message, mail_from, mail_to, fail_silently=False)
            messages.success(
                request, "Registered Successfully. Kindly check your email to verify your account")
            return redirect('register')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'auth/register.html', context)


def verificationView(request, uidb64, token):
    try:
        id = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=id)

        if not account_activation_token.check_token(user, token):
            return redirect('login'+'?message'+'User already activated')
        if user.is_active:
            return redirect('login')
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated successfully')
        return redirect('login')
    except Exception as ex:
        pass
    return redirect("login")


# LOGIN VIEW
def loginView(request, *args, **kwargs):
    context = {}
    user = request.user
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)

                destination = get_redirect_if_exist(request)
                if destination:
                    return redirect(destination)
                if user.profile_updated:
                    messages.info(request, f"Login Successfully")
                    return redirect("index")
                elif not user.is_active:
                    messages.info(request, f"You have not verify your account")
                    return redirect('login')
                else:
                    messages.info(request, f"You have to update your profile")
                    return redirect('update-user')
        else:
            context['login_form'] = form
    else:
        form = AccountAuthenticationForm()
        context['login_form'] = form
    return render(request, 'auth/login.html', context)


def get_redirect_if_exist(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get('next'))
    return redirect

# LOGOUT VIEW


def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("login")
    else:
        print("your not login")


def update_profile(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    if request.POST:
        form = AccountUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            upd = form.save()
            print(upd)
            upd.profile_updated = True
            upd.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("index")
    else:
        form = AccountUpdateForm()
        context['form'] = form
    return render(request, 'auth/update_profile.html', context)


def forgetPass(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get('email')
        print(email)

        context = {
            'values': request.POST
        }
        '''if not validate_email(email):
            messages.info(request, 'Please supply a valid email')
            return render(request, "auth/forgot_pass.html")'''

        current_site = get_current_site(request)
        user = Account.objects.filter(email=email)
        print(user.exists())
        if user.exists():
            email_content = {
                'user': user[0],
                'doamin': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            }

            link = reverse('reset-user-pass', kwargs={
                'uidb64': email_content['uid'], 'token': email_content['token']
            })

            email_subject = "Password reset Instructions"
            reset_url = f'http://{current_site.domain}{link}'

            message = f"Hi {user[0].username}, Kindly click the link below to reset your password\n {reset_url}"
            mail_from = settings.EMAIL_HOST_USER
            mail_to = [email]
            email = EmailMessage(email_subject, message, mail_from, mail_to)
            EmailThread(email).start()

            messages.success(
                request, "We have sent you an email to reset your password")
            redirect('login')
        else:
            messages.success(
                request, "Account not valid, Kindly provide a valid account")
            redirect('forgot-pass')

    return render(request, "auth/forgot_pass.html", context)


def resetPass(request, uidb64, token):
    if request.method == "POST":
        password1 = request.POST.get('password1')
        print(password1)
        password2 = request.POST.get('password2')
        (password2)
        if password1 != password2:
            messages.info(request, "Password deos not match")
            return render(request, "auth/reset_pass.html")
        if len(password1) < 6:
            messages.info(request, "Password too short")
            return render(request, "auth/reset_pass.html")

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=user_id)
            user.set_password(password1)
            user.save()
            if PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request, 'Password link invalid, Pls request for a new one')
                return redirect('forgot-pass')
            messages.info(request, "Password was set successfully")
            return redirect('login')
        except Exception as identifier:
            messages.info(request, 'something went wrong')
            return render(request, "auth/reset_pass.html")
    else:
        print("Enter something")
    return render(request, "auth/reset_pass.html")


class AdditionaInfoView(View):
    def get(self, *args, **kwargs):
        try:

            form = AdditionalInformationForm()

            context = {
                'form': form
            }

        except Exception:
            print("Nothing")
        return render(self.request, 'auth/new_intake.html', context)

    def post(self, *args, **kwargs):

        if self.request.method == 'POST':
            form = AdditionalInformationForm(self.request.POST or None)
            print(form.is_valid())
            if form.is_valid():
                firstname = form.cleaned_data.get('firstname')
                lastname = form.cleaned_data.get('lastname')
                email = form.cleaned_data.get('email')
                phone_number = form.cleaned_data.get('phone_number')
                dob = form.cleaned_data.get('dob')
                gender = form.cleaned_data.get('gender')
                city = form.cleaned_data.get('city')
                state = form.cleaned_data.get('state')
                zipCode = form.cleaned_data.get('zipCode')
                best_way_reach = form.cleaned_data.get('best_way_reach')
                best_time_reach = form.cleaned_data.get('best_time_reach')
                insurance_or_pay = form.cleaned_data.get(
                    'insurance_or_pay')
                my_insure_carrier = form.cleaned_data.get(
                    'my_insure_carrier')
                insurance = form.cleaned_data.get('insurance')
                do_you_have_secondary_insurance = form.cleaned_data.get(
                    'do_you_have_secondary_insurance')
                secondary_insurance_carrier = form.cleaned_data.get(
                    'secondary_insurance_carrier')
                secondary_insurance = form.cleaned_data.get(
                    'secondary_insurance')
                current_psychiatric_diagnosis = form.cleaned_data.get(
                    'current_psychiatric_diagnosis')
                current_medications = form.cleaned_data.get(
                    'current_medications')
                current_psychiatric_prescriber = form.cleaned_data.get(
                    'current_psychiatric_prescriber')
                history_of_suicide_attempts = form.cleaned_data.get(
                    'history_of_suicide_attempts')
                history_of_eating_disorder = form.cleaned_data.get(
                    'history_of_eating_disorder')
                history_of_substance_abuse = form.cleaned_data.get(
                    'history_of_substance_abuse')
                emergency_contact_firstname = form.cleaned_data.get(
                    'emergency_contact_firstname')
                emergency_contact_phone = form.cleaned_data.get(
                    'emergency_contact_phone')
                referred_by = form.cleaned_data.get('referred_by')
                additional_comments = form.cleaned_data.get(
                    'additional_comments')
                # print(current_psychiatric_prescriber)

                AdditionalInformation.objects.create(
                    firstname=firstname,
                    lastname=lastname,
                    email=email,
                    phone_number=phone_number,
                    dob=dob,
                    gender=gender,
                    city=city,
                    state=state,
                    zipCode=zipCode,
                    best_time_reach=best_time_reach,
                    best_way_reach=best_way_reach,
                    insurance_or_pay=insurance_or_pay,
                    my_insure_carrier=my_insure_carrier,
                    insurance=insurance,
                    do_you_have_secondary_insurance=do_you_have_secondary_insurance,
                    secondary_insurance_carrier=secondary_insurance_carrier,
                    secondary_insurance=secondary_insurance,
                    current_psychiatric_diagnosis=current_psychiatric_diagnosis,
                    current_psychiatric_prescriber=current_psychiatric_prescriber,
                    current_medications=current_medications,
                    history_of_suicide_attempts=history_of_suicide_attempts,
                    history_of_eating_disorder=history_of_eating_disorder,
                    history_of_substance_abuse=history_of_substance_abuse,
                    emergency_contact_firstname=emergency_contact_firstname,
                    emergency_contact_phone=emergency_contact_phone,
                    referred_by=referred_by,
                    additional_comments=additional_comments
                )
                # addInfo.save()

                subject = 'New Intake Patient'
                message = f"""
                Hello, {firstname} {lastname} Just book an Appintment with Amitop Care LCC\n\n.
                Email sent from: {email} \n
                Phone number: {phone_number}\n
                Payment: {insurance_or_pay}\n
                Best way to reach them: {best_way_reach}\n
                Best Time to Reach them: {best_time_reach}

                
                """
                mail_from = settings.EMAIL_HOST_USER
                mail_to = [email, 'amitopcarellc@gmail.com']
                setemail = EmailMessage(subject, message, mail_from, mail_to)
                EmailThread(setemail).start()

                messages.success(
                    self.request, "Form Submitted Successfully. We will get back to you in 10 Minutes")
                return redirect('index')
            else:
                print(form.errors.as_data())
                form = AdditionalInformationForm()

        return render(self.request, 'auth/new_intake.html')
