from django.shortcuts import render, redirect
from .admin import UserCreationForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
import time
from .models import AccountProfile, StripePayment

# from django.contrib.auth import get_user_model


# User = get_user_model()


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('account:homepage')
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
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
        form = UserCreationForm(request.POST)
        print("before valid")
        if form.is_valid():
            print('before save')
            form.save()
            return render(request, 'account/login.html')
        else:
            print("not valid")
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})


def logoutpage(request):
    print('before')
    logout(request)
    print("after")
    return redirect('account:loginpage')


def homepage(request):
    return render(request, 'account/home.html')


def subscription_page(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    if request.method == 'POST':
        account_profile = AccountProfile.objects.get(user=request.user)
        if account_profile.stripe_cus_id:
            customer_id = account_profile.stripe_cus_id
        else:
            customer_id = None
        checkout_session = stripe.checkout.Session.create(
            customer = customer_id,
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


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    if checkout_session_id:
        session = stripe.checkout.Session.retrieve(checkout_session_id)
        customer = stripe.Customer.retrieve(session.customer)
        account_profile = AccountProfile.objects.get(user=request.user)
        account_profile.stripe_cus_id = customer.id
        account_profile.save()
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
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print(f'payload is {payload}')
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST

        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.complete':
        session = event['data']['object']
        session_id = session.get('id', None)
        print(f'wh id is {{ session_id }}')
        # time.sleep(15)
        # account_payment = AccountPayment.objects.get(stripe_checkout_id=session_id)
        # line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        # account_payment.payment_bool = True
        # account_payment.save()
    return HttpResponse(status=200)
