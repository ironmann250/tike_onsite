from django.db import models
# Create your models here.
class badges(models.Model):
    First_name= models.CharField(max_length=100)
    Last_namee= models.CharField(max_length=100)
    company=models.CharField(max_length=100)
    Picture= models.ImageField(upload_to="media/profiles",null=True)

class Admin:
	pass

    