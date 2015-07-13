from django.contrib.auth.models import User
from django.db import models

class TimeStampedModel(models.Model):

    """
    Abstract model class that provides
    self-updating 'created' and 'modified'
    fields.
    """

    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class Account(TimeStampedModel):
    owner = models.ForeignKey(User, related_name='accounts')
    name = models.CharField(max_length=50, verbose_name='nama')
    code = models.CharField(max_length=10, verbose_name='kode', unique=True)

    def __str__(self):
        return self.name

class Transaction(TimeStampedModel):
    owner = models.ForeignKey(User, related_name='transactions',
                              help_text='owner is logged in user and will be'+
                              ' automatically created')
    name = models.CharField(max_length=100, verbose_name='nama')
    keterangan = models.CharField(max_length=100, blank=True)
    account_debet = models.ForeignKey(Account, related_name='trasaksi_debet')
    account_kredit = models.ForeignKey(Account,
                                       related_name='transaksi_kredit')
    jumlah = models.IntegerField()
    def __str__(self):
        return self.name