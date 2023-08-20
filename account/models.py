from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Must enter an email")

        user = self.model(
            email=self.normalize_email(email, **extra_fields),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff = True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser = True")
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    class AccountStatus(models.TextChoices):
        ACTIVE = "AT", "Active"
        INACTIVE = "IA", "Inactive"
        TRIAL = "TL", "Trial"
        BETA = "BT", "Beta Tester"

    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    status = models.CharField(max_length=2, choices=AccountStatus.choices, default=AccountStatus.INACTIVE)
    stripe_cus_id = models.CharField(max_length=500, blank=True)
    stripe_sub_id = models.CharField(max_length=500, blank=True)
    sub_start = models.DateField(blank=True, null=True)
    sub_expire = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return self.email


class StripePayment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)
    stripe_sub_id = models.CharField(max_length=500, blank=True)
