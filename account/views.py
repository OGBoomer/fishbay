from django.shortcuts import render, redirect
from .forms import AccountCreationForm
# from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import stripe
import datetime
import time
import json
from .models import StripePayment

# from django.contrib.auth import get_user_model


# User = get_user_model()


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('account:homepage')
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = authenticate(request, email=email, password=password)
        print('in login')
        if user is not None:
            print('user not none')
            login(request, user)
            return redirect('account:homepage')
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
            return render(request, 'account/login.html')
        else:
            print("not valid")
    else:
        form = AccountCreationForm()
    return render(request, 'account/register.html', {'form': form})


def logoutpage(request):
    logout(request)
    return redirect('account:loginpage')


def homepage(request):
    return render(request, 'account/home.html')


def subscription_page(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    if request.method == 'POST':
        account_profile, created = AccountProfile.objects.get_or_create(user=request.user)
        customer_id = account_profile.stripe_cus_id
        customer_email = None
        if not customer_id:
            customer_id = None
            customer_email = request.user.email
        checkout_session = stripe.checkout.Session.create(
            customer=customer_id,
            customer_email=customer_email,
            line_items=[
                {
                    'price': settings.PRODUCT_PRICE,
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
        return redirect(checkout_session.url, code=303)
    return render(request, 'account/subscription_page.html')


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
        StripePayment.objects.create(user=request.user, stripe_checkout_id=checkout_session_id)
    return render(request, 'account/payment_successful.html', {'customer': customer})


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
        print("in sub")
        subscription = event.data.object
        print(subscription)
        customer = stripe.Customer.retrieve(subscription.customer)
        user = Account.objects.get(email=customer.email)
        print(f'sub is {subscription.id}')
        user.stripe_sub_id = subscription.id
        user.sub_start = datetime.date.fromtimestamp(subscription.current_period_start)
        user.sub_expire = datetime.date.fromtimestamp(subscription.current_period_end)
        user.status = 'BT'
        user.save()
        #stripe_payment = StripePayment.objects.get(stripe_checkout_id=session_id)
        #line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        #stripe_payment.payment_bool = True
        # stripe_payment.save()
        else:
            print(subscription.customer)
    else:
        print(event.type)
        print('no sub')
    return HttpResponse(status=200)
