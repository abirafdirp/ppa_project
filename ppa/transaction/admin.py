from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export import fields
from .models import Account
from .models import Transaction
from .models import AccountCategory


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
    list_display = ('created', 'name', 'no_kwitansi', 'keterangan', 'kode_debet', 'account_debet',
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
        jumlah = "{:,}".format(jumlah)
        return jumlah

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.has_perm('transaction.delete_transaction'):
            self.exclude.append('created')
            self.exclude.append('modified')
        return super(TransactionAdmin, self).get_form(request, obj, **kwargs)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_category', 'code', 'jumlah_')
    readonly_fields = ('jumlah',)

    def jumlah_(self, obj):
        jumlah = obj.jumlah
        jumlah = "{:,}".format(jumlah)
        return jumlah

class AccountCategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(AccountCategory, AccountCategoryAdmin)

