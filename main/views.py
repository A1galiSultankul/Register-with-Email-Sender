from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from . tokens import generate_token

from .models import SmartPhone# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from djangoProject import settings


def index(request):
    obj = SmartPhone.objects.all()
    context = {
        "obj": obj,
    }

    return render(request, 'main/index.html', context)


def about(request):
    obj = SmartPhone.objects.all()
    context = {
        "obj": obj,
    }
    return render(request, 'main/about.html',context)


def register(request):
    if request.method == 'POST':
        #username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if User.objects.filter(username=username):
            messages.error(request, 'Username already exist! Please try another username.')
            return redirect('Home')

        if not pass1 or not pass2:
            messages.error(request, "Password cannot be empty")
            return redirect('Home')
        if len(username) > 10:
            messages.error(request, 'Username must be under 10 characters.')
        if pass1 != pass2:
            messages.error(request, "Password didn't match")
            return redirect('Home')
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric characters")
            return redirect('Home')
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        messages.success(request, 'Your account has been successfully created! We have sent you a confirmation email, please confirm your email in order to activate your account.')

        #Welcome Email

        subject = 'Welcome to SmartShop'
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to SmartShop \nThank you for visiting our online technical shop \n We have also sent you confirmation Email, please confirm your email addres in order to activate your account \n Thank You!!! \n Much love from Aigali"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        #Email Addres Confirmation Email

        current_site = get_current_site(request)
        email_subject = 'Activate your SmartShop account!\n '
        message2 = render_to_string("main/email_confirmation.html", {
            "name": myuser.first_name,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
            "token": generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True

        email.send()


        return redirect('login')
    return render(request, 'main/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        auth_login(request, myuser)  # Use auth_login instead of login
        messages.success(request, 'Your account has been activated!')
        return redirect('login')
    else:
        return render(request, 'main/activation_failed.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            auth_login(request, user)
            fname = user.first_name
            return render(request, 'main/index.html', {"fname": fname})
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('Home')
    return render(request, 'main/login.html')


def logout(request):
    auth_logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('Home')










