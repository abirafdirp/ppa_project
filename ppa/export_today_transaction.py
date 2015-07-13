import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ppa.settings')

import django
django.setup()

from django.utils import timezone
from django.utils.timezone import now
from transaction.admin import ExportData
from transaction.models import Transaction

queryset = Transaction.objects.filter(created=timezone.localtime(now()).date())
data = ExportData().export(queryset)
with open('output-%s.xlsx' %(timezone.localtime(now()).date()), 'wb') as f:
    f.write(data.xlsx)

