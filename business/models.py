from django.db import models
import random
def id_random():
    return int(random.random()*1000)
# Create your models here.
class badges(models.Model):
    id=models.IntegerField(default=id_random())
    First_name= models.CharField(max_length=100)
    Last_namee= models.CharField(max_length=100)
    company=models.CharField(max_length=100)
    Picture= models.ImageField(upload_to="media/profiles")

class Admin:
	pass

    