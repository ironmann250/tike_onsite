from django.shortcuts import render
from business.models import *
import csv
# Create your views here.
def create_db(request):
	if request.method == "POST":
		# get the uploaded file
		_file = request.FILES['file']
		print 'post',type(_file)
		reader = csv.reader(_file,delimiter=',')
		#add error hadling later
		for row in reader:
			new_badge=badges(First_name=row[0],Last_namee=row[1],company=row[2])
			new_badge.save()
			print row
		#reader = csv.reader(_file)#csv.DictReader(_file.splitlines())
        #for row in reader:
        #	print row
        # do something with the file

        # and return the result    
		return render(request,'html/badges/Create_database.html')        
	else:
		return render(request,'html/badges/Create_database.html')

def search(request):
    return render(request,'html/badges/search.html')

def generate(request):
     return render(request,'html/badges/add_photo.html')