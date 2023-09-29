from django import views
from django.contrib import admin
from django.urls import path
from .views import customer_dashboard, customerlists, download_customers_with_gifts, download_customers_without_gifts, home, index, table2, upload_recharge_cards,uploadIMEI, registerCustomer,deleteAllImeis,adminIndex,uploadIMEInos,indexWithError,downloadData,downloadDataToday,downloadDataYesterday,reuseIMEI

urlpatterns = [
    path('', index,name = 'index'),
    path('dashboard/', adminIndex,name = 'adminIndexx'),
    path('customer-dashboard/', customer_dashboard, name='customer_dashboard'),
    path('customerlists/', customerlists, name='customerlists'),
    path('table2/', table2, name='table2'),
    path('home/', home, name='home'),

    path('download_customers_with_gifts/', download_customers_with_gifts,
         name='download_customers_with_gifts'),
    path('download_customers_without_gifts/', download_customers_without_gifts,
         name='download_customers_without_gifts'),
    path('upload-recharge-cards/', upload_recharge_cards,
         name='upload_recharge_cards'),
    path('uploadimei/', uploadIMEInos, name='uploadimei'),
    path('upload/', uploadIMEI,name = 'uploaddd'),
    path('delete-all-imei/', deleteAllImeis,name = 'deleteimeis'),
    path('', indexWithError,name = 'indexWithError'),
    path('output/', registerCustomer,name = 'register_customer'),
    path('export/', downloadData,name = 'down'),
    path('reuseimei/<str>/', reuseIMEI,name = 'reuseIMEI'),
    path('export-today/', downloadDataToday,name = 'down-today'),
    path('export-yesterday/', downloadDataYesterday,name = 'down-yest'),
]
