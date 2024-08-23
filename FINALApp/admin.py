from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'transaction_id', 'payment_date']
    search_fields = ['user__username', 'transaction_id']
    list_filter = ['status', 'payment_date']

admin.site.register(Payment, PaymentAdmin)
