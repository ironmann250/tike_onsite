from django.shortcuts import render
from business.models import *
from django.db.models import Q
from tickapp.utils import qrcodeGenerator
#from tickapp.utils import libbadge
from StringIO import StringIO
from django.http import  HttpResponse, HttpResponseRedirect
from django.http import  HttpResponse,JsonResponse, HttpResponseRedirect
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
		print ('post',type(_file))
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
#from  tickapp.utils 
from tickapp.utils import qrcodeGenerator
from PIL import Image,ImageFont,ImageDraw,ImageOps

#why not make this into a class for a change :) (lot's of coffee lol)
#nahh speedy, no time to structure

#init vals, make it as dict to use it directly in a loop



def make_badge(user_vals,qrcode, bias=10):
	size=(480,240)#width,height
	text_pos=[37,27]#array cause it changes at somepoint
	qrcode_pos=(330,95)
	pin_pos=(287,208)
	font_name,font_size=['Helvetica-Normal.ttf',30]
	color='white' #maybe light gray? front always black
	canvas=Image.new("RGB",size,color)
	font = ImageFont.truetype(font_name, font_size)

	#resize qrcode to 100 by 100 px and add it to main image
	qrcode.thumbnail((100,100),Image.ANTIALIAS)#if buggy use consise_rect algo
	canvas.paste(qrcode,qrcode_pos)
	# text stuffs now
	drawHandler = ImageDraw.Draw(canvas)
	#write line get dimensions to compute newline
	#name
	drawHandler.text(text_pos, user_vals['name'], (0,0,0), font=font)
	textlen=font.getsize(user_vals['name'])
	text_pos[1]=text_pos[1]+textlen[1]+bias#adjust the bias as needed
	#title
	drawHandler.text(text_pos, user_vals['title'], (0,0,0), font=font)
	#code
	drawHandler.text(pin_pos, user_vals['pin'], (0,0,0), font=font)
	#show
	return canvas

def generate(request,id):
	badge=badges.objects.get(id=id)
	#libbadge.init()
	user_vals={}
#core vals
#messed the filesys with fonts...
#compute size from text? later now no more than 30 chars(further work more coffee)
	
	user_vals={
	'pin':badge.id,
	'name':badge.First_name+' '+badge.Last_namee,
	'title':badge.company 
	}
#init vals
	
	qrcode=qrcodeGenerator.init(user_vals['pin'])#or use make_qrcode 

#vals to write on image
	badge_img=save_to_string(make_badge(user_vals, qrcode))
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
		q=request.GET['q']
		badge=badges.objects.get(Q(id__exact=q))
		first_name=badge.First_name
		last_name=badge.Last_namee
		company=badge.company
		result={'first_name': first_name, 'last_name': last_name, 'company':company}
		return JsonResponse(result)

	else:
		result={}
		return JsonResponse(result)
	


		