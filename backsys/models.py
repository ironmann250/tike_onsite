from django.db import models

# Create your models here.
class user(models.Model):
	username = models.CharField( max_length=15,primary_key= True)
	first_name = models.CharField(max_length=40)
	second_name = models.CharField(max_length = 30)
	Email = models.EmailField()
	password = models.CharField(max_length=40)
	def __str__(self):
		return self.username

class Admin:
	pass

class category(models.Model):
	category_name= models.CharField(max_length= 40)
	def __str__(self):
		return self.category_name

class Admin:
	pass

class subcategory(models.Model):
	subcategory_name = models.CharField(max_length = 20)
	category= models.ForeignKey(category)
	def __str__(self):
		return self.subcategory_name

class Admin:
	pass

class event(models.Model):
	title = models.CharField( max_length=100)
	organiser = models.ForeignKey(user)
	poster = models.ImageField(upload_to="media/img")
	video =  models.FileField(upload_to= "media/video")
	Description = models.CharField(max_length= 1000)
	date= models.DateTimeField()
	subcategory = models.ForeignKey(subcategory)
	def __str__(self):
		return self.title

class Admin:
	pass


class ticket_type(models.Model):
	event = models.ForeignKey(event)
	tike_type = models.CharField(max_length = 30)
	amount = models.CommaSeparatedIntegerField(max_length = 10)
	def __str__(self):
		return self.tike_type

class Admin:
	pass
class ticket(models.Model):
	ticket_number = models.CharField(max_length = 8, unique = True )
	pic = models.ImageField(upload_to="media/tickets")
	owner= models.ForeignKey(user)
	event = models.ForeignKey(event)
	ticket_type = models.ForeignKey(ticket_type)
	def __str__(self):
		return self.ticket_number


class Admin:
	pass

class review(models.Model):
	author = models.ForeignKey(user)
	comment = models.CharField(max_length= 200)
	event = models.ForeignKey(event)
	def __str__(self):
		return self.comment

class Admin:
	pass
