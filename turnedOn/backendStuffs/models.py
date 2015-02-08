from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
regionChoices = (("PRI","Providence, RI"), ("NNY", "New York, NY"), ("SCA", "San Francisco, CA"))

class UserPhone(models.Model):
	global regionChoices
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], unique=True, max_length = 10)
	verificationNumber = models.IntegerField()
	name = models.CharField(max_length = 100)
	token = models.IntegerField()
	region = models.CharField(choices = regionChoices, max_length = 3)

class UserinGroup(models.Model):
	global regionChoices
	region = models.CharField(choices = regionChoices, max_length = 3)
	user = models.ForeignKey(UserPhone)
	name = models.CharField(max_length = 500)
	description = models.TextField(blank = True)
	isOn = models.BooleanField(default=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	twilioNumber = models.CharField(validators=[phone_regex],max_length = 10)

	
