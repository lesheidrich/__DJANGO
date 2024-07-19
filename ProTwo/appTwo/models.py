from django.db import models

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self) -> str:
        return str(f"first_name: {self.first_name} last_name: {self.last_name} email: {self.email}")