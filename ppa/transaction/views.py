from .models import Transaction
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import now
import datetime


def display_today(request):
    context = {'transactions':
    Transaction.objects.all()}
    return render(request, template_name='today.html', context=context)
