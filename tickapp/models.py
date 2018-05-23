from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# Create your models here.
class Show(models.Model):
	title = models.CharField( max_length=100)
	poster = models.ImageField(upload_to="media/img")
	video =  models.FileField(upload_to= "media/video")
	Description = models.TextField()
	date= models.DateTimeField(str(datetime.date.today()))
	tickets_no = models.IntegerField(default=0)
	supervisor = models.ForeignKey(User,default="0")
	def __str__(self):
		return self.title

class Admin:
	pass

class profile(models.Model):
	seller = models.ForeignKey(User)
	event = models.ForeignKey(Show, default = "0")
	def __str__(self):
		return self.seller.username
	
''' @receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
	'''


class Admin:
	pass

class tickettype(models.Model):
	amount = models.IntegerField()
	event = models.ForeignKey(Show)
	tike_type = models.CharField(max_length = 50)

	def __str__(self):
		return self.tike_type

class Admin:
	pass

class ticket(models.Model):
	phone_number = models.IntegerField(null = True)
	email = models.EmailField()
	Name = models.CharField(max_length = 100, default="0")
	pin = models.CharField(max_length = 10)
	event = models.ForeignKey(Show, null = True)
	seller = models.ForeignKey(profile, null = True) #it does not show up when called
	ticket_type = models.ForeignKey(tickettype, null = True)
	status = models.BooleanField(default = False)
	date=models.DateTimeField(default=str(datetime.date.today()))
	def __str__(self):
		return self.Name

class Admin:
	pass

