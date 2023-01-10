from django.db import models
from guest_user.models import Guest
from django.conf import settings

class Profile(models.Model):
    guest = models.ForeignKey(settings.GUEST_USER_MODEL, on_delete=models.CASCADE, related_name="guest")


class Result(models.Model):
    class Choices(models.TextChoices):
        CHOICE_1 = 'acne', 'Acne'
        CHOICE_2 = 'basilcell', 'Basal Cell',
        CHOICE_3 = 'eczema', 'Eczema',
        CHOICE_4 = 'normal', 'Normal',
        CHOICE_5 = 'wartz', 'Wartz',
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="result")
    description = models.CharField(max_length=128, blank=True, null=True)
    sex = models.CharField(max_length=64, blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    skin_disease = models.CharField(max_length=32, choices=Choices.choices)
    pic = models.ImageField(upload_to="images/")
    accuracy = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)