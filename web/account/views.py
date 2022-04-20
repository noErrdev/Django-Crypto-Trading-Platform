from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, UpdateView
from exchange.common_functions import search

from .forms import LoginForm, ProfileForm, SignupForm
from .models import User
from .tokens import account_activation_token


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy("account:profile")

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)


@login_required
def wallet(request):
    return render(request, "registration/wallet.html")


@login_required
def tradeHistory(request):
    return render(request, "registration/tradeHistory.html")


def trade(request, pair="BINANCE:BTCUSDT"):

    if pair != "BINANCE:BTCUSDT":
        name = pair.split("-")[0]
        pair = search(pair)
    else:
        name = "BTC"

    context = {"pair": pair, "name": name.upper()}

    if not pair:
        pair = "BINANCE:BTCUSDT"
        name = "BTC"

        context = {
            "pair": pair,
            "name": name.upper(),
        }
        return redirect("/account/trade/BTC-USDT")
    else:
        return render(request, "registration/trade.html", context=context)


class Login(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True


class Register(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("exchange:home")
        return super(Register, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = "Activate your Trading-Platform account."
        message = render_to_string(
            "registration/activate_account.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        to_email = form.cleaned_data.get("email")
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        context = {
            "title": "Signup",
            "redirect": "exchange:home",
            "message": "Please confirm your email address to complete the registration.",
        }
        return render(self.request, "registration/messages.html", context=context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        context = {
            "title": "Signup",
            "redirect": "login",
            "message": "Your account has been successfully activated now you can login.",
        }
        return render(request, "registration/messages.html", context=context)
    else:
        context = {
            "title": "Signup",
            "redirect": "signUp",
            "message": "This link has been expired.",
        }
        return render(request, "registration/messages.html", context=context)
