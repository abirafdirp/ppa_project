import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ppa.settings')

import sys
import django
django.setup()

from transaction.models import Transaction

for transaction in Transaction.objects.all():
    transaction.date = transaction.created
    transaction.save()
