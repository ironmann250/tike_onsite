from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from tickapp.models import profile,ticket,tickettype,Show
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
from django.http import  HttpResponse,JsonResponse, HttpResponseRedirect
from StringIO import StringIO
from tickapp.utils import qrcodeGenerator
# Create a pin code
import random
import string
import smtplib
from smsapi.client import SmsAPI
from smsapi.responses import ApiError
import datetime
web_url='http://tikeweb.herokuapp.com/'  
'''
Munyakabera Jean Claude Log:
in the implementation of the codes for this view there have been an inefficient use
or should i say no usage of django's object relations things like fetching from the
database class directly and filtering the resulting like this Show.objects.get(title = event)
while you already requested a row with that event like this event = objs.event
so it would be more efficient to use directly that event underlying capabilities rather
that call a separate filter from the main table class 
for now i will not change most of the code except those that i will work on
'''

def save_to_string(img):
    obj=StringIO()
    img.save(obj,format='PNG',quality=90)
    obj.seek(0)
    return obj.read() 

def render_qrcode(request,text):#text is pin #this is considered a helper function not really a view func
    text=web_url+'result?pin='+text
    qrcode=save_to_string(qrcodeGenerator.init(text)) #render and save it in mem
    response=HttpResponse(qrcode,content_type='image/png') 
    return response


api = SmsAPI()

api.set_username('tike')
api.set_password('869579e0598bd70a216261a80507efed')
api.auth_token = 'q6QWErR7qkI9MNzA4bJJ86fltC5KfselYYiO2DUi'
    #sending SMS

def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    """
    generate a 4 character pin that is unique in db/ticket
    """
    pin=''.join(random.choice(chars) for _ in range(size))
    if ticket.objects.filter(pin=pin).count() !=0:
        id_generator()
    else:
        return pin


#creating an email
me='tikerwanda@gmail.com'
web_url='http://tikeweb.herokuapp.com/'  #fetch from settings


