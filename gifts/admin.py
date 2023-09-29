from django.contrib import admin
from .models import Customer, Gift, MobilePhone, Offers, Sales, IMEINO, FixOffer, MobilePhone, RechargeCard


admin.site.register(Gift)
admin.site.register(Sales)
admin.site.register(Offers)
admin.site.register(IMEINO)
admin.site.register(FixOffer)
admin.site.register(MobilePhone)
admin.site.register(RechargeCard)



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "shop_name",
        "sold_area",
        "phone_number",
        "phone_model",
        "sale_status",
        "gift",
        "imei",
        "date_of_purchase",
        "how_know_about_campaign",
    )
    list_filter = (
        "date_of_purchase",
    )

    class Meta:
        model = Customer
