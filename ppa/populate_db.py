import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ppa.settings')

import sys
import django
django.setup()

from django.contrib.auth.models import User
from transaction.models import Transaction
from transaction.models import Account

def populate():

    # get user for auth, username is from command line argument
    username = str(sys.argv[1])
    try:
        owner = User.objects.get(username=username)
    except:
        print 'invalid username or password'
        return

    # clear current database
    Account.objects.all().delete()
    Transaction.objects.all().delete()
    print 'current database cleared'

    a = add_account(owner=owner, name='gaji', code='1.1.1')
    b = add_account(owner=owner, name='tabungan', code='1.1.2')
    c = add_account(owner=owner, name='kas', code='1.1.3')
    d = add_account(owner=owner, name='pinjaman', code='1.1.4')
    add_transaction(owner=owner, name='gaji', account_debet=a,
                    account_kredit=b, jumlah=1000000)






def add_account(owner, name, code):

    # prevent field constraint code unique
    try:
        account, created = Account.objects.get_or_create(owner=owner,
                                                         name=name, code=code)
        return account
    except:
        print 'code harus unik'
        return

def add_transaction(name, owner, account_debet, account_kredit, jumlah):
    try:
        account_debet = Account.objects.get(code=account_debet.code)
    except:
        print 'Account debet %s does not exist. Please create it first' \
              %(account_debet)
        return

    try:
        account_kredit = Account.objects.get(code=account_kredit.code)
    except:
        print 'Account kredit %s does not exist. Please create it first' \
              %(account_kredit)
        return

    transaction, created = Transaction.objects.get_or_create\
        (owner=owner, name=name, account_debet=account_debet,
         account_kredit=account_kredit, jumlah=jumlah)
    display(name+' '+type, 'transaction')
    return transaction


def display(name, model):
    print 'Added %s in %s' %(name, model)

# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    populate()