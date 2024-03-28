# urls.py
from django.urls import path
from .views import home, workshop_registration, report, information
from .views import vehicle_registration,  register_vehicle_success, workshop_registration_success
from .views import workshop_login_view, workshop_panel, vin_report
from .views import contact_view, contact_success

urlpatterns = [
    path('', home, name='home'),
    path('register_workshop/', workshop_registration, name='register_workshop'),
    path('report/', report, name='report'),
    path('information/', information, name='information'),
    path('vehicle_registration/', vehicle_registration, name='register_vehicle'),
    path('register_vehicle_success/', register_vehicle_success, name='register_vehicle_success'),
    path('workshop_registration_success/', workshop_registration_success, name='workshop_registration_success'),
    path('workshop/login/', workshop_login_view, name='workshop_login'),
    path('vin_report/<str:vin_number>/', vin_report, name='vin_report'),
    path('workshop_panel/', workshop_panel, name='workshop_panel'),
    path('contact/', contact_view, name='contact'),
    path('contact/success/', contact_success, name='contact_success'),
]