@login_required
def sell(request):
    if request.user.is_authenticated():
        username = request.user.username

        objs = profile.objects.get(seller__username=username)
        event = objs.event
        view=event.id
        tickobjs=list()
        tickobjs = tickettype.objects.filter(event= event)
        ticket_types=list()
        ticketdict = {}
        for tickobj in tickobjs:
            ticket_types.append(tickobj.tike_type)
            element = ticket_types[-1]
            ticketdict[element]=(tickobj.amount)
        show = Show.objects.get(title = event)
        total = show.tickets_no 
        soldobj = list()
        stobj = list()
        soldobj = ticket.objects.filter(event= show)
        sold= len(soldobj)
        stobj = ticket.objects.filter(event = event, seller= objs)
        st= len(stobj)
        perc =  (sold/total)* 100
    if request.method == 'POST':
        event= request.POST['event']
        ticket_type = request.POST['ticket_type']
        name= request.POST['name']
        if name=='':name='undef'
        email=request.POST['email']
        tel= request.POST['tel']
        tel_double_check=request.POST['pass']
        autocheck='off'
        if 'autocheck' in request.POST.keys(): autocheck=request.POST['autocheck']
        print autocheck
        usage = request.POST['usage']
        pin = id_generator()
        eventobj= Show.objects.get(title = event)
        sellerobj= profile.objects.get(seller__username = username)
        tobj= tickettype.objects.get(tike_type = ticket_type)
        fee = tobj.amount
        datetime= eventobj.date 
        if usage == '0':
            try:
                sold1 = sold +1
                htmlmsg = render_to_string('html/essay/email.html',{'event':event,'names': name,'ticket_type':ticket_type,'fee': fee,'date':datetime,'pin':pin,'sold':sold1})
                send_mail('Your ticket to attend the event','',me,email,html_message= htmlmsg, fail_silently= False)
                if autocheck=='on':
                    newticket= ticket.objects.create(phone_number = tel, email= email, Name= name, pin = pin, event = eventobj, seller= sellerobj,ticket_type= tobj,status=True)
                else:
                    newticket= ticket.objects.create(phone_number = tel, email= email, Name= name, pin = pin, event = eventobj, seller= sellerobj,ticket_type= tobj)
            
                newticket.save()
            except smtplib.SMTPException:
                return render(request,'html/essay/sell.html',{'view' : 'Sell','action': True, 'event': event, 'ticket_types' : ticket_types, 'action': True,'username':username,'st': st, 'income': 0,'ticketdict': ticketdict , 'total': total,'sold': sold,'perc': perc,'email':email,'pin':pin})
            total = total
            st = st + 1
            sold = sold + 1
            perc = (sold/total)* 100
            return render(request,'html/essay/sell.html',{'view' : 'Sell', 'action': False, 'event': event, 'ticket_types' : ticket_types, 'action': False,'username':username,'st':st,'income': 0,'ticketdict': ticketdict,'total': total,'sold': sold,'perc': perc,'email':email })
        if usage == '1':
            try:
                api.service('sms').action('send')
                api.set_content('[%1%] ticket for the [%2%] for [%3%] on [%4%], code: '+pin)
                api.set_params(ticket_type,event,name,datetime.strftime("%d-%b at %H:%M")) 
                api.set_to(tel)
                #api.set_from('Tike ltd') #Requested sender name
                result = api.execute()
                for r in result:
                    print (r.id, r.points, r.status)
                total = total
                st = st + 1
                sold = sold + 1
                perc = (sold/total)* 100  
                if autocheck=='on':
                    newticket=ticket.objects.create(phone_number = tel, email= email, Name= name, pin = pin, event = eventobj, seller= sellerobj,ticket_type= tobj,status=True)
                else:
                    newticket= ticket.objects.create(phone_number = tel, email= email, Name= name, pin = pin, event = eventobj, seller= sellerobj,ticket_type= tobj)            
                newticket.save()
                return render(request,'html/essay/sell.html',{'view' : 'Sell', 'event': event, 'action': False, 'ticket_types' : ticket_types, 'action': False,'username':username,'st':st,'income': 0,'ticketdict': ticketdict,'total': total,'sold': sold,'perc': perc,'tel': tel })
            except ApiError as e:
                print(tel)
                print(datetime)
                print ('%s - %s' % (e.code, e.message))
                return render(request,'html/essay/sell.html',{'view' : view, 'action': False, 'event': event, 'ticket_types' : ticket_types,'username':username,'st': st, 'income': 0,'ticketdict': ticketdict , 'total': total,'sold': sold,'perc': perc,'tel':e.code})
            
        
        
    else:
        return render(request,'html/essay/sell.html',{'view' : 'Sell', 'action': True, 'event': event,'ticket_types': ticket_types,'username': username,'st':st,'income': 0,'ticketdict': ticketdict,'total': total,'sold': sold,'perc': perc,})
   

    
        
 
            #events=list()
'''
            for obj in objs :
                events.append(obj.event)
                tickets_types=list()
'''
'''
            for event in events:
                global ticket_type
                tickobjs= ticket_type.objects.filter(event = event)
                tickets_types.append('nothing')
                tickets_types[:] = []
                for tickobj in tickobjs:
                    ticket_types.append(tickobj.tike_type)
                    if event not in eventdict:
                        eventdict[event] = list()
                        eventdict[event].append(tickets_types)
'''
@login_required
def search(request):
    return render(request,'html/essay/search.html')

@login_required
def restore(request):      
    return render(request,'html/essay/restore.html',{'view' : 'Restore'})

@login_required
def check(request):
    if request.method == 'POST':
        pin = request.POST['pin']
        try:
            tickobj=ticket.objects.get(Q(pin__exact = pin))
            owner= tickobj. Name
            ticket_type = tickobj.ticket_type
            status = tickobj.status
            if(status == False):
                tickobj.status = True
                status = True
                tickobj.save()
                return render(request,'html/essay/check.html',{'view' : 'Check','status':status,'owner':owner,'ticket_type': ticket_type,'pin':pin})
            else:
                status = False
                return render(request,'html/essay/check.html',{'view' : 'Check','status':status,'owner':owner,'ticket_type': ticket_type})
        except ticket.DoesNotExist:
            status = False
            return render(request,'html/essay/check.html',{'view' : 'Check','status': status,'pin':pin})

   

    else:
        return render(request,'html/essay/check.html',{'view' : 'Check'})
        
