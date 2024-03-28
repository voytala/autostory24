# forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core import validators
from .models import Workshop, Vehicle, Repair, ContactRequest
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class WorkshopRegistrationForm(UserCreationForm):
    
    WOJEWODZTWO_CHOICES = [
        ('dolnośląskie', 'Dolnośląskie'),
        ('kujawsko-pomorskie', 'Kujawsko-pomorskie'),
        ('lubelskie', 'Lubelskie'),
        ('lubuskie', 'Lubuskie'),
        ('łódzkie', 'Łódzkie'),
        ('małopolskie', 'Małopolskie'),
        ('mazowieckie', 'Mazowieckie'),
        ('opolskie', 'Opolskie'),
        ('podkarpackie', 'Podkarpackie'),
        ('podlaskie', 'Podlaskie'),
        ('pomorskie', 'Pomorskie'),
        ('śląskie', 'Śląskie'),
        ('świętokrzyskie', 'Świętokrzyskie'),
        ('warmińsko-mazurskie', 'Warmińsko-mazurskie'),
        ('wielkopolskie', 'Wielkopolskie'),
        ('zachodniopomorskie', 'Zachodniopomorskie'),
    ]
    name = forms.CharField(label='Nazwa', max_length=100)
    nip = forms.CharField(label='Numer NIP', max_length=15)
    phone_validator = RegexValidator(
        regex=r'^\+?\d{1,15}$', 
        message="Wprowadź poprawny numer telefonu."
    )
    phone = forms.CharField(label='Telefon', max_length=15, validators=[phone_validator])
    regon = forms.CharField(label='Numer REGON', max_length=15)
    year = forms.DateField(label='Data założenia', widget=forms.TextInput(attrs={'type': 'date'}))
    email = forms.EmailField(label='Email')
    woj = forms.ChoiceField(label='Województwo', choices=WOJEWODZTWO_CHOICES)
    powiat = forms.CharField(label='Powiat', max_length=50)
    gmina = forms.CharField(label='Gmina', max_length=50)
    zip_validator = RegexValidator(
        regex='^\d{2}-\d{3}$', 
        message="Wprowadź poprawny kod pocztowy."
    )
    zip_code = forms.CharField(label='Kod pocztowy', max_length=6, validators=[zip_validator])
    specialisation = forms.CharField(label='Specjalizacja', max_length=100)
    street = forms.CharField(label='Ulica', max_length=100)
    number = forms.CharField(label='Numer', max_length=10)
    agree_terms = forms.BooleanField(label='Akceptuję regulamin warsztatów')

    class Meta:
        model = Workshop
        fields = ['name', 'nip', 'phone', 'regon', 'year', 'email', 'woj', 'powiat', 'gmina', 'zip_code', 'specialisation', 'street', 'number', 'password1', 'password2', 'agree_terms']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dostosowanie etykiet pól hasła i powtórzenia hasła
        self.fields['password1'].label = 'Hasło'
        self.fields['password2'].label = 'Powtórz hasło'

        # Dostosowanie walidatorów hasła
        self.fields['password1'].help_text = "Twoje hasło musi zawierać co najmniej 8 znaków."
        self.fields['password2'].help_text = "Twoje hasło nie może być zbyt podobne do innych informacji osobistych."

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if len(password1) < 8:
            raise forms.ValidationError("Hasło musi mieć przynajmniej 8 znaków.")

        return password1

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Workshop.objects.filter(email=email).exists():
            raise forms.ValidationError('Użytkownik o podanym adresie e-mail już istnieje.')
        return email
    
class VehicleRegistrationForm(forms.Form):
    vin_number = forms.CharField(label='Numer VIN', max_length=17)
    brand = forms.CharField(label='Marka', max_length=50)
    model = forms.CharField(label='Model', max_length=50)
    production_year = forms.IntegerField(label='Rok produkcji', validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    
    FUEL_CHOICES = [
        ('diesel', 'Diesel'),
        ('petrol', 'Benzyna'),
        ('electric', 'Elektryk'),
        ('cng', 'CNG'),
    ]
    fuel_type = forms.ChoiceField(label='Rodzaj paliwa', choices=FUEL_CHOICES)
    
    engine_capacity = forms.FloatField(label='Pojemność silnika (cm³)')
    color = forms.CharField(label='Kolor pojazdu', max_length=50)

    class Meta:
        model = Vehicle
        fields = ['vin_number', 'brand', 'model', 'production_year', 'fuel_type', 'engine_capacity', 'color']

class WorkshopLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
class RepairForm(forms.ModelForm):
    repair_description = forms.CharField(label='Opis naprawy', widget=forms.Textarea)
    vin_number = forms.CharField(label='Numer VIN', max_length=17)
    mileage = forms.IntegerField(label='Przebieg')
    
    # Oddzielne pola na datę i godzinę
    repair_date = forms.DateField(label='Data naprawy', widget=forms.TextInput(attrs={'type': 'date'}))
    repair_time = forms.TimeField(label='Godzina naprawy', input_formats=['%H:%M'], widget=forms.TextInput(attrs={'type': 'time'}))

    class Meta:
        model = Repair
        fields = ['repair_description', 'vin_number', 'mileage', 'repair_date', 'repair_time']
        widgets = {
            'repair_description': forms.Textarea,
            'repair_date': forms.TextInput(attrs={'type': 'date'}),
            'repair_time': forms.TextInput(attrs={'type': 'time'}),
        }
class VinForm(forms.Form):
    vin_number = forms.CharField(label='Numer VIN', max_length=17)
    
class ContactForm(forms.ModelForm):
    name = forms.CharField(label='Temat', max_length=100)
    email = forms.EmailField(label='Twój adres email')
    message = forms.CharField(label='Wiadomość', widget=forms.Textarea)
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'message']
