from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):

    """
    Abstract model class that provides
    self-updating 'created' and 'modified'
    fields.
    """

    created = models.DateField(default=timezone.now())
    modified = models.DateField(default=timezone.now())

    class Meta:
        abstract = True


class AccountCategory(TimeStampedModel):
    name = models.CharField(max_length=50, verbose_name='nama')
    CHOICES = (
        ('+', '+'),
        ('-', '-'),
        (' ', ' '),
    )
    debet = models.CharField(max_length=5, choices=CHOICES)
    kredit = models.CharField(max_length=5, choices=CHOICES)

    class Meta:
        verbose_name_plural = 'Account Categories'

    def __str__(self):
        return self.name


class Account(TimeStampedModel):
    owner = models.ForeignKey(User, related_name='accounts')
    name = models.CharField(max_length=50, verbose_name='nama')
    account_category = models.ForeignKey(AccountCategory, blank=True,
                                         null=True)
    code = models.CharField(max_length=10, verbose_name='kode', unique=True)
    jumlah = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']

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

    def save(self, *args, **kwargs):
        super(Transaction, self).save(*args, **kwargs)

        if self.account_debet.account_category.debet == '+':
            self.account_debet.jumlah += self.jumlah
            self.account_debet.save()

        elif self.account_debet.account_category.debet == '-':
            self.account_debet.jumlah -= self.jumlah
            self.account_debet.save()

        if self.account_kredit.account_category.kredit == '+':
            self.account_kredit.jumlah += self.jumlah
            self.account_kredit.save()

        elif self.account_kredit.account_category.kredit == '-':
            self.account_kredit.jumlah -= self.jumlah
            self.account_kredit.save()

    def __str__(self):
        return self.name