def result(request):
    if request.method == 'GET':
        pin= request.GET['pin']
        try:
            tickobj=ticket.objects.get(Q(pin__exact = pin.upper()))
            owner= tickobj.Name
            ticket_type = tickobj.ticket_type
            status = tickobj.status
            if(status == False):
                tickobj.status = True
                status = True
                #tickobj.save()
                result= {'status':status,'owner':owner,'ticket_type': str(ticket_type),'pin':pin}
                return JsonResponse(result)
            else:
                status = False
                result= {'status':status,'owner':owner,'ticket_type': str(ticket_type),'pin':pin} 
                return JsonResponse(result)
        except ticket.DoesNotExist:
            status = False
            result= {'status': False} 
            return JsonResponse(result)

def applogin(request):
    if request.method == 'GET':
        username = request.GET['username']
        password = request.GET['password']
        user = authenticate(username= username, password= password)
        
        if user is not None:
            result = {'status':True}
            return JsonResponse(result)
        else:
            result = {'status': False}
            return JsonResponse(result) 

@login_required
def transfer(request):
    '''
    Munyakabera Jean Claude Log:
    needs major restructure, needs addition to name of the new recipient
    also adding the structure to request the underlying datatypes
    hahaha just a silly way to say that this function is asking for 
    database entries/or data that it did not call or store
    anyway will work on that!
    a better idea would just to update the ticket we are working with
    and give it the new data since we are essentially updating it
    but maybe that is a question for the first developer of this

    again since we are transfering we need new data for the new owner!

    also the generator is not optimal the bare minimum would be to add
    a while loop instead of an if to check if the pin is already available
    but again a better way would be to store or for a better terminology
    cache pins in their own table and clean the cache once every year or once
    it has achieved such and such a size because for the current implementation
    this operation will get .lower().strip() and .lower().strip() and error prone as the tickets get
    increased
    '''
    if request.method == 'POST':
        tel1 = request.POST['tel1']
        tel2 = request.POST['tel2']
        pin = request.POST['pin']
        try:
            '''
            Munyakabera Jean Claude Log:
            under here i have used to the best of my abilities object relations
            doing the same would create more efficient and re-usable code
            '''
            tickobj=ticket.objects.get(Q(phone_number__exact = tel1, pin__exact = pin ))
            eventobj=tickobj.event
            email=tickobj.email
            event=eventobj.title
            datetime=eventobj.date
            name=tickobj.Name
            tobj=tickobj.ticket_type
            ticket_type=tobj.tike_type
            sellerobj=tickobj.seller
            print eventobj.date
            try:
                pinobj=ticket.objects.get(Q(pin__exact = pin))
                if pinobj:
                    pin = id_generator()
            except ticket.DoesNotExist:
                pass
            try:
                api.service('sms').action('send')
                api.set_content('  valid ticket(250)  \nOwner:[%1%]\nEvent: [%2%] \nTicket: [%4%]\nCode:[%3%]\nIssued by Tike ltd \n Visit  \nPlease keep this ticket safe. ')
                api.set_params(name, event+" on"+str(datetime) , pin,ticket_type,) #add some datetime formating
                api.set_to(tel2)
                api.set_from('Tike') #Requested sender name
                result = api.execute()
                for r in result:
                    print (r.id, r.points, r.status)
                '''
                #Munyakabera Jean Claude Log:
                #this is not needed (you wonder what the developer was thinking about :) )
                total = total
                st = st + 1
                sold = sold + 1
                perc = (sold/total)* 100'''
                newticket= ticket.objects.create()
                newticket= ticket(phone_number = tel2, email= email, Name= name, pin = pin, event = eventobj, seller= sellerobj,ticket_type= tobj)
                newticket.save()
                print(pin)
                return render(request,'html/essay/transfer.html',{'view' : 'Transfer','status':1})
            except ApiError as e:
                print(tel)
                print ('%s - %s' % (e.code, e.message))
                return render(request,'html/essay/transfer.html',{'view' : 'Transfer','status':0})
        except ticket.DoesNotExist:
            return render(request,'html/essay/transfer.html',{'view' : 'Transfer','status':0})
    else:
        pass
        return render(request,'html/essay/transfer.html',{'view':'Transfer'})
  

