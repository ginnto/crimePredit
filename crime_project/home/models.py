from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class complaints(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    complaint = models.CharField(max_length=50)
    name = models.CharField(max_length=50,default='name')
    details = models.TextField()
    address = models.TextField(default='address')
    pincode_regex = RegexValidator(
        regex=r'^\d{6}$',
        message="Pincode must be a 6-digit number."
    )
    pincode = models.CharField(
        max_length=6,
        validators=[pincode_regex],default='689105'
    )
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.name} {self.complaint} {self.user}'


class replays(models.Model):
    complaint = models.ForeignKey(complaints, on_delete=models.CASCADE, null=True, default=None, to_field="id")
    replay = models.TextField(default='', blank=False)



class PoliceUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    station= models.CharField(max_length=30,default='',null=False)
    stationadmin= models.CharField(max_length=30,default='')
    adminposition = models.CharField(max_length=30,default='')
    district= models.CharField(max_length=30,default='')
    address= models.TextField(default='')
    phonenumber= models.CharField(max_length=20,default='')
    # Add any additional fields for the police user

    def __str__(self):
        return self.user.username

class crime_types(models.Model):
    ctypes = models.CharField(max_length=30)

    def __str__(self):
        return '{}'.format(self.ctypes)

class fir(models.Model):
    police_station = models.ForeignKey(PoliceUser, on_delete=models.CASCADE)
    crime_type = models.ForeignKey(crime_types, on_delete=models.CASCADE)
    criminal_name = models.CharField(max_length=30)
    criminal_address = models.CharField(max_length=30)
    description = models.CharField(max_length=30)


