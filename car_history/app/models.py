from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth import get_user_model

class WorkshopManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required for creating a user')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Jeżeli masz inne pola, które musisz dodać do superusera, dodaj je tutaj

        return self.create_user(email, password, **extra_fields)

class Workshop(AbstractUser):
    REQUIRED_FIELDS = ['name', 'nip', 'phone', 'regon', 'year', 'woj', 'powiat', 'gmina', 'zip_code', 'specialisation', 'street', 'number']
    name = models.CharField(max_length=100)
    nip = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    regon = models.CharField(max_length=15)
    year = models.DateField()
    woj = models.CharField(max_length=50)
    powiat = models.CharField(max_length=50)
    gmina = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    specialisation = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10)

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = WorkshopManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nip', 'phone', 'regon', 'year', 'woj', 'powiat', 'gmina', 'zip_code', 'specialisation', 'street', 'number']

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="workshop_groups",
        related_query_name="workshop_group",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="workshop_user_permissions",
        related_query_name="workshop_user_permission",
        blank=True,
    )

    def __str__(self):
        return self.email

class Vehicle(models.Model):
    vin_number = models.CharField(max_length=17, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    production_year = models.IntegerField()
    
    FUEL_CHOICES = [
        ('diesel', 'Diesel'),
        ('petrol', 'Benzyna'),
        ('electric', 'Elektryk'),
        ('cng', 'CNG'),
    ]
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    
    engine_capacity = models.FloatField()
    color = models.CharField(max_length=50)

class Repair(models.Model):
    repair_description = models.CharField(max_length=255)
    vin_number = models.CharField(max_length=17)
    mileage = models.IntegerField()
    repair_date = models.DateField()
    repair_time = models.TimeField()
    workshop = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)  # Dodane pole związane z warsztatem

    def __str__(self):
        return f"Repair for {self.vin_number} by {self.workshop}"
    
class ContactRequest(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email}"

