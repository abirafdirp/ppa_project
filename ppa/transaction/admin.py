from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export import fields
from .models import Account
from .models import Transaction


class ExportData(resources.ModelResource):

    owner__username = fields.Field(attribute='owner__username',column_name='Pembuat')


    account_kredit__code = fields.Field(attribute='account_kredit__code',
                                        column_name='kode account kredit')
    account_kredit = fields.Field(attribute='account_kredit',
                                  column_name='account kredit')
    account_debet__code = fields.Field(attribute='account_debet__code',
                                       column_name='kode account debet')
    account_debet = fields.Field(attribute='account_debet',
                                 column_name='account debet')
    name = fields.Field(attribute='name',column_name='transaksi')

    class Meta:
        model = Transaction
        exclude = ('owner', 'id')
        export_order = ('created', 'name', 'keterangan', 'account_debet__code',
        'account_debet', 'account_kredit__code', 'account_kredit',
        'jumlah', 'owner__username')


class TransactionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('created', 'name', 'keterangan', 'kode_debet', 'account_debet',
                    'kode_kredit', 'account_kredit', 'jumlah_', 'owner')

    search_fields = ('name', 'keterangan', 'jumlah_')
    readonly_fields = ('owner',)
    date_hierarchy = 'created'

    def kode_debet(self, obj):
        return obj.account_debet.code

    def kode_kredit(self, obj):
        return obj.account_kredit.code

    def jumlah_(self, obj):
        jumlah = obj.jumlah
        jumlah = map(int, str(jumlah))
        jumlah_len = len(jumlah)
        b = 0
        for a in range(-1, jumlah_len * -1, -1):
            if a % 3 == 0:
                jumlah.insert(a-b, '.')
                jumlah_len += 1
                b += 1
        return ''.join(str(e) for e in jumlah)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Account, AccountAdmin)

