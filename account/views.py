from django.shortcuts import render, redirect
from .forms import AccountCreationForm, SubscriptionForm
# from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import stripe
import datetime
import time
import json
from .models import Account, StripePayment

# from django.contrib.auth import get_user_model


# User = get_user_model()


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('account:homepage')
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('account:profile')
        else:
            messages.error(request, 'Login Failed')
    return render(request, 'account/login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('account:homepage')
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = request.POST.get('email')
            password = request.POST.get('password1')
            user = authenticate(request, email=email, password=password)
            login(request, user)
            return render(request, 'account/profile.html')
    else:
        form = AccountCreationForm()
    return render(request, 'account/register.html', {'form': form})


def logoutpage(request):
    logout(request)
    return redirect('account:loginpage')


@login_required()
def profile(request):
    return render(request, 'account/profile.html')


def homepage(request):
    return render(request, 'account/home.html')


def howto(request):
    return render(request, 'account/howto.html')


def subscription_page(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            customer_id = request.user.stripe_cus_id
            customer_email = None
            if not customer_id:
                customer_id = None
                customer_email = request.user.email
            term = request.POST['sub_term']
            match term:
                case 'beta':
                    request.user.status = 'BT'
                    request.user.sub_start = datetime.datetime.now()
                    request.user.save()
                    return redirect('/account/profile/')
                case 'month':
                    PRICE = settings.MONTHLY_PRICE
                case 'semi':
                    PRICE = settings.SEMI_PRICE
                case 'year':
                    PRICE = settings.ANNUAL_PRICE
                case _:
                    pass
            checkout_session = stripe.checkout.Session.create(
                customer=customer_id,
                customer_email=customer_email,
                line_items=[
                    {
                        'price': PRICE,
                        'quantity': 1
                    },
                ],
                mode='subscription',
                # subscription_data={
                #     'trial_period_days': 7
                # },
                success_url=settings.REDIRECT_DOMAIN + '/account/payment_successful?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.REDIRECT_DOMAIN + '/account/payment_cancelled',
            )
        # return redirect(checkout_session.url, code=303)
    else:
        form = SubscriptionForm()
    return render(request, 'account/subscription_page.html', {'form': form})


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    if checkout_session_id:
        session = stripe.checkout.Session.retrieve(checkout_session_id)
        customer = stripe.Customer.retrieve(session.customer)
        request.user.stripe_cus_id = customer.id
        request.user.save()
    return render(request, 'account/profile')


@login_required
def go_stripe_portal(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    session = stripe.billing_portal.Session.create(
        customer=request.user.stripe_cus_id,
        return_url='http://www.myfishbay.com/account/profile',
    )
    return redirect(session.url)


def payment_cancelled(request):
    return render(request, 'account/payment_cancelled.html')


@csrf_exempt
def webhook_test(request):
    print(request.body)
    return HttpResponse(status=200)


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    payload = request.body
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        print("Webhook error while parsing basic request." + str(e))
        return HttpResponse({"success": True}, status=400)
    except stripe.error.SignatureVerificationError as e:
        print("Webhook Stripe verificationError." + str(e))
        return HttpResponse({"success": True}, status=400)
    if event.type == 'customer.subscription.updated':
        subscription = event.data.object
        customer = stripe.Customer.retrieve(subscription.customer)
        user = Account.objects.get(email=customer.email)
        user.stripe_sub_id = subscription.id
        user.sub_start = datetime.date.fromtimestamp(subscription.current_period_start)
        user.sub_expire = datetime.date.fromtimestamp(subscription.current_period_end)
        user.status = 'AT'
        user.sub_auto_renew = not subscription.cancel_at_period_end
        user.save()
        #stripe_payment = StripePayment.objects.get(stripe_checkout_id=session_id)
        #line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        #stripe_payment.payment_bool = True
        # stripe_payment.save()
    if event.type == 'customer.subscription.deleted':
        subscription = event.data.object
        user = Account.objects.get(stripe_sub_id=subscription.id)
        user.sub_auto_renew = False
        user.save()
    return HttpResponse(status=200)
