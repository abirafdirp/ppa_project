from django.contrib import admin
from .models import Account
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('created', 'name', 'kode_debet', 'account_debet',
                    'kode_kredit', 'account_kredit', 'jumlah')

    search_fields = ('created', 'name')

    def kode_debet(self, obj):
        return obj.account_debet.code

    def kode_kredit(self, obj):
        return obj.account_kredit.code

class AccountAdmin(admin.ModelAdmin):
    pass

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Account, AccountAdmin)

