# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import WorkshopRegistrationForm
from .forms import VehicleRegistrationForm
from .forms import WorkshopLoginForm, RepairForm, VinForm, ContactForm
from .models import Workshop, Vehicle, Repair
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def home(request):
    if request.method == 'POST':
        form = VinForm(request.POST)
        if form.is_valid():
            vin_number = form.cleaned_data['vin_number']
            return redirect('vin_report', vin_number=vin_number)
    else:
        form = VinForm()

    return render(request, 'home.html', {'form': form})

def vin_report(request, vin_number):
    repairs = Repair.objects.filter(vin_number=vin_number).order_by('-repair_date', '-repair_time')
    vehicle = get_object_or_404(Vehicle, vin_number=vin_number)

    return render(request, 'vin_report.html', {'repairs': repairs, 'vin_number': vin_number, 'vehicle': vehicle})

def report(request):
    return render(request, 'report.html')

def information(request):
    return render(request, 'information.html')


def workshop_registration(request):
    if request.method == 'POST':
        form = WorkshopRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email  # ustaw nazwę użytkownika jako e-mail
            user.save()
            #login(request, user)
            return redirect('workshop_registration_success')
    else:
        form = WorkshopRegistrationForm()

    return render(request, 'register_workshop.html', {'form': form})


def workshop_registration_success(request):
    return render(request, 'register_workshop_success.html')

def vehicle_registration(request):
    if request.method == 'POST':
        form = VehicleRegistrationForm(request.POST)
        if form.is_valid():
            vin_number = form.cleaned_data['vin_number']
            brand = form.cleaned_data['brand']
            model = form.cleaned_data['model']
            production_year = form.cleaned_data['production_year']
            fuel_type = form.cleaned_data['fuel_type']
            engine_capacity = form.cleaned_data['engine_capacity']
            color = form.cleaned_data['color']

            # Sprawdzamy, czy pojazd o podanym numerze VIN już istnieje
            if not Vehicle.objects.filter(vin_number=vin_number).exists():
                # Jeżeli nie, to tworzymy nowy obiekt i go zapisujemy
                vehicle = Vehicle.objects.create(
                    vin_number=vin_number,
                    brand=brand,
                    model=model,
                    production_year=production_year,
                    fuel_type=fuel_type,
                    engine_capacity=engine_capacity,
                    color=color
                )
                return redirect('register_vehicle_success')
            else:
                # Jeżeli istnieje, możemy obsłużyć ten przypadek
                form.add_error('vin_number', 'Pojazd o podanym numerze VIN już istnieje.')
    else:
        form = VehicleRegistrationForm()

    return render(request, 'register_vehicle.html', {'form': form})
    
def register_vehicle_success(request):
    return render(request, 'register_vehicle_success.html')
    
def workshop_login_view(request):
    if request.method == 'POST':
        form = WorkshopLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('workshop_panel')
            else:
                form.add_error('email', 'Nieprawidłowy email lub hasło.')
    else:
        form = WorkshopLoginForm()

    return render(request, 'login_workshop.html', {'form': form})

@login_required(login_url='/login/')
def workshop_panel(request):
    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            repair_instance = form.save(commit=False)
            
            # Przypisz warsztat do naprawy - użyj aktualnie zalogowanego warsztatu
            repair_instance.workshop = request.user  # Załóżmy, że request.user to warsztat
            
            repair_instance.save()
            
            # Przekieruj na stronę sukcesu z odpowiednimi opcjami
            return render(request, 'repair_success.html')

    else:
        form = RepairForm()
    
    return render(request, 'workshop_panel.html', {'form': form})


    
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Dodaj kod obsługujący zapisanie zgłoszenia
            return redirect('contact_success')  # Przekieruj na stronę sukcesu
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')

