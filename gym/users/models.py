from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import uuid

class CUserManager(UserManager):
    def create_user(self, full_name, username, email, age, password):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model()
        user.full_name = full_name
        user.username = username
        user.email = self.normalize_email(email)
        user.set_password(password)
        user.age = age
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

class CUser(AbstractUser):
    id = models.UUIDField(primary_key=True, unique=True, auto_created=True, verbose_name="id", name="id", null=False, default=uuid.uuid4)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.IntegerField(blank=True, null=True)

    objects = CUserManager()

    class Meta:
        permissions = [
            ("can_create_staff", "Can create staff accounts."),
            ("can_create_user", "Can create all kinds of accounts."),
            ("can_add_subscriber", "Can add new subscriber."),
            ("can_approve_subscriber", "Can approve newly added subscriber."),
        ]

    def __str__(self):
        return f"{self.username} | {self.full_name} | {self.id}"