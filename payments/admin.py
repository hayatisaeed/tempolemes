from django.contrib import admin
from .models import Payment, Installment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'timestamp', 'successful')
    list_filter = ('successful', 'timestamp')
    search_fields = ('customer__name', 'description', 'receipt_text')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)


@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_amount', 'due_date', 'paid', 'paid_date')
    list_filter = ('paid', 'due_date')
    search_fields = ('customer__name', 'customer__national_code' 'paid_description')
    date_hierarchy = 'due_date'
    ordering = ('-due_date',)
