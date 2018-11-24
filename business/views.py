from django.shortcuts import render

# Create your views here.
def create_db(request):
    return render(request,'html/badges/create_database.html')

def search(request):
    return render(request,'html/badges/create_database.html')

def generate(request):
     return render(request,'html/badges/create_database.html')