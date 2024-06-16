from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, username=None, email=None, password=None):
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            phone_number=phone_number,
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return f"{self.username} - {self.phone_number}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):

        return check_password(raw_password, self.password)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set', 
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

class Spam(models.Model):
    phone_number = models.CharField(max_length=10, unique=True)
    reason = models.TextField()
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reported_spams')

    class Meta:
        indexes = [
            models.Index(fields=['phone_number']),
        ]

    def __str__(self):
        return f"{self.phone_number} - {self.reason}"

class Global(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    spam = models.ForeignKey(Spam, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['phone_number']),
        ]

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    
    class Meta:
        unique_together = ('user', 'phone_number')
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['phone_number']),
        ]

    def __str__(self):
        return f"{self.name} - {self.phone_number}"
