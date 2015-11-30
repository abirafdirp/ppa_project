from django.contrib import admin
from django.db.models import Sum
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
    list_display = ('date', 'name', 'no_kwitansi', 'keterangan', 'kode_debet', 'account_debet',
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
            self.exclude.append('date')
        return super(TransactionAdmin, self).get_form(request, obj, **kwargs)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_category', 'code', 'jumlahh', 'jumlah')
    readonly_fields = ('jumlah',)

    def jumlahh(self, obj):
        debet_tambah = obj.transaksi_debet.filter(account_debet__account_category__debet='+').aggregate(Sum('jumlah'))
        debet_kurang = obj.transaksi_debet.filter(account_debet__account_category__debet='-').aggregate(Sum('jumlah'))

        if debet_tambah.values()[0] == None:
            debet_tambah = 0
        else:
            debet_tambah = debet_tambah.values()[0]

        if debet_kurang.values()[0] == None:
            debet_kurang = 0
        else:
            debet_kurang = debet_kurang.values()[0]

        debet = debet_tambah - debet_kurang

        kredit_tambah = obj.transaksi_kredit.filter(account_kredit__account_category__kredit='+').aggregate(Sum('jumlah'))
        kredit_kurang = obj.transaksi_kredit.filter(account_kredit__account_category__kredit='-').aggregate(Sum('jumlah'))

        if kredit_tambah.values()[0] == None:
            kredit_tambah = 0
        else:
            kredit_tambah = kredit_tambah.values()[0]

        if kredit_kurang.values()[0] == None:
            kredit_kurang = 0
        else:
            kredit_kurang = kredit_kurang.values()[0]

        kredit = kredit_tambah - kredit_kurang
        jumlah = abs(debet + kredit)
        jumlah = "{:,}".format(jumlah)
        return jumlah


class AccountCategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(AccountCategory, AccountCategoryAdmin)