@login_required
def tools(request):
    '''
    Munyakabera jean claude log:
    the following includes tools to be used in getting information
    about the operations being undertaken,it is built to easily add
    new components with time first we get general variables and get
    into a body of IFs depending on the tool requested
    '''
    
    if request.user.is_authenticated():
        username=request.user.username
        sellers=[]
        for profl in profile.objects.all():#.ordey_by('seller__username'):
            sellers.append(profl.seller.username)
        events=[]
        for evnt in Show.objects.all():#.order_by('title'):
            events.append(evnt.title)
        days,months,years=[range(32),range(1,13,1),range(datetime.date.today().year-20,datetime.date.today().year+21)]
        print days
        '''
        with this tools to be able to add different tools and view what you are using
        each tool shall manage it's 'active' key
        put active_toolnum ( for example active_0 for search) into the tab of that tool
        and if that tool is selected send 'active' for that key
        '''
        if request.method=='GET': #post or get? change according to needs
            if "toolnum" in request.GET.keys(): #to see if they want a tool and avoid an error if not
                toolnum=request.GET["toolnum"]
                '''
                Munyakabera Jean Claude log:
                i would like to suggest that there is a more useful way of adding tools the logic of selecting
                them is the same what is different is instead of writing long lines of codes following each
                if statement we make a file "tools.py" then call it and get different tools from there for now
                i won't pursue this approach since i'm supposed to deliver this tonight
                '''
                if toolnum=="0": #search
                    '''
                    foreword it searches tickets with some variables and will search
                    with any number of varible it is given when given a date it will 
                    give all tickets only if the date is a date of 0s(or maybe just the day) otherwise it
                    will give tickets of that date only, oh and it will differentiate 
                    phones with emails so only one field for contact info may add this
                    in the sell view
                    '''
                    search_vars=['event','seller','name','pin','contacts','day','month','year'] #all fields contained in the search page
                    tmp=""
                    search_queries=[Q(event__title=tmp),Q(seller__username=tmp),]
                    query_keywords=Q()
                    date=datetime.date.today()
                    #following is a functional approach to assign values for fields queried accurate only when search is done in a certain order
                    #i think there is a better way to do it in django till then imma use this idea
                    qevent,qseller,qname,qpin,qcontacts,qday,qmonth,qyear=[request.GET[var] for var in search_vars if var in request.GET.keys()]
                    for search_var in search_vars:
                        #print search_var,str(request.GET[search_var])
                        if search_var in request.GET.keys():
                            if search_var=="event" and request.GET[search_var] not in ['',' ',None]:
                                query_keywords= query_keywords & Q(event__title=request.GET[search_var])
                            elif search_var=="name" and request.GET[search_var] != '':
                                query_keywords= query_keywords & Q(Name__contains=request.GET[search_var])
                            elif search_var=="seller" and request.GET[search_var] != '':
                                query_keywords= query_keywords & Q(seller__seller__username=request.GET[search_var])
                            elif search_var=="pin" and request.GET[search_var] != '':
                                query_keywords= query_keywords & Q(pin=request.GET[search_var].upper())
                            elif search_var=="contacts" and request.GET[search_var] != '':
                                if "@" in request.GET[search_var]:
                                    query_keywords= query_keywords & Q(email=request.GET[search_var])
                                elif request.GET[search_var] != '' and search_var != '':
                                    query_keywords= query_keywords & Q(phone_number=int(request.GET[search_var]))
                            elif search_var in ["day",'month','year'] and request.GET[search_var] != '0':
                                if search_var == "day":   
                                    date.replace(day=int(request.GET[search_var]))
                                elif search_var=="month":
                                    date.replace(month=int(request.GET[search_var]))
                                elif search_var=="year":
                                    date.replace(year=int(request.GET[search_var]))
                    '''if date != datetime.date.today():
                        query_keywords= query_keywords #& Q(date__eq=join(date))'''
                    results=''
                    if str(query_keywords)not in ['(AND: )',]:
                        results=ticket.objects.filter(query_keywords)
                    parsed_results=[]
                    print str(query_keywords),'---->',(results)
                    for result in results:
                        parsed_results.append(
                            [str(result.Name).lower().strip(),
                            str(result.event.title).lower().strip(),
                            str(result.ticket_type.tike_type).lower().strip(),
                            str(result.pin).lower().strip(),
                            str(result.seller).lower().strip(),#result.seller result in an error
                            result.date.strftime("%d-%m-%y"),
                            str(result.phone_number),result.status])

                    
                    return render(request,'html/essay/search.html',{"err_disp":'none','active_0':'active','view':str(query_keywords),'days':days,'months':months,'years':years,'sellers':sellers,'events':events,'results':parsed_results,
                        })
                elif toolnum=='1':#seller stats
                    #thinking...
                    #see which show the current user supervise if none KABOOM!
                    try:
                        cur_show=Show.objects.get(Q(supervisor__username=username))
                        show_tickets=cur_show.tickets_no
                        #get available tike types for an efficient price calculator for only that event
                        cur_types=tickettype.objects.filter(event=cur_show)
                        #get all the sellers for this event
                        cur_sellers=profile.objects.filter(event=cur_show)
                        #for each type and seller get all tickets and record how much of each you have
                        crude=[]
                        tot_tickets,tot_money=[0,0]
                        for cur_seller in cur_sellers:
                            amount=0
                            num=0
                            for cur_type in cur_types:
                                factor=cur_type.amount
                                query=ticket.objects.filter(Q(event=cur_show) & Q(ticket_type=cur_type) & Q(seller=cur_seller))
                                amount=amount+(len(query)*factor)
                                num=num+len(query)
                            crude.append([str(cur_seller.seller.username),amount,num])
                            tot_money,tot_tickets=[tot_money+amount,tot_tickets+num]
                        print crude,'\n',
                        perc=int(round(((1.0*tot_tickets)/show_tickets)*100))
                        #the type.amount*len(ticket__of_that_type) is the money we earned do this for each seller
                        return render(request,'html/essay/search.html',{'active_1':'active','view':'tools','days':days,'months':months,'years':years,'sellers':sellers,'events':events,'reports':crude,'tot_money':tot_money,'tot_tickets':tot_tickets,'perc':perc,'show_tickets':show_tickets,"err_disp":'none'})
                    except Exception as e:
                        print e
                        return render(request,'html/essay/search.html',{'active_0':'active','view':'tools','days':days,'months':months,'years':years,'sellers':sellers,'events':events,"err_disp":'',})
        else:
            return render(request,'html/essay/search.html',{"err_disp":'none','active_0':'active','view':'tools','days':days,'months':months,'years':years,'sellers':sellers,'events':events})
        return render(request,'html/essay/search.html',{"err_disp":'none','active_0':'active','view':'tools','days':days,'months':months,'years':years,'sellers':sellers,'events':events})

