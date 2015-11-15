import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ppa.settings')

import django
import sys

from transaction.models import Transaction, Account, AccountCategory

django.setup()

# clear all account jumlah first
all_accounts = Account.objects.all()
for account in all_accounts:
    account.jumlah = 0
    account.save()

all_transaction = Transaction.objects.all()
for transaction in all_transaction:

    if transaction.account_debet.account_category.debet == '+':
        transaction.account_debet.jumlah += transaction.jumlah
        transaction.account_debet.save()

    elif transaction.account_debet.account_category.debet == '-':
        transaction.account_debet.jumlah -= transaction.jumlah
        transaction.account_debet.save()

    if transaction.account_kredit.account_category.kredit == '+':
        transaction.account_kredit.jumlah += transaction.jumlah
        transaction.account_kredit.save()

    elif transaction.account_kredit.account_category.kredit == '-':
        transaction.account_kredit.jumlah -= transaction.jumlah
        transaction.account_kredit.save()