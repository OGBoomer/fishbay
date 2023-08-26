import functools
from django.shortcuts import redirect
import datetime
from .models import Account

def active_status_required(view_func, redirect_url='account:profile'):
    '''
        custom decorector to check user.sub_auto_renew if false then compare user.sub_expire
        to today's date. If today is after expire then set status to IA(inactive). Then
        check user.status if inactive then redirect accordingly.
    '''

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = Account.objects.get(email=request.user.email)
        if datetime.date.today() > request.user.sub_expire:
            user.status = 'IA'
            user.save()
        if user.status != 'IA':
            return view_func(request, *args, *kwargs)
        return redirect(redirect_url)
    return wrapper