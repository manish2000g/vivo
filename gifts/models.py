import datetime
from django.db import models


class Sales(models.Model):
    sales_count = models.IntegerField(default=0)
    date = models.DateField(
        auto_now=False, auto_created=False, auto_now_add=False)

    def __str__(self):
        return str(self.sales_count)


class RechargeCard(models.Model):
    cardno = models.CharField(max_length=400)
    provider = models.CharField(max_length=400)
    amount = models.IntegerField()
    image = models.ImageField(
        upload_to='recharge_card_images/', null=True, blank=True)
    is_assigned = models.BooleanField(default=False) 

    
    def __str__(self):
        return self.cardno

class Gift(models.Model):
    name = models.CharField(max_length=400)
    image_url = models.FileField()

    def __str__(self):
        return self.name


class IMEINO(models.Model):
    imei_no = models.CharField(max_length=400)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.imei_no


class FixOffer(models.Model):
    imei_no = models.CharField(max_length=400)
    quantity = models.IntegerField()
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)

    def __str__(self):
        return self.imei_no


class Offers(models.Model):
    OFFER_CHOICES = [
        ("After every certain sale", "After every certain sale"),
        ("At certain sale position", "At certain sale position"),
    ]

    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    quantity = models.IntegerField()
    type_of_offer = models.CharField(max_length=800, choices=OFFER_CHOICES)
    offer_condition_value = models.CharField(max_length=500)

    def __str__(self):
        return f"Offer on {self.gift.name}"

    def is_valid_date(self):
        today = datetime.date.today()
        return self.start_date <= today <= self.end_date

    class Meta:
        ordering = ("start_date",)


class MobilePhone(models.Model):
    phone_model = models.CharField(max_length=400)
    phone_image = models.ImageField()
    phone_price = models.IntegerField()

    def __str__(self):
        return self.phone_model


class Customer(models.Model):

    CAMPAIGN_CHOICES = [
        ("Facebook Ads", "Facebook Ads"),
        ("Reatil Shop", "Reatil Shop"),
        ("Google Ads", "Google Ads"),
        ("Others", "Others"),
    ]

    customer_name = models.CharField(max_length=400)
    shop_name = models.TextField()
    sold_area = models.CharField(max_length=800)
    phone_number = models.CharField(max_length=400)
    phone_model = models.ForeignKey(MobilePhone, on_delete=models.CASCADE)
    sale_status = models.CharField(max_length=400, default="SOLD")
    prize_details = models.CharField(
        max_length=900, default="Happy Sales Carnival")
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE, null=True)
    imei = models.CharField(max_length=400)
    date_of_purchase = models.DateField(auto_now_add=True, auto_now=False)
    how_know_about_campaign = models.CharField(
        max_length=800, choices=CAMPAIGN_CHOICES)
    recharge_card = models.ForeignKey(RechargeCard, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.customer_name

    class Meta:
        ordering = ("-date_of_purchase",)
