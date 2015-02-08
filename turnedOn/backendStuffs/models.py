from django.db import models

# Create your models here.

class Regions(models.Model):
	regionChoices = (("PRI","Providence, RI"), ("NNY", "New York, NY"), ("SCA", "San Francisco, CA"))
	region = models.CharField(max_length = 3, choices = regionChoices)

	@classmethod
	def getJSONServer(cls):
		regions = [{"code":x[0],"name":x[1]} for x in cls.regionChoices]
		return regions

class UserPhone(models.Model):
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], unique=True)
	verificationNumber = models.IntegerField(max_value=9999)
	token = models.IntegerField(max_value=999999999)
	region = models.ForeignKey(Regions)

class UserinGroup(models.Model):

	region = models.ForeignKey(Regions)
	user = models.ForeignKey(UserPhone)
	name = models.CharField(max_length = 500)
	description = models.TextField(blank = True)

	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	twilioNumber = models.CharField(validators=[phone_regex])

	
