from .models import Transaction
from .models import Account
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import now
from django import http
import datetime


def display_today(request):
    
    context = {'transactions':
    Transaction.objects.filter(created=timezone.localtime(now()).date())}
    return render(request, template_name='today.html', context=context)


def display_not_today(request, day, month, year):

    if not request.user.has_perm('transaction.delete_transaction'):
        return http.HttpResponseForbidden('Access Denied')

    context = {'transactions':
    Transaction.objects.filter(created__day=day,
               created__month=month,
               created__year=year)}
    return render(request, template_name='today.html', context=context)
