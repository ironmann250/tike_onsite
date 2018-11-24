from django.shortcuts import render

# Create your views here.
def create_db():
    return render(request,'html/badges/create_database.html')