def overview(request,id):
    try:
        event=Show.objects.get(id=id)
        tiktypes=tickettype.objects.filter(event=event)
        profiles=profile.objects.filter(event=event)
        data=[]
        total=[0,0]
        for prfl in profiles:
            for tkt in tiktypes:
                amount=ticket.objects.filter(event=event,ticket_type=tkt,seller=prfl).count()
                data.append([prfl.seller.username,tkt.tike_type,tkt.amount,
                    amount,amount*tkt.amount])
                total[0]+=amount
                total[1]+=amount*tkt.amount
        print total
        return render(request,'html/essay/overview.html',locals())     
    except:
        return HttpResponseRedirect('/')


def get_ticket(request):
    pin_=request.GET['pin']
    obj=ticket.objects.get(Q(pin__exact = pin_.upper()))
    qr_code_info=web_url+'ticket/'+obj.pin.lower()
    print qr_code_info
    render(request,'html/essay/sell.html',{'obj':obj,'qr_code_info':qr_code_info})
#.strftime("%d-%m-%y")
#.split("@")[0]

#API section: mostly funcs to share and update data     
#it seems i can make one func and exec db request depending on data given                  
def api_update_shows(request):
    #put a field of a password
    '''
    add info in db/Show, checks first if info is already in
    returns item.id,OK if update/create and 0,err.msg if not(error)
    '''
    #gather data,init defaults and remove the unnecessary
    fields={'title':'','poster':'','Description':'',
    'date':'','supervisor':'','tickets_no':''}
    for key in fields.keys():
        if key in request.GET.keys():
            fields[key]=request.GET[key]

    #check if record already exists
    try:
        obj, created = Show.objects.update_or_create(**fields)
        return JsonResponse({'id':obj.id,'stat':'OK'})
    except Exception as err:
        return JsonResponse({'id':0,'stat':str(err)})


