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
from .models import AccountPayment

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
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': settings.PRODUCT_PRICE,
                    'quantity': 1
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)
    return render(request, 'account/subscription_page.html')


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user.user_id
    user_payment = AccountPayment.objects.get(api_user=user_id)
    user_payment.stripe.checkout_id = checkout_session_id
    user_payment.save()
    return render(request, 'account/payment_successful.html', {'customer': customer})


def payment_cancelled(request):
    return render(request, 'account/payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
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
        time.sleep(15)
        account_payment = AccountPayment.objects.get(stripe_checkout_id=session_id)
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        account_payment.payment_bool = True
        account_payment.save()
    return HttpResponse(status=200)
