from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from killer import settings
import constants
from django.core.mail import send_mail,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_tokens
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from killer.settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model
from django.views import View








# Create your views here.
class home(View):
    def get(self,request):

        return render(request, "shooter/index.html")


# sign up page

class signup(View):
    def get(self, request):
        return render(request, 'shooter/signup.html')

    def post(self, request):
        if request.method == "POST":
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

           # Validations

            if User.objects.filter(username=username):
                messages.error(request, constants.ERROR['username']['already_taken'])
                return redirect('home')

            if User.objects.filter(email=email):
                messages.error(request, constants.ERROR['email']['already_exists'])
                return redirect('home')

            if len(username)>10:
                messages.error(request,"username must be under 10 characters")
                return redirect('home')

            if password != password2:
                messages.error(request,"passwords didn't match!")
                return redirect('home')

            if not username.isalnum():
                messages.error(request,"usernmae must be Alpha-Numeric")
                return redirect("home")

            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                            last_name=last_name)
            user.is_active= False
            user.save()

            messages.success(request, "your account has been successfully created. We had send you a confirmation mail, Please confirm your email in order to activate your account")

            # Welcome Email
            subject = "welcome to gang"
            message = "hello" + user.first_name + "!!\n" + "Welcome to gang\n"
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            #Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = "want to make a career in underworld"
            messages2 = render_to_string('email_confirmation.html',{
                'name' : user,
                'domain': current_site.domain,
                'uid' :user.pk,
                'token' : generate_tokens.make_token(user),

            })
            email = EmailMessage(
                email_subject,
                messages2,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = True
            email.send()



            return redirect('signin')

        return render(request, "shooter/signup.html")



#for activating account
class activate(View):
    def get(self,request, token, uid):

        try:

            uid = uid
            user = User.objects.get(pk=uid)


        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user=None

        if user is not None:

            if token == token:
                user.is_active = True
                user.save()

                messages.success(request, "Your Account has been activated!!")
                return redirect('signin')
        else:
            return render(request, 'activation_failed.html')

        # if user is not None and generate_token.check_token(user, token):
        #     user.is_active=True
        #     user.save()
        #     messages.add_message(request,messages.INFO,'account is activated')
        #     return redirect('signin')
        # return render(request,'activation_failed.html')


#for signing

class signin(View):
    def get(self, request):
        return render(request, "shooter/signin.html")

    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                messages.success(request, constants.ERROR['login_successfully']['login'])
                return redirect('home')

            else:
                messages.error(request, constants.ERROR['credentials']['Invalid credentials'])
                return redirect('signin')

        else:
            return render(request, "shooter/signin.html")



def signout(request):
    logout(request)
    messages.success(request, constants.ERROR['logout']['logout'])
    return redirect('home')

