from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
<<<<<<< HEAD
=======
from django.utils import timezone
>>>>>>> 935f1df3fb310e2dd8749e884ad68e49ea7b3b90
import datetime

# Create your models here.

class Show(models.Model):
<<<<<<< HEAD
	title = models.CharField( max_length=100)
	poster = models.ImageField(upload_to="media/img")
	video =  models.FileField(upload_to= "media/video")
	Description = models.TextField()
	date= models.DateTimeField(str(datetime.date.today()))
	tickets_no = models.IntegerField(default=0)
	supervisor = models.ForeignKey(User,default="0")
	def __str__(self):
		return self.title
=======
    #idshow = models.CharField(max_length=10,primary_key=True) #why did you do this ;(
    title = models.CharField(max_length=100)
    Description = models.TextField(null=True,default='')
    date = models.DateTimeField()
    venue = models.CharField(max_length=100, default="0")
    tickets_no = models.IntegerField()
    supervisor=models.ForeignKey(User,default='0')

    def __str__(self):
        return self.title

>>>>>>> 935f1df3fb310e2dd8749e884ad68e49ea7b3b90

class Admin:
    pass


class profile(models.Model):
<<<<<<< HEAD
	seller = models.ForeignKey(User)
	event = models.ForeignKey(Show, default = "0")
	def __str__(self):
		return self.seller.username
	
=======
    seller = models.ForeignKey(User)
    #iduser = models.CharField(primary_key=True, max_length = 40) #again seriously i wonder what's beneath
    event = models.ForeignKey(Show, default="0")
    def __str__(self):
        return self.seller.username


>>>>>>> 935f1df3fb310e2dd8749e884ad68e49ea7b3b90
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
<<<<<<< HEAD
	amount = models.IntegerField()
	event = models.ForeignKey(Show)
	tike_type = models.CharField(max_length = 50)
=======
    tike_type = models.CharField(max_length=100)
    event = models.ForeignKey(Show)
    amount = models.IntegerField()
    #idticktype = models.CharField(primary_key=True,max_length =30) #this is just poor codes

    def __str__(self):
        return self.tike_type
>>>>>>> 935f1df3fb310e2dd8749e884ad68e49ea7b3b90


class Admin:
    pass


class ticket(models.Model):
<<<<<<< HEAD
	phone_number = models.IntegerField(null = True)
	email = models.EmailField()
	Name = models.CharField(max_length = 100, default="0")
	pin = models.CharField(max_length = 10)
	event = models.ForeignKey(Show, null = True)
	seller = models.ForeignKey(profile, default ="0", null = True) #it does not show up when called
	ticket_type = models.ForeignKey(tickettype, default = "0", null = True)
	status = models.BooleanField(default = False)
	date=models.DateTimeField(default=str(datetime.date.today()))
	def __str__(self):
		return self.Name

class Admin:
	pass

=======
    event = models.CharField(max_length=100, null=True)
    phone_number = models.BigIntegerField(null=True)
    pin = models.CharField(max_length=10)
    email = models.EmailField(null=True)
    seller = models.CharField(max_length=20, null=True)
    Name = models.CharField(max_length=100)
    ticket_type = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)
    date=models.DateTimeField(default=timezone.now())#i hear there is a timezone module go ahead and use it instead
    def __str__(self):
        return self.Name
    


class Admin:
    pass
>>>>>>> 935f1df3fb310e2dd8749e884ad68e49ea7b3b90
