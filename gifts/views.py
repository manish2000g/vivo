from .models import RechargeCard
from django.shortcuts import render, redirect
from django.db.models import Q
from datetime import datetime
from django import forms
from .models import Customer, MobilePhone, RechargeCard
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response
from .models import Customer, Sales, Offers, Gift, IMEINO, FixOffer
from datetime import date, timedelta
import csv
from json import dumps
from datetime import date, datetime


def index(request):
    phone_models = MobilePhone.objects.all()

    context = {
        'phone_models': phone_models,
    }
    return render(request, 'index.html', context)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def adminIndex(request):
    customerss = Customer.objects.all()
    ctx = {
        "customers": customerss
    }
    return render(request, "admin2/index.html", ctx)


def indexWithError(request):
    ctx = {
        "error": "Invalid IMEI"
    }
    return render(request, "index.html", ctx)


def uploadIMEI(request):
    with open('datas.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        for row in data:
            okk = IMEINO.objects.create(imei_no=row[0])
            okk.save()
    ctx = {
        "error": "Invalid Uploaded"
    }
    return render(request, "index.html", ctx)


def deleteAllImeis(request):
    allimeis = IMEINO.objects.all()
    allimeis.delete()

    ctx = {
        "error": "All IMEI Deleted"
    }
    return render(request, "index.html", ctx)


def uploadIMEInos(request):
    if request.method == 'POST':

        filee = request.FILES['csv_file']
        file_data = filee.read().decode('utf-8')
        lines = file_data.split('\n')

        imei_objects = [IMEINO(imei_no=line) for line in lines if line.strip()]

        # Batch insert the IMEI numbers
        IMEINO.objects.bulk_create(imei_objects)

        ctx = {'error': 'IMEI Uploaded'}
        return render(request, 'index.html', ctx)

    return render(request, 'upload_imei.html')


def reuseIMEI(request, str):
    okk = IMEINO.objects.get(imei_no=str)
    okk.used = False
    okk.save()
    ctx = {
        "error": "Invalid IMEI"
    }
    return render(request, "index.html", ctx)


def upload_recharge_cards(request):
    if request.method == "POST":
        csv_file = request.FILES.get('csv_file')

        if csv_file:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)

            for row in csv_reader:
                cardno = row['cardno']
                provider = row['provider']
                amount = int(row['amount'])
                image_url = row.get('image', None)

                # Create a new RechargeCard object and save it
                recharge_card = RechargeCard(
                    cardno=cardno,
                    provider=provider,
                    amount=amount,
                    image=image_url
                )
                recharge_card.save()

            return redirect('upload_success')

    return render(request, 'upload_recharge_cards.html')


def customer_dashboard(request):
    # Retrieve all customers from the database
    customers = Customer.objects.all()
    customers_with_gifts = Customer.objects.filter(gift__isnull=False)
    customers_without_gifts = Customer.objects.filter(gift__isnull=True)

    context = {
        'customers': customers,
        'customers_with_gifts': customers_with_gifts,
        'customers_without_gifts': customers_without_gifts,
    }

    return render(request, 'customer_dashboard.html', context)


def customerlists():
    datalist = list(Customer.objects.all().values('customer_name', 'shop_name', 'sold_area', 'phone_number', 'phone_model',
                    'sale_status', 'prize_details', 'imei', 'gift__name', 'date_of_purchase', 'how_know_about_campaign'))
    return JsonResponse(datalist, safe=False)


def table2(request):
    datalist = list(Customer.objects.all().values('customer_name', 'shop_name', 'sold_area', 'phone_number', 'phone_model',
                    'sale_status', 'prize_details', 'imei', 'gift__name', 'date_of_purchase', 'how_know_about_campaign'))
    data = dumps(datalist, default=json_serial)
    return render(request, 'table2.html', {"data": data})


