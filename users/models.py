from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, phone, password):
        if not phone:
            raise ValueError("Users must have an email address")

        user = self.model(phone=phone)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):

        user = self.create_user(phone,password=password,)
        user.is_admin = True
        user.is_superuser =True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone = models.CharField(verbose_name="phone number is username",max_length=100,unique=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

