from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from killer import settings
from django.core.mail import send_mail


# Create your views here.
def home(request):

    return render(request, "shooter/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

       # Validations

        if User.objects.filter(username=username):
            messages.error(request,"username already exist! Please try some other username")
            return redirect('home')

        if User.objects.filter(email=email):
            mesages.error(request, "Email already registered")
            return redirect(home)

        if len(username)>10:
            message.error(request,"username must be under 10 characters")

        if password != password2:
            message.error(request,"passwords didn't match!")

        if not username.isalnum():
            message.error(request,"usernmae must be Alpha-Numeric")
            return redirect("home")

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                        last_name=last_name)
        user.save()

        messages.success(request, "your account has been successfully created")

        # Welcome Email
        subject = "Welcome to gang!!"
        message= "Hello" + user.first_name + "!! \n" + "Welcome to our Gang \n"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')

    return render(request, "shooter/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            messages.success(request, 'You are successfully logged in ')
            return redirect('home')

        else:
            messages.error(request, "Bad credentials")
            return redirect('signin')

    else:
        return render(request, "shooter/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "you are successfully logged out")
    return redirect('home')

