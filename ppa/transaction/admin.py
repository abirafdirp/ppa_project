from django.contrib import admin
from .models import Account
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('created', 'name', 'keterangan', 'kode_debet', 'account_debet',
                    'kode_kredit', 'account_kredit', 'jumlah', 'owner')

    search_fields = ('name', 'keterangan', 'jumlah')
    readonly_fields = ('owner',)
    date_hierarchy = 'created'

    def kode_debet(self, obj):
        return obj.account_debet.code

    def kode_kredit(self, obj):
        return obj.account_kredit.code

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Account, AccountAdmin)

