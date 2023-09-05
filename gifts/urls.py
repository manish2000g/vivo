from django.contrib import admin
from django.urls import path
from .views import customer_dashboard, customerlists, home, index, table2,uploadIMEI, registerCustomer,deleteAllImeis,adminIndex,uploadIMEInos,indexWithError,downloadData,downloadDataToday,downloadDataYesterday,reuseIMEI

urlpatterns = [
    path('', index,name = 'index'),
    path('dashboard/', adminIndex,name = 'adminIndexx'),
    path('customer-dashboard/', customer_dashboard, name='customer_dashboard'),
    path('customerlists/', customerlists, name='customerlists'),
    path('table2/', table2, name='table2'),
    path('home/', home, name='home'),

    path('uploadimei/', uploadIMEInos,name = 'uploadimei'),
    path('upload/', uploadIMEI,name = 'uploaddd'),
    path('delete-all-imei/', deleteAllImeis,name = 'deleteimeis'),
    path('', indexWithError,name = 'indexWithError'),
    path('output/', registerCustomer,name = 'register_customer'),
    path('export/', downloadData,name = 'down'),
    path('reuseimei/<str>/', reuseIMEI,name = 'reuseIMEI'),
    path('export-today/', downloadDataToday,name = 'down-today'),
    path('export-yesterday/', downloadDataYesterday,name = 'down-yest'),
]
