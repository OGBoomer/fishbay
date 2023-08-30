from functools import wraps
from django.shortcuts import redirect
import datetime
from .models import Account


def check_active_status(user):
    if user.sub_expire:
        if datetime.date.today() > user.sub_expire:
            user.status = 'IA'
            user.save()
    if user.status != 'IA':
        return True
    return False
