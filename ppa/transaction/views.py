from .models import Transaction
from .models import Account
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import now
from django import http
import datetime


def display_today(request):
    if not request.user.has_perm('transaction.delete_transaction'):
        transactions = Transaction.objects.filter(date=timezone.localtime(now()).date(), owner=request.user)
    else:
        transactions = Transaction.objects.filter(date=timezone.localtime(now()).date())
    context = {
        'transactions': transactions
    }
    return render(request, template_name='today.html', context=context)


def display_not_today(request, day, month, year):

    if not request.user.has_perm('transaction.delete_transaction'):
        return http.HttpResponseForbidden('Access Denied')

    qs = Transaction.objects.filter(created__day=day,
               created__month=month,
               created__year=year)
    oneobject = list(qs[:1])
    tanggal = oneobject[0].created
    context = {'transactions': qs,
               'tanggal': tanggal}
    return render(request, template_name='not_today.html', context=context)


def display_saldodana(request):

    totalbelanja = 0
    for belanja in Account.objects.filter(account_category__name='BELANJA'):
        totalbelanja += belanja.jumlah

    totalpendapatan = 0
    for pendapatan in Account.objects.filter(account_category__name='PENDAPATAN'):
        totalpendapatan += pendapatan.jumlah

    totalasset = 0
    for aset in Account.objects.filter(account_category__name='ASET'):
        totalasset += aset.jumlah

    totalutang = 0
    for utang in Account.objects.filter(account_category__name='UTANG'):
        totalutang += utang.jumlah

    context = {'belanja': totalbelanja, 'pendapatan': totalpendapatan,
               'totalasset': totalasset, 'totalutang': totalutang}
    return render(request, template_name='saldodana.html', context=context)
