from .models import Transaction
from django.shortcuts import render


def display_today(request):
    context = {'transactions': Transaction.objects.all()}
    return render(request, template_name='today.html', context=context)