def api_update_types(request):
    #put a field of a password
    '''
    add info in db/tickettype, checks first if info is already in
    returns item.id,OK if update/create and 0,err.msg if not(error)
    '''
    #gather data,init defaults and remove the unnecessary
    fields={'event':'','amount':'','tike_type':''}
    for key in fields.keys():
        if key in request.GET.keys():
            fields[key]=request.GET[key]

    #check if record already exists
    try:
        obj, created = tickettype.objects.update_or_create(**fields)
        return JsonResponse({'id':obj.id,'stat':'OK'})
    except Exception as err:
        return JsonResponse({'id':0,'stat':str(err)})

def api_update_profile(request):
    #put a field of a password
    #change to bulk
    #this shall be used mostly to automate profile creation
    '''
    add info in db/profile, checks first if info is already in
    returns item.id,OK if update/create and 0,err.msg if not(error)
    '''
    #gather data,init defaults and remove the unnecessary 
    fields={'seller':'','event':''}
    for key in fields.keys():
        if key in request.GET.keys():
            fields[key]=request.GET[key]

    #check if record already exists
    try:
        obj, created = profile.objects.update_or_create(**fields)
        return JsonResponse({'id':obj.id,'stat':'OK'})
    except Exception as err:
        return JsonResponse({'id':0,'stat':str(err)})

def api_update_ticket(request):
    #put a field of a password
    '''
    add info in db/ticket, checks first if info is already in
    returns item.id,OK if update/create and 0,err.msg if not(error)
    '''
    #gather data,init defaults and remove the unnecessary

    fields={'phone_number':'','email':'','Name':'',
            'pin':'','event':'','seller':'',
            'ticket_type':'','status':'','date':''}
    for key in fields.keys():
        if key in request.GET.keys():
            fields[key]=request.GET[key]

    #check if record already exists
    try:
        obj, created = ticket.objects.update_or_create(**fields)
        return JsonResponse({'id':obj.id,'stat':'OK'})
    except Exception as err:
        return JsonResponse({'id':0,'stat':str(err)})

def api_create_user(request):
    #put a field of a password
    '''
    create user or retrieve one and returns user.id,OK 
    when successful or 0,err 
    '''
    #gather data and defaults
    fields={'username':None,'password':None,'firstName':'','lastName':'','mail':''}
    for key in fields.keys():
        if key in request.GET.keys():
            fields[key]=request.GET[key]

    #check if record already exists 
    try:
        if fields['username'] and fields['password']:
            obj,created = User.objects.get_or_create(username=fields['username'],
                   first_name=fields['firstName'],last_name=fields['lastName'])
            if created:
                obj.set_password(fields['password'])
                return JsonResponse({'id':obj.id,'stat':'OK'})
            else:
                return JsonResponse({'id':obj.id,'stat':'OK'})
        else:
            return JsonResponse({'id':0,'stat':"no username or password sent"})
    except Exception as err:
        return JsonResponse({'id':0,'stat':str(err)})


def download_event_tickets(request,id):
    #add authentication
    if 'timestamp' in request.GET.keys():
        pass #TODO: process the time stamp
    else:
        timestamp=0

    #TODO: IMPLEMENT A BETTER ONE WITHOUT LOOPS
    raw={}
    c=0
    raw['timestamp']=datetime.datetime.now()
    raw['event']=Show.objects.get(id=id).title
    tmp={}
    tickets=ticket.objects.filter(event_id=id)
    for tcket in tickets:
        tmp[tcket.pin]={'name':tcket.Name,'scanned':tcket.status,
        'date':tcket.date}
    raw['tickets']=tmp
    return JsonResponse(raw)

def get_event_ids(request,n=10):
    events=Show.objects.all()
    result={}
    for event in events[:n]:
        result[event.title]=event.id
    return JsonResponse(result)