def download_customers_with_gifts(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    # Create a base queryset for customers with gifts
    queryset = Customer.objects.filter(gift__isnull=False)

    if start_date and end_date:
        # Filter data within the specified date range
        queryset = queryset.filter(
            date_of_purchase__range=(start_date, end_date))

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers_with_gifts.csv"'

    # Create a CSV writer and write the header row
    writer = csv.writer(response)
    writer.writerow(['Customer Name', 'Shop Name', 'Sold Area', 'Phone Number', 'Phone Model',
                     'Sale Status', 'Prize Details', 'IMEI', 'Gift', 'Date of Purchase', 'How Know About Campaign'])

    # Write the data rows
    for customer in queryset:
        writer.writerow([customer.customer_name, customer.shop_name, customer.sold_area, customer.phone_number, customer.phone_model,
                         customer.sale_status, customer.prize_details, customer.imei, customer.gift, customer.date_of_purchase, customer.how_know_about_campaign])

    return response


def download_customers_without_gifts(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    # Create a base queryset for customers without gifts
    queryset = Customer.objects.filter(gift__isnull=True)

    if start_date and end_date:
        # Filter data within the specified date range
        queryset = queryset.filter(
            date_of_purchase__range=(start_date, end_date))

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers_without_gifts.csv"'

    # Create a CSV writer and write the header row
    writer = csv.writer(response)
    writer.writerow(['Customer Name', 'Shop Name', 'Sold Area', 'Phone Number', 'Phone Model',
                     'Sale Status', 'Prize Details', 'IMEI', 'Gift', 'Date of Purchase', 'How Know About Campaign'])

    # Write the data rows
    for customer in queryset:
        writer.writerow([customer.customer_name, customer.shop_name, customer.sold_area, customer.phone_number, customer.phone_model,
                         customer.sale_status, customer.prize_details, customer.imei, customer.gift, customer.date_of_purchase, customer.how_know_about_campaign])

    return response


def home(request):
    context = {
    }
    return render(request, 'home.html', context)


""" def uploadCustomer2(request):
    with open('datas2.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        for row in data:
            if(row[5]!=''):
                gifts = Gift.objects.get(name=row[5])
                customer = Customer.objects.create(customer_name=row[0],phone_number=row[3],shop_name=row[1],sold_area=row[2],phone_model=row[4],sale_status="SOLD",imei=row[6],how_know_about_campaign=row[8],date_of_purchase=row[7],gift=gifts)
                customer.save()
            else:
                customer = Customer.objects.create(customer_name=row[0],phone_number=row[3],shop_name=row[1],sold_area=row[2],phone_model=row[4],sale_status="SOLD",imei=row[6],how_know_about_campaign=row[8],date_of_purchase=row[7])
                customer.save()
            
            try:
                imeiii = IMEINO.objects.get(imei_no=row[6])
                imeiii.used = True
                imeiii.save()
            except:
                pass
    ctx = {
        "error":"Invalid IMEI"
    }
    return render(request, "index.html",ctx) """


def downloadData(request):
    # Get all data from UserDetail Databse Table
    users = Customer.objects.all()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all.csv"'

    writer = csv.writer(response)
    writer.writerow(['customer_name', 'shop_name', 'sold_area', 'phone_number',
                    'phone_model', 'gift', 'imei', 'date_of_purchase', 'how_know_about_campaign'])

    for user in users:
        if user.gift:
            writer.writerow([user.customer_name, user.shop_name, user.sold_area, user.phone_number,
                            user.phone_model, user.gift.name, user.imei, user.date_of_purchase, user.how_know_about_campaign])
        else:
            writer.writerow([user.customer_name, user.shop_name, user.sold_area, user.phone_number,
                            user.phone_model, user.gift, user.imei, user.date_of_purchase, user.how_know_about_campaign])
    return response


def downloadDataToday(request):
    # Get all data from UserDetail Databse Table
    today_date = date.today()
    users = Customer.objects.filter(date_of_purchase=today_date)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="today.csv"'

    writer = csv.writer(response)
    writer.writerow(['customer_name', 'shop_name', 'sold_area', 'phone_number',
                    'phone_model', 'gift', 'imei', 'date_of_purchase', 'how_know_about_campaign'])

    for user in users:
        if user.gift:
            writer.writerow([user.customer_name, user.shop_name, user.sold_area, user.phone_number,
                            user.phone_model, user.gift.name, user.imei, user.date_of_purchase, user.how_know_about_campaign])
        else:
            writer.writerow([user.customer_name, user.shop_name, user.sold_area, user.phone_number,
                            user.phone_model, user.gift, user.imei, user.date_of_purchase, user.how_know_about_campaign])
    return response


def downloadDataYesterday(request):
    # Get all data from UserDetail Databse Table
    today_date = date.today() - timedelta(days=1)
    users = Customer.objects.filter(date_of_purchase=today_date)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="today.csv"'

    writer = csv.writer(response)
    writer.writerow(['customer_name', 'shop_name', 'sold_area', 'phone_number',
                    'phone_model', 'gift', 'imei', 'date_of_purchase', 'how_know_about_campaign'])

    for user in users:
        if user.gift:
            writer.writerow([user.customer_name, user.shop_name, user.sold_area, user.phone_number,
                            user.phone_model, user.gift.name, user.imei, user.date_of_purchase, user.how_know_about_campaign])
        else:
            writer.writerow([user.customer_name, user.shop_name, user.sold_area, user.phone_number,
                            user.phone_model, user.gift, user.imei, user.date_of_purchase, user.how_know_about_campaign])
    return response


def registerCustomer(request):
    if request.method == "POST":
        customer_name = request.POST["customer_name"]
        contact_number = request.POST["phone_number"]
        shop_name = request.POST["shop_name"]
        sold_area = request.POST["sold_area"]
        phone_model = request.POST["phone_model"]
        imei_number = request.POST["imei_number"]
        how_know_about_campaign = request.POST["how_know_about_campaign"]

        # Check if a customer with the same phone number already exists
        if Customer.objects.filter(phone_number=contact_number).exists():
            ctx = {
                "error": "This phone number is already registered by another customer."
            }
            return render(request, "index.html", ctx)

        """ IMEI no check """
        """ IMEI no check """

        get_all_customers = Customer.objects.all()

        for cust in get_all_customers:
            if cust.imei == imei_number:
                ctx = {
                    "error": "This IMEI no is already registered by customer "+cust.customer_name
                }
                return render(request, "index.html", ctx)

        imei_check = False
        get_all_imeis = IMEINO.objects.filter(used=False)
        for imeei in get_all_imeis:
            if imei_number == str(imeei):
                imei_check = True

        if (imei_check == False):
            ctx = {
                "error": "Invalid IMEI no entered"
            }
            return render(request, "index.html", ctx)

        customer = Customer.objects.create(customer_name=customer_name, phone_number=contact_number, shop_name=shop_name, sold_area=sold_area,
                                           phone_model=phone_model, sale_status="SOLD", imei=imei_number, how_know_about_campaign=how_know_about_campaign)
        customer.save()
        imeiii = IMEINO.objects.get(imei_no=imei_number)
        imeiii.used = True
        imeiii.save()
        giftassign = False

        """ Select Gift """
        today_date = date.today()
        offers_all = Offers.objects.filter(end_date=today_date)
        sales_all = Sales.objects.all()
        check = 0
        for sale in sales_all:
            if sale.date == today_date:
                check = 1
        if check == 0:
            saless = Sales.objects.create(sales_count=0, date=today_date)
            saless.save()

        sale_today = Sales.objects.get(date=today_date)
        get_sale_count = sale_today.sales_count
        sale_today.sales_count = get_sale_count+1
        sale_today.save()

        dsd = FixOffer.objects.all()

        myoff = False

        for off in dsd:
            if (imei_number in off.imei_no):
                if (off.quantity > 0):
                    customer.gift = off.gift
                    customer.save()
                    giftassign = True
                    myoff = True
                    off.quantity = 0
                    off.save()
                    break

        if myoff == False:
            for offer in offers_all:
                if offer.type_of_offer == "After every certain sale":
                    if (((get_sale_count+1) % offer.offer_condtion_value == 0)) and (offer.quantity > 0):
                        """ Grant Gift """
                        qty = offer.quantity
                        customer.gift = offer.gift
                        customer.save()
                        offer.quantity = qty-1
                        offer.save()
                        giftassign = True
                        break
                else:
                    if ((get_sale_count+1) == offer.offer_condtion_value) and (offer.quantity > 0):
                        """ Grant Gift """
                        qty = offer.quantity
                        customer.gift = offer.gift
                        customer.save()
                        offer.quantity = qty-1
                        offer.save()
                        giftassign = True
                        break
        if not giftassign:
            recharge_card = RechargeCard.objects.filter(
                is_assigned=False).first()
            if recharge_card:
                customer.recharge_card = recharge_card
                customer.save()
                recharge_card.is_assigned = True
                recharge_card.save()

        return render(request, "output.html", {"customer": customer, "giftassigned": giftassign})
    else:
        return redirect('indexWithError')
