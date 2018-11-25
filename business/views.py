from django.shortcuts import render
from business.models import *
from django.db.models import Q
from tickapp.utils import libbadge
from StringIO import StringIO
from django.http import  HttpResponse, HttpResponseRedirect
import csv

def save_to_string(img):
    obj=StringIO()
    img.save(obj,format='jpeg',quality=90)
    obj.seek(0)
    return obj.read()
# Create your views here.
def create_db(request):
	if request.method == "POST":
		# get the uploaded file
		_file = request.FILES['file']
		print 'post',type(_file)
		# do something with the file
		#add error hadling later
		reader = csv.reader(_file,delimiter=',')
		for row in reader:
			new_badge=badges(First_name=row[0],Last_namee=row[1],company=row[2])
			new_badge.save()
			print row
        # and return the result   
        # redirect to search maybe 
		return HttpResponseRedirect('/search_database')        
	else:
		return render(request,'html/badges/Create_database.html')

def search(request):
	if 'q' in request.GET.keys():
		q=request.GET['q']
		badges_=badges.objects.filter(Q(First_name__contains=q)|Q(Last_namee__contains=q)|Q(company__contains=q))
		print len(badges_)
	return render(request,'html/badges/search.html',locals())

def generate(request,id):
	badge=badges.objects.get(id=id)
	libbadge.init()
	libbadge.user_vals={
	'pin':'#TIKE'+str(badge.id),
	'name':badge.First_name+' '+badge.Last_namee,
	'title':badge.company 
	}
	badge_img=save_to_string(libbadge.make_badge())
	response= HttpResponse(badge_img,content_type='image/jpeg')
	return response

def edit(request,id):
	badge=badges.objects.get(id=id)
	if request.method == "POST":
		#editing names necessary?
		file_ = request.FILES['image']
		badge.Picture=file_
		badge.save()
	return render(request,'html/badges/add_photo.html',locals())




def check(request):
	if 'q' in request.GET.keys():
		try: 
			badge=badges.objects.get(Q(id__exact=q))
		except badges.DoesNotExist:
			result={}
			return JsonResponse(result)

		first_name=badge.first_name
		last_name=badge.last_name
		company=badge.company
		result= {'first_name':first_name,'last_name': last_name,'company':company}
		return JsonResponse(result)
